"""
FastAPI service for election prediction.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import joblib
import numpy as np
from pathlib import Path
import time
import json
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from src.utils.logger import get_logger
from src.utils.config import Config


logger = get_logger(__name__)


# Prometheus metrics
REQUEST_COUNT = Counter(
    'election_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'election_api_request_latency_seconds',
    'API request latency',
    ['method', 'endpoint']
)
PREDICTION_CONFIDENCE = Histogram(
    'election_prediction_confidence',
    'Prediction confidence scores'
)
MODEL_VERSION = Gauge(
    'election_model_version',
    'Current model version'
)


# Pydantic models
class ElectionFeatures(BaseModel):
    """Input features for election prediction."""
    
    # Demographics
    population: float = Field(..., description="Population of the region")
    median_age: float = Field(..., description="Median age")
    median_income: float = Field(..., description="Median income")
    education_rate: float = Field(..., description="Education rate (0-1)")
    urban_ratio: float = Field(..., description="Urban population ratio (0-1)")
    
    # Voting history
    prev_election_turnout: float = Field(..., description="Previous election turnout (0-1)")
    prev_winner_margin: float = Field(..., description="Previous winner margin (-1 to 1)")
    voter_registration_rate: float = Field(..., description="Voter registration rate (0-1)")
    
    # Sentiment
    social_sentiment_score: float = Field(..., description="Social sentiment score (-1 to 1)")
    candidate_a_favorability: float = Field(..., description="Candidate A favorability (0-1)")
    candidate_b_favorability: float = Field(..., description="Candidate B favorability (0-1)")
    
    # Surveys
    poll_candidate_a: float = Field(..., description="Poll support for Candidate A (0-1)")
    poll_candidate_b: float = Field(..., description="Poll support for Candidate B (0-1)")
    undecided_rate: float = Field(..., description="Undecided voters rate (0-1)")
    
    class Config:
        schema_extra = {
            "example": {
                "population": 150000,
                "median_age": 42.5,
                "median_income": 55000,
                "education_rate": 0.85,
                "urban_ratio": 0.7,
                "prev_election_turnout": 0.68,
                "prev_winner_margin": 0.05,
                "voter_registration_rate": 0.82,
                "social_sentiment_score": 0.15,
                "candidate_a_favorability": 0.55,
                "candidate_b_favorability": 0.48,
                "poll_candidate_a": 0.48,
                "poll_candidate_b": 0.45,
                "undecided_rate": 0.07
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    
    predicted_winner: str
    confidence: float
    probabilities: Dict[str, float]
    model_version: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str
    model_loaded: bool
    model_version: str
    timestamp: str


# Initialize FastAPI app
app = FastAPI(
    title="Election Prediction API",
    description="Production-ready API for predicting election outcomes",
    version="1.0.0"
)


class PredictionService:
    """Service for making election predictions."""
    
    def __init__(self):
        """Initialize prediction service."""
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.model_version = Config.MODEL_VERSION
        self.load_model()
    
    def load_model(self):
        """Load the trained model and scaler."""
        try:
            model_path = Config.MODELS_DIR / "best_model.pkl"
            scaler_path = Config.MODELS_DIR / "scaler.pkl"
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found at {model_path}")
            
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
            
            if scaler_path.exists():
                self.scaler = joblib.load(scaler_path)
                logger.info(f"Scaler loaded from {scaler_path}")
            
            # Load feature names from saved file or calculate from training data
            feature_names_path = Config.DATA_DIR / "features" / "feature_names.txt"
            if feature_names_path.exists():
                with open(feature_names_path, 'r') as f:
                    self.feature_names = [line.strip() for line in f.readlines()]
                logger.info(f"Loaded {len(self.feature_names)} feature names")
            else:
                # Fallback: use all features except target and ID
                train_path = Config.DATA_DIR / "features" / "train_features.csv"
                if train_path.exists():
                    import pandas as pd
                    train_df = pd.read_csv(train_path, nrows=1)
                    exclude_cols = [Config.TARGET_COLUMN, 'region_id']
                    self.feature_names = [col for col in train_df.columns if col not in exclude_cols]
                    logger.info(f"Loaded {len(self.feature_names)} feature names from training data")
                else:
                    logger.warning("Could not load feature names")
                    self.feature_names = None
            
            # Update Prometheus metric
            MODEL_VERSION.set(1.0)
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def engineer_features(self, features: Dict[str, float]) -> np.ndarray:
        """
        Engineer features from raw input.
        
        Args:
            features: Raw feature dictionary
        
        Returns:
            Engineered feature array
        """
        import pandas as pd
        from src.data.features import ElectionFeatureEngineering
        
        # Create DataFrame from input
        df = pd.DataFrame([features])
        
        # Apply feature engineering
        feature_engineer = ElectionFeatureEngineering()
        df_engineered = feature_engineer.engineer_features(df)
        
        # Get feature values in correct order
        feature_values = df_engineered[self.feature_names].values[0]
        
        return feature_values
    
    def predict(self, features: ElectionFeatures) -> PredictionResponse:
        """
        Make election prediction.
        
        Args:
            features: Input features
        
        Returns:
            Prediction response
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        # Convert features to dict
        features_dict = features.dict()
        
        # Engineer features
        X = self.engineer_features(features_dict)
        X = X.reshape(1, -1)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        # Map to candidate names
        predicted_winner = "Candidate_A" if prediction == 1 else "Candidate_B"
        confidence = float(max(probabilities))
        
        proba_dict = {
            "Candidate_B": float(probabilities[0]),
            "Candidate_A": float(probabilities[1])
        }
        
        # Update Prometheus metrics
        PREDICTION_CONFIDENCE.observe(confidence)
        
        return PredictionResponse(
            predicted_winner=predicted_winner,
            confidence=confidence,
            probabilities=proba_dict,
            model_version=self.model_version
        )


# Initialize service
prediction_service = PredictionService()


# Middleware for request tracking
@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Track request metrics."""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate latency
    latency = time.time() - start_time
    
    # Update metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(latency)
    
    return response


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "Election Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "metrics": "/metrics"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    from datetime import datetime
    
    return HealthResponse(
        status="healthy",
        model_loaded=prediction_service.model is not None,
        model_version=prediction_service.model_version,
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: ElectionFeatures):
    """
    Predict election outcome.
    
    Args:
        features: Election features
    
    Returns:
        Prediction response with winner and confidence
    """
    try:
        prediction = prediction_service.predict(features)
        return prediction
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", response_model=List[PredictionResponse])
async def predict_batch(features_list: List[ElectionFeatures]):
    """
    Batch prediction endpoint.
    
    Args:
        features_list: List of election features
    
    Returns:
        List of prediction responses
    """
    try:
        predictions = []
        for features in features_list:
            prediction = prediction_service.predict(features)
            predictions.append(prediction)
        return predictions
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/model/info")
async def model_info():
    """Get model information."""
    try:
        metadata_path = Config.MODELS_DIR / "model_metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            return metadata
        else:
            return {
                "model_version": prediction_service.model_version,
                "model_type": type(prediction_service.model).__name__,
                "n_features": len(prediction_service.feature_names) if prediction_service.feature_names else 0
            }
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=Config.API_HOST,
        port=Config.API_PORT,
        workers=Config.API_WORKERS
    )
