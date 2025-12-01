"""
Inference Module
================

This module provides the inference function for the churn prediction model.
"""

import logging
from pathlib import Path
from typing import Dict, List, Union

import numpy as np
import pandas as pd

from churn_mlops.models import ChurnModel

logger = logging.getLogger(__name__)


class ChurnPredictor:
    """
    Inference class for making churn predictions.
    
    This class wraps the trained model and provides a clean interface
    for making predictions in production.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the predictor with a trained model.
        
        Args:
            model_path: Path to the saved model file
        """
        self.model_path = model_path
        self.model = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the model from disk."""
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        self.model = ChurnModel.load(self.model_path)
        logger.info(f"Model loaded from {self.model_path}")
    
    def predict(self, features: Dict[str, Union[float, int, str]]) -> Dict:
        """
        Make a single prediction.
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Dictionary with prediction results:
            {
                "prediction": 0 or 1,
                "churn_probability": float,
                "confidence": float
            }
        """
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # Filter to only include features the model was trained on
        if self.model.feature_names:
            available_features = [f for f in self.model.feature_names if f in df.columns]
            df = df[available_features]
        
        # Make prediction
        prediction = self.model.predict(df)[0]
        probabilities = self.model.predict_proba(df)[0]
        
        result = {
            "prediction": int(prediction),
            "will_churn": bool(prediction == 1),
            "churn_probability": float(probabilities[1]),
            "confidence": float(max(probabilities)),
        }
        
        logger.debug(f"Prediction result: {result}")
        return result
    
    def predict_batch(self, features_list: List[Dict]) -> List[Dict]:
        """
        Make batch predictions.
        
        Args:
            features_list: List of feature dictionaries
            
        Returns:
            List of prediction results
        """
        df = pd.DataFrame(features_list)
        
        # Filter to only include features the model was trained on
        if self.model.feature_names:
            available_features = [f for f in self.model.feature_names if f in df.columns]
            df = df[available_features]
        
        predictions = self.model.predict(df)
        probabilities = self.model.predict_proba(df)
        
        results = []
        for i in range(len(predictions)):
            results.append({
                "prediction": int(predictions[i]),
                "will_churn": bool(predictions[i] == 1),
                "churn_probability": float(probabilities[i][1]),
                "confidence": float(max(probabilities[i])),
            })
        
        return results


# Convenience function for simple inference
def predict(
    features: Dict[str, Union[float, int, str]],
    model_path: str = "models/churn_model.pkl"
) -> Dict:
    """
    Make a prediction using the trained model.
    
    Args:
        features: Dictionary of feature values
        model_path: Path to the saved model
        
    Returns:
        Prediction result dictionary
    """
    predictor = ChurnPredictor(model_path)
    return predictor.predict(features)
