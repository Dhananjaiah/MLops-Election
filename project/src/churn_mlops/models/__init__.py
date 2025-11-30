"""
Models Module
=============

This module handles model training, evaluation, and inference for the
Customer Churn Prediction project.
"""

import pickle
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split, GridSearchCV

logger = logging.getLogger(__name__)


class ChurnModel:
    """
    Wrapper class for churn prediction models.
    
    Supports multiple model types:
    - logistic_regression
    - random_forest
    """
    
    MODEL_TYPES = {
        "logistic_regression": LogisticRegression,
        "random_forest": RandomForestClassifier,
    }
    
    DEFAULT_PARAMS = {
        "logistic_regression": {
            "max_iter": 1000,
            "random_state": 42,
        },
        "random_forest": {
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42,
        },
    }
    
    def __init__(self, model_type: str = "random_forest", **kwargs):
        """
        Initialize the model.
        
        Args:
            model_type: Type of model to use
            **kwargs: Additional parameters for the model
        """
        if model_type not in self.MODEL_TYPES:
            raise ValueError(f"Unknown model type: {model_type}. Choose from {list(self.MODEL_TYPES.keys())}")
        
        self.model_type = model_type
        self.params = {**self.DEFAULT_PARAMS[model_type], **kwargs}
        self.model = self.MODEL_TYPES[model_type](**self.params)
        self._is_fitted = False
        self.feature_names = None
        
        logger.info(f"Initialized {model_type} model with params: {self.params}")
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "ChurnModel":
        """
        Train the model.
        
        Args:
            X: Feature matrix
            y: Target vector
            
        Returns:
            self
        """
        logger.info(f"Training model on {len(X)} samples")
        self.feature_names = list(X.columns) if isinstance(X, pd.DataFrame) else None
        self.model.fit(X, y)
        self._is_fitted = True
        logger.info("Model training complete")
        return self
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of predictions (0 or 1)
        """
        if not self._is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        return self.model.predict(X)
    
    def predict_proba(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Get prediction probabilities.
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of probability pairs [prob_no_churn, prob_churn]
        """
        if not self._is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        return self.model.predict_proba(X)
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            X: Feature matrix
            y: True labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        y_pred = self.predict(X)
        y_proba = self.predict_proba(X)[:, 1]
        
        metrics = {
            "accuracy": accuracy_score(y, y_pred),
            "precision": precision_score(y, y_pred),
            "recall": recall_score(y, y_pred),
            "f1": f1_score(y, y_pred),
            "roc_auc": roc_auc_score(y, y_proba),
        }
        
        logger.info(f"Evaluation metrics: {metrics}")
        return metrics
    
    def save(self, filepath: str) -> None:
        """
        Save the model to disk.
        
        Args:
            filepath: Path to save the model
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
        
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> "ChurnModel":
        """
        Load a model from disk.
        
        Args:
            filepath: Path to the saved model
            
        Returns:
            Loaded model
        """
        with open(filepath, "rb") as f:
            model = pickle.load(f)
        
        logger.info(f"Model loaded from {filepath}")
        return model


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_type: str = "random_forest",
    **model_params
) -> Tuple[ChurnModel, Dict[str, float]]:
    """
    Train and evaluate a model.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        y_test: Test labels
        model_type: Type of model to train
        **model_params: Additional model parameters
        
    Returns:
        Tuple of (trained model, evaluation metrics)
    """
    model = ChurnModel(model_type=model_type, **model_params)
    model.fit(X_train, y_train)
    metrics = model.evaluate(X_test, y_test)
    
    return model, metrics


def hyperparameter_search(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_type: str = "random_forest",
    param_grid: Optional[Dict] = None,
    cv: int = 5
) -> Tuple[Any, Dict]:
    """
    Perform hyperparameter search.
    
    Args:
        X_train: Training features
        y_train: Training labels
        model_type: Type of model to tune
        param_grid: Parameter grid to search
        cv: Number of cross-validation folds
        
    Returns:
        Tuple of (best estimator, best parameters)
    """
    if param_grid is None:
        if model_type == "random_forest":
            param_grid = {
                "n_estimators": [50, 100, 200],
                "max_depth": [5, 10, 15],
            }
        elif model_type == "logistic_regression":
            param_grid = {
                "C": [0.1, 1.0, 10.0],
            }
    
    model_class = ChurnModel.MODEL_TYPES[model_type]
    base_model = model_class()
    
    grid_search = GridSearchCV(
        base_model,
        param_grid,
        cv=cv,
        scoring="f1",
        n_jobs=-1,
    )
    
    logger.info(f"Starting hyperparameter search with {cv}-fold CV")
    grid_search.fit(X_train, y_train)
    
    logger.info(f"Best parameters: {grid_search.best_params_}")
    logger.info(f"Best score: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_, grid_search.best_params_
