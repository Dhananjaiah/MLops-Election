"""
FastAPI Application for Churn Prediction
========================================

This module provides a REST API for the churn prediction model.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Import model inference module
# Note: Import will be available when running from project root
try:
    from churn_mlops.models.inference import ChurnPredictor
except ImportError:
    ChurnPredictor = None  # Will fail gracefully if model not available

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Customer Churn Prediction API",
    description="REST API for predicting customer churn using machine learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Model path from environment or default
MODEL_PATH = os.getenv("MODEL_PATH", "models/churn_model.pkl")

# Global predictor instance (lazy loaded)
_predictor: Optional["ChurnPredictor"] = None


def get_predictor():
    """Get or create predictor instance."""
    global _predictor
    if _predictor is None:
        if ChurnPredictor is None:
            raise HTTPException(
                status_code=503,
                detail="Model inference module not available"
            )
        if not Path(MODEL_PATH).exists():
            raise HTTPException(
                status_code=503,
                detail=f"Model not found at {MODEL_PATH}. Please train a model first."
            )
        _predictor = ChurnPredictor(MODEL_PATH)
    return _predictor


# Request/Response Models
class CustomerFeatures(BaseModel):
    """Input features for a single customer."""
    tenure: float = Field(..., ge=0, description="Number of months as customer")
    monthly_charges: float = Field(..., ge=0, description="Monthly charges in dollars")
    total_charges: float = Field(..., ge=0, description="Total charges to date")
    
    # Optional features with defaults
    contract_type: Optional[str] = Field("month-to-month", description="Contract type")
    payment_method: Optional[str] = Field("credit_card", description="Payment method")
    internet_service: Optional[str] = Field("fiber_optic", description="Internet service type")
    tech_support: Optional[str] = Field("no", description="Has tech support")
    online_security: Optional[str] = Field("no", description="Has online security")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tenure": 24,
                "monthly_charges": 65.50,
                "total_charges": 1572.00,
                "contract_type": "one_year",
                "payment_method": "credit_card",
                "internet_service": "fiber_optic",
                "tech_support": "yes",
                "online_security": "yes",
            }
        }


class PredictionResponse(BaseModel):
    """Prediction response for a single customer."""
    prediction: int = Field(..., description="0 = No Churn, 1 = Churn")
    will_churn: bool = Field(..., description="Whether customer is predicted to churn")
    churn_probability: float = Field(..., ge=0, le=1, description="Probability of churn")
    confidence: float = Field(..., ge=0, le=1, description="Model confidence")


class BatchPredictionRequest(BaseModel):
    """Request body for batch predictions."""
    customers: List[CustomerFeatures] = Field(..., description="List of customers")


class BatchPredictionResponse(BaseModel):
    """Response for batch predictions."""
    predictions: List[PredictionResponse]
    total_customers: int
    predicted_churners: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    model_loaded: bool
    version: str


class ModelInfoResponse(BaseModel):
    """Model information response."""
    model_type: str
    model_path: str
    features: Optional[List[str]]
    version: str


# API Endpoints
@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Customer Churn Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API and model.
    """
    model_loaded = False
    try:
        if Path(MODEL_PATH).exists():
            model_loaded = True
    except Exception:
        pass
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        model_loaded=model_loaded,
        version="1.0.0",
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_single(customer: CustomerFeatures):
    """
    Make a prediction for a single customer.
    
    Returns the churn prediction and probability.
    """
    try:
        predictor = get_predictor()
        features = customer.model_dump()
        result = predictor.predict(features)
        
        return PredictionResponse(**result)
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Predictions"])
async def predict_batch(request: BatchPredictionRequest):
    """
    Make predictions for multiple customers.
    
    Returns predictions for all customers in the batch.
    """
    try:
        predictor = get_predictor()
        features_list = [c.model_dump() for c in request.customers]
        results = predictor.predict_batch(features_list)
        
        predictions = [PredictionResponse(**r) for r in results]
        predicted_churners = sum(1 for p in predictions if p.will_churn)
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_customers=len(predictions),
            predicted_churners=predicted_churners,
        )
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


@app.get("/model/info", response_model=ModelInfoResponse, tags=["Model"])
async def model_info():
    """
    Get information about the loaded model.
    """
    try:
        predictor = get_predictor()
        return ModelInfoResponse(
            model_type=predictor.model.model_type,
            model_path=MODEL_PATH,
            features=predictor.model.feature_names,
            version="1.0.0",
        )
    except Exception as e:
        return ModelInfoResponse(
            model_type="unknown",
            model_path=MODEL_PATH,
            features=None,
            version="1.0.0",
        )


# Run with: uvicorn churn_mlops.serving.app:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
