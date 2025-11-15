"""
Model training with MLflow tracking.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import joblib

from src.utils.logger import get_logger
from src.utils.config import Config
from src.data.features import ElectionFeatureEngineering


logger = get_logger(__name__)


class ElectionModelTrainer:
    """Train election prediction models with MLflow tracking."""
    
    def __init__(self, experiment_name: str = None):
        """
        Initialize trainer.
        
        Args:
            experiment_name: MLflow experiment name
        """
        self.experiment_name = experiment_name or Config.MLFLOW_EXPERIMENT_NAME
        mlflow.set_tracking_uri(Config.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(self.experiment_name)
        
        self.models = {
            "random_forest": RandomForestClassifier(random_state=Config.RANDOM_STATE),
            "xgboost": XGBClassifier(
                random_state=Config.RANDOM_STATE,
                eval_metric='logloss'
            ),
            "logistic_regression": LogisticRegression(random_state=Config.RANDOM_STATE)
        }
        
        logger.info(f"Initialized trainer with experiment: {self.experiment_name}")
    
    def prepare_data(
        self,
        df: pd.DataFrame,
        feature_columns: list
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features and target from DataFrame.
        
        Args:
            df: Input DataFrame
            feature_columns: List of feature column names
        
        Returns:
            Tuple of (X, y)
        """
        X = df[feature_columns].values
        y = df[Config.TARGET_COLUMN].values
        
        # Encode target
        y = np.where(y == "Candidate_A", 1, 0)
        
        return X, y
    
    def train_model(
        self,
        model_name: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        hyperparameters: Dict[str, Any] = None
    ) -> Any:
        """
        Train a single model with hyperparameter tuning.
        
        Args:
            model_name: Name of the model to train
            X_train: Training features
            y_train: Training target
            hyperparameters: Hyperparameter grid for tuning
        
        Returns:
            Trained model
        """
        logger.info(f"Training {model_name}...")
        
        model = self.models[model_name]
        
        if hyperparameters:
            logger.info(f"Performing grid search with parameters: {hyperparameters}")
            grid_search = GridSearchCV(
                model,
                hyperparameters,
                cv=5,
                scoring='accuracy',
                n_jobs=-1,
                verbose=1
            )
            grid_search.fit(X_train, y_train)
            
            logger.info(f"Best parameters: {grid_search.best_params_}")
            logger.info(f"Best CV score: {grid_search.best_score_:.4f}")
            
            return grid_search.best_estimator_
        else:
            model.fit(X_train, y_train)
            return model
    
    def train_with_mlflow(
        self,
        model_name: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        feature_names: list,
        hyperparameters: Dict[str, Any] = None
    ) -> Tuple[Any, str]:
        """
        Train model with full MLflow tracking.
        
        Args:
            model_name: Name of the model
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            feature_names: List of feature names
            hyperparameters: Hyperparameter grid
        
        Returns:
            Tuple of (trained_model, run_id)
        """
        with mlflow.start_run(run_name=f"{model_name}_training") as run:
            # Log parameters
            mlflow.log_param("model_type", model_name)
            mlflow.log_param("n_features", X_train.shape[1])
            mlflow.log_param("n_train_samples", X_train.shape[0])
            mlflow.log_param("n_test_samples", X_test.shape[0])
            
            if hyperparameters:
                mlflow.log_params({f"hyperparam_{k}": str(v) for k, v in hyperparameters.items()})
            
            # Train model
            model = self.train_model(model_name, X_train, y_train, hyperparameters)
            
            # Make predictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            y_test_proba = model.predict_proba(X_test)
            
            # Calculate metrics
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
            
            train_accuracy = accuracy_score(y_train, y_train_pred)
            test_accuracy = accuracy_score(y_test, y_test_pred)
            test_precision = precision_score(y_test, y_test_pred, average='binary')
            test_recall = recall_score(y_test, y_test_pred, average='binary')
            test_f1 = f1_score(y_test, y_test_pred, average='binary')
            test_roc_auc = roc_auc_score(y_test, y_test_proba[:, 1])
            
            # Log metrics
            mlflow.log_metric("train_accuracy", train_accuracy)
            mlflow.log_metric("test_accuracy", test_accuracy)
            mlflow.log_metric("test_precision", test_precision)
            mlflow.log_metric("test_recall", test_recall)
            mlflow.log_metric("test_f1", test_f1)
            mlflow.log_metric("test_roc_auc", test_roc_auc)
            
            # Log model
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name=f"{Config.MLFLOW_MODEL_REGISTRY_NAME}_{model_name}"
            )
            
            # Log feature importance if available
            if hasattr(model, 'feature_importances_'):
                importance_df = pd.DataFrame({
                    'feature': feature_names,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                importance_path = Path("/tmp/feature_importance.csv")
                importance_df.to_csv(importance_path, index=False)
                mlflow.log_artifact(importance_path)
            
            logger.info(f"{model_name} - Test Accuracy: {test_accuracy:.4f}, F1: {test_f1:.4f}, ROC-AUC: {test_roc_auc:.4f}")
            
            return model, run.info.run_id
    
    def train_all_models(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        feature_names: list
    ) -> Dict[str, Tuple[Any, str, float]]:
        """
        Train all configured models.
        
        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            feature_names: List of feature names
        
        Returns:
            Dictionary of model results
        """
        results = {}
        
        for model_name in Config.MODELS_TO_TRAIN:
            logger.info(f"\n{'='*60}")
            logger.info(f"Training {model_name}")
            logger.info(f"{'='*60}")
            
            hyperparameters = Config.HYPERPARAMETERS.get(model_name)
            
            model, run_id = self.train_with_mlflow(
                model_name,
                X_train,
                y_train,
                X_test,
                y_test,
                feature_names,
                hyperparameters
            )
            
            # Calculate test accuracy for comparison
            from sklearn.metrics import accuracy_score
            test_accuracy = accuracy_score(y_test, model.predict(X_test))
            
            results[model_name] = (model, run_id, test_accuracy)
        
        return results
    
    def save_best_model(
        self,
        results: Dict[str, Tuple[Any, str, float]],
        output_path: Path
    ) -> str:
        """
        Save the best performing model.
        
        Args:
            results: Dictionary of model results
            output_path: Path to save the model
        
        Returns:
            Name of the best model
        """
        # Find best model based on test accuracy
        best_model_name = max(results.items(), key=lambda x: x[1][2])[0]
        best_model, run_id, accuracy = results[best_model_name]
        
        logger.info(f"\nBest model: {best_model_name} with accuracy: {accuracy:.4f}")
        
        # Save model
        output_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(best_model, output_path)
        logger.info(f"Best model saved to {output_path}")
        
        # Save metadata
        metadata = {
            "model_name": best_model_name,
            "accuracy": accuracy,
            "run_id": run_id,
            "model_path": str(output_path)
        }
        
        metadata_path = output_path.parent / "model_metadata.json"
        import json
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return best_model_name


def main():
    """Main training function."""
    logger.info("Starting model training pipeline...")
    
    # Load feature-engineered data
    train_path = Config.DATA_DIR / "features" / "train_features.csv"
    test_path = Config.DATA_DIR / "features" / "test_features.csv"
    
    if not train_path.exists() or not test_path.exists():
        logger.error("Feature data not found. Please run feature engineering first.")
        return
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    logger.info(f"Loaded train data: {train_df.shape}")
    logger.info(f"Loaded test data: {test_df.shape}")
    
    # Get feature names
    feature_engineer = ElectionFeatureEngineering()
    train_df_with_features = feature_engineer.engineer_features(pd.DataFrame())  # Just to get feature names
    feature_names = feature_engineer.get_all_feature_names()
    
    logger.info(f"Using {len(feature_names)} features")
    
    # Initialize trainer
    trainer = ElectionModelTrainer()
    
    # Prepare data
    X_train, y_train = trainer.prepare_data(train_df, feature_names)
    X_test, y_test = trainer.prepare_data(test_df, feature_names)
    
    logger.info(f"Training data shape: X={X_train.shape}, y={y_train.shape}")
    logger.info(f"Test data shape: X={X_test.shape}, y={y_test.shape}")
    
    # Train all models
    results = trainer.train_all_models(
        X_train,
        y_train,
        X_test,
        y_test,
        feature_names
    )
    
    # Save best model
    best_model_path = Config.MODELS_DIR / "best_model.pkl"
    best_model_name = trainer.save_best_model(results, best_model_path)
    
    logger.info(f"\n{'='*60}")
    logger.info("Training completed successfully!")
    logger.info(f"Best model: {best_model_name}")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    main()
