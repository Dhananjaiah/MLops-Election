"""
Training Pipeline
=================

Orchestration pipeline for end-to-end model training.
This is a simple example that can be extended with proper orchestrators
like Airflow, Prefect, or Kubeflow.
"""

import logging
from datetime import datetime
from typing import Dict, Optional

from churn_mlops.data import generate_sample_data, validate_data
from churn_mlops.features import FeatureEngineer, handle_missing_values, create_derived_features
from churn_mlops.models import train_model

logger = logging.getLogger(__name__)


class TrainingPipeline:
    """
    End-to-end training pipeline for churn prediction.
    
    Steps:
    1. Load data
    2. Validate data
    3. Handle missing values
    4. Create features
    5. Engineer features
    6. Split data
    7. Train model
    8. Evaluate model
    9. Save model
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the pipeline.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.metrics = {}
        self.model = None
        
    def run(self, data_path: Optional[str] = None) -> Dict:
        """
        Execute the full training pipeline.
        
        Args:
            data_path: Path to input data (uses synthetic if not provided)
            
        Returns:
            Dictionary with run results
        """
        logger.info(f"Starting training pipeline run: {self.run_id}")
        
        # Step 1: Load data
        logger.info("Step 1: Loading data")
        if data_path:
            from churn_mlops.data import load_csv
            df = load_csv(data_path)
        else:
            df = generate_sample_data(n_samples=5000)
        
        # Step 2: Validate data
        logger.info("Step 2: Validating data")
        validate_data(df, required_columns=["churn"])
        
        # Step 3: Handle missing values
        logger.info("Step 3: Handling missing values")
        df = handle_missing_values(df)
        
        # Step 4: Create derived features
        logger.info("Step 4: Creating derived features")
        df = create_derived_features(df)
        
        # Step 5: Prepare features
        logger.info("Step 5: Preparing features")
        target = "churn"
        exclude_cols = [target, "customer_id"]
        
        # For simplicity, use only numeric columns
        df_numeric = df.select_dtypes(include=['number'])
        feature_cols = [c for c in df_numeric.columns if c not in exclude_cols]
        
        X = df_numeric[feature_cols]
        y = df[target]
        
        # Step 6: Split data
        logger.info("Step 6: Splitting data")
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Step 7 & 8: Train and evaluate
        logger.info("Step 7-8: Training and evaluating model")
        model_type = self.config.get("model_type", "random_forest")
        self.model, self.metrics = train_model(
            X_train, y_train, X_test, y_test, model_type=model_type
        )
        
        # Step 9: Save model
        logger.info("Step 9: Saving model")
        model_path = self.config.get("model_path", "models/churn_model.pkl")
        self.model.save(model_path)
        
        result = {
            "run_id": self.run_id,
            "status": "success",
            "model_path": model_path,
            "metrics": self.metrics,
            "samples_trained": len(X_train),
            "samples_tested": len(X_test),
        }
        
        logger.info(f"Pipeline complete: {result}")
        return result


def run_training_pipeline(config: Optional[Dict] = None) -> Dict:
    """
    Convenience function to run the training pipeline.
    
    Args:
        config: Pipeline configuration
        
    Returns:
        Pipeline results
    """
    pipeline = TrainingPipeline(config)
    return pipeline.run()


if __name__ == "__main__":
    # Run pipeline
    logging.basicConfig(level=logging.INFO)
    result = run_training_pipeline()
    print(f"\nPipeline completed successfully!")
    print(f"Run ID: {result['run_id']}")
    print(f"Metrics: {result['metrics']}")
