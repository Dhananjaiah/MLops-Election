"""
Configuration management for the election prediction system.
"""

import os
from pathlib import Path
from typing import Any, Dict


class Config:
    """Central configuration for the election prediction system."""
    
    # Base paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Data configuration
    RAW_DATA_PATH = DATA_DIR / "raw" / "election_data.csv"
    PROCESSED_DATA_PATH = DATA_DIR / "processed" / "election_processed.csv"
    FEATURES_PATH = DATA_DIR / "features" / "election_features.csv"
    
    # Model configuration
    MODEL_NAME = "election_predictor"
    MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    
    # MLflow configuration
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    MLFLOW_EXPERIMENT_NAME = "election_prediction"
    MLFLOW_MODEL_REGISTRY_NAME = "election_model"
    
    # Training configuration
    MODELS_TO_TRAIN = ["random_forest", "xgboost", "logistic_regression"]
    HYPERPARAMETERS = {
        "random_forest": {
            "n_estimators": [100, 200],
            "max_depth": [10, 20, None],
            "min_samples_split": [2, 5]
        },
        "xgboost": {
            "n_estimators": [100, 200],
            "max_depth": [3, 5, 7],
            "learning_rate": [0.01, 0.1]
        },
        "logistic_regression": {
            "C": [0.1, 1.0, 10.0],
            "max_iter": [1000]
        }
    }
    
    # API configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_WORKERS = int(os.getenv("API_WORKERS", "4"))
    
    # Monitoring configuration
    DRIFT_THRESHOLD = float(os.getenv("DRIFT_THRESHOLD", "0.1"))
    METRICS_PORT = int(os.getenv("METRICS_PORT", "8001"))
    
    # Feature columns
    DEMOGRAPHIC_FEATURES = [
        "population",
        "median_age",
        "median_income",
        "education_rate",
        "urban_ratio"
    ]
    
    VOTING_HISTORY_FEATURES = [
        "prev_election_turnout",
        "prev_winner_margin",
        "voter_registration_rate"
    ]
    
    SENTIMENT_FEATURES = [
        "social_sentiment_score",
        "candidate_a_favorability",
        "candidate_b_favorability"
    ]
    
    SURVEY_FEATURES = [
        "poll_candidate_a",
        "poll_candidate_b",
        "undecided_rate"
    ]
    
    ALL_FEATURES = (
        DEMOGRAPHIC_FEATURES +
        VOTING_HISTORY_FEATURES +
        SENTIMENT_FEATURES +
        SURVEY_FEATURES
    )
    
    TARGET_COLUMN = "winning_candidate"
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        for directory in [cls.DATA_DIR, cls.MODELS_DIR, cls.LOGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
            for subdir in ["raw", "processed", "features"]:
                (directory / subdir).mkdir(exist_ok=True) if directory == cls.DATA_DIR else None
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return {
            "model_name": cls.MODEL_NAME,
            "model_version": cls.MODEL_VERSION,
            "mlflow_tracking_uri": cls.MLFLOW_TRACKING_URI,
            "random_state": cls.RANDOM_STATE,
            "test_size": cls.TEST_SIZE,
            "drift_threshold": cls.DRIFT_THRESHOLD
        }
