"""
Training Script
===============

Main script for training the churn prediction model.
"""

import argparse
import logging
import yaml
from pathlib import Path

from churn_mlops.data import load_csv, generate_sample_data, validate_data
from churn_mlops.features import FeatureEngineer, create_derived_features, handle_missing_values
from churn_mlops.models import ChurnModel, train_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main(config_path: str = None):
    """
    Main training function.
    
    Args:
        config_path: Path to configuration file
    """
    logger.info("Starting training pipeline")
    
    # Load config or use defaults
    if config_path and Path(config_path).exists():
        config = load_config(config_path)
    else:
        config = {
            "model": {
                "type": "random_forest",
                "params": {
                    "n_estimators": 100,
                    "max_depth": 10,
                }
            },
            "data": {
                "test_size": 0.2,
                "random_state": 42,
            },
            "output": {
                "model_path": "models/churn_model.pkl",
            }
        }
    
    # Generate or load data
    logger.info("Loading data")
    # TODO: Replace with actual data loading in production
    df = generate_sample_data(n_samples=5000)
    
    # Validate data
    validate_data(df, required_columns=["churn"])
    
    # Handle missing values
    df = handle_missing_values(df)
    
    # Create derived features
    df = create_derived_features(df)
    
    # Prepare features and target
    target_column = "churn"
    feature_columns = [col for col in df.columns if col not in [target_column, "customer_id"]]
    
    # Handle categorical columns for demo
    df_numeric = df[feature_columns].select_dtypes(include=['number'])
    
    X = df_numeric
    y = df[target_column]
    
    # Split data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config["data"]["test_size"],
        random_state=config["data"]["random_state"],
        stratify=y
    )
    
    logger.info(f"Training set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    
    # Train model
    model, metrics = train_model(
        X_train, y_train,
        X_test, y_test,
        model_type=config["model"]["type"],
        **config["model"]["params"]
    )
    
    # Log metrics
    logger.info("Training Results:")
    for metric, value in metrics.items():
        logger.info(f"  {metric}: {value:.4f}")
    
    # Save model
    model_path = config["output"]["model_path"]
    model.save(model_path)
    
    logger.info(f"Training complete. Model saved to {model_path}")
    
    return model, metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train churn prediction model")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    args = parser.parse_args()
    
    main(args.config)
