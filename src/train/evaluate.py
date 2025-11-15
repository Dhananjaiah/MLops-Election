"""
Model evaluation and metrics calculation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
import joblib
import json
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.logger import get_logger
from src.utils.config import Config


logger = get_logger(__name__)


class ModelEvaluator:
    """Evaluate election prediction models."""
    
    def __init__(self, model_path: Path = None):
        """
        Initialize evaluator.
        
        Args:
            model_path: Path to the trained model
        """
        self.model_path = model_path or Config.MODELS_DIR / "best_model.pkl"
        self.model = None
        self.metrics = {}
    
    def load_model(self):
        """Load the trained model."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        self.model = joblib.load(self.model_path)
        logger.info(f"Model loaded from {self.model_path}")
    
    def calculate_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_proba: np.ndarray = None
    ) -> Dict[str, float]:
        """
        Calculate comprehensive evaluation metrics.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Prediction probabilities
        
        Returns:
            Dictionary of metrics
        """
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average='binary'),
            "recall": recall_score(y_true, y_pred, average='binary'),
            "f1_score": f1_score(y_true, y_pred, average='binary'),
            "precision_macro": precision_score(y_true, y_pred, average='macro'),
            "recall_macro": recall_score(y_true, y_pred, average='macro'),
            "f1_macro": f1_score(y_true, y_pred, average='macro'),
        }
        
        if y_proba is not None:
            metrics["roc_auc"] = roc_auc_score(y_true, y_proba[:, 1])
        
        return metrics
    
    def evaluate(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        dataset_name: str = "test"
    ) -> Dict[str, Any]:
        """
        Evaluate model on test data.
        
        Args:
            X_test: Test features
            y_test: Test labels
            dataset_name: Name of the dataset being evaluated
        
        Returns:
            Evaluation results dictionary
        """
        if self.model is None:
            self.load_model()
        
        logger.info(f"Evaluating model on {dataset_name} dataset...")
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)
        
        # Calculate metrics
        metrics = self.calculate_metrics(y_test, y_pred, y_proba)
        
        # Calculate confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Generate classification report
        class_report = classification_report(
            y_test,
            y_pred,
            target_names=["Candidate_B", "Candidate_A"],
            output_dict=True
        )
        
        results = {
            "dataset": dataset_name,
            "metrics": metrics,
            "confusion_matrix": cm.tolist(),
            "classification_report": class_report,
            "predictions": {
                "y_pred": y_pred.tolist(),
                "y_proba": y_proba.tolist()
            }
        }
        
        # Log metrics
        logger.info(f"\n{'='*60}")
        logger.info(f"Evaluation Results - {dataset_name}")
        logger.info(f"{'='*60}")
        for metric, value in metrics.items():
            logger.info(f"{metric}: {value:.4f}")
        logger.info(f"{'='*60}\n")
        
        return results
    
    def evaluate_fairness(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        sensitive_feature: np.ndarray,
        sensitive_feature_name: str
    ) -> Dict[str, Any]:
        """
        Evaluate model fairness across demographic groups.
        
        Args:
            X_test: Test features
            y_test: Test labels
            sensitive_feature: Sensitive feature values (e.g., demographic group)
            sensitive_feature_name: Name of the sensitive feature
        
        Returns:
            Fairness evaluation results
        """
        if self.model is None:
            self.load_model()
        
        logger.info(f"Evaluating fairness for {sensitive_feature_name}...")
        
        y_pred = self.model.predict(X_test)
        
        # Split by sensitive feature
        unique_groups = np.unique(sensitive_feature)
        group_metrics = {}
        
        for group in unique_groups:
            mask = sensitive_feature == group
            if mask.sum() == 0:
                continue
            
            y_true_group = y_test[mask]
            y_pred_group = y_pred[mask]
            
            metrics = {
                "accuracy": accuracy_score(y_true_group, y_pred_group),
                "precision": precision_score(y_true_group, y_pred_group, average='binary', zero_division=0),
                "recall": recall_score(y_true_group, y_pred_group, average='binary', zero_division=0),
                "f1_score": f1_score(y_true_group, y_pred_group, average='binary', zero_division=0),
                "sample_size": mask.sum()
            }
            
            group_metrics[str(group)] = metrics
        
        # Calculate disparities
        accuracies = [m["accuracy"] for m in group_metrics.values()]
        disparity = max(accuracies) - min(accuracies) if accuracies else 0
        
        results = {
            "sensitive_feature": sensitive_feature_name,
            "group_metrics": group_metrics,
            "accuracy_disparity": disparity
        }
        
        logger.info(f"Fairness evaluation completed. Accuracy disparity: {disparity:.4f}")
        
        return results
    
    def plot_confusion_matrix(
        self,
        cm: np.ndarray,
        output_path: Path
    ):
        """
        Plot confusion matrix.
        
        Args:
            cm: Confusion matrix
            output_path: Path to save the plot
        """
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=["Candidate_B", "Candidate_A"],
            yticklabels=["Candidate_B", "Candidate_A"]
        )
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        logger.info(f"Confusion matrix plot saved to {output_path}")
    
    def plot_roc_curve(
        self,
        y_test: np.ndarray,
        y_proba: np.ndarray,
        output_path: Path
    ):
        """
        Plot ROC curve.
        
        Args:
            y_test: Test labels
            y_proba: Prediction probabilities
            output_path: Path to save the plot
        """
        fpr, tpr, _ = roc_curve(y_test, y_proba[:, 1])
        roc_auc = roc_auc_score(y_test, y_proba[:, 1])
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        logger.info(f"ROC curve plot saved to {output_path}")
    
    def generate_evaluation_report(
        self,
        results: Dict[str, Any],
        output_path: Path
    ):
        """
        Generate comprehensive evaluation report.
        
        Args:
            results: Evaluation results
            output_path: Path to save the report
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Evaluation report saved to {output_path}")


def main():
    """Main evaluation function."""
    logger.info("Starting model evaluation...")
    
    # Load test data
    test_path = Config.DATA_DIR / "features" / "test_features.csv"
    
    if not test_path.exists():
        logger.error("Test data not found. Please run feature engineering first.")
        return
    
    test_df = pd.read_csv(test_path)
    logger.info(f"Loaded test data: {test_df.shape}")
    
    # Get feature names
    from src.data.features import ElectionFeatureEngineering
    feature_engineer = ElectionFeatureEngineering()
    feature_engineer.engineer_features(pd.DataFrame())  # Just to initialize
    feature_names = feature_engineer.get_all_feature_names()
    
    # Prepare data
    X_test = test_df[feature_names].values
    y_test = np.where(test_df[Config.TARGET_COLUMN].values == "Candidate_A", 1, 0)
    
    # Initialize evaluator
    evaluator = ModelEvaluator()
    evaluator.load_model()
    
    # Evaluate model
    results = evaluator.evaluate(X_test, y_test, dataset_name="test")
    
    # Generate plots
    plots_dir = Config.BASE_DIR / "reports" / "figures"
    plots_dir.mkdir(parents=True, exist_ok=True)
    
    cm = np.array(results["confusion_matrix"])
    evaluator.plot_confusion_matrix(cm, plots_dir / "confusion_matrix.png")
    
    y_proba = np.array(results["predictions"]["y_proba"])
    evaluator.plot_roc_curve(y_test, y_proba, plots_dir / "roc_curve.png")
    
    # Save evaluation report
    report_path = Config.BASE_DIR / "reports" / "evaluation_report.json"
    evaluator.generate_evaluation_report(results, report_path)
    
    logger.info("Model evaluation completed successfully!")


if __name__ == "__main__":
    main()
