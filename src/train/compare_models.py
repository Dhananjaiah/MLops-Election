"""
Compare multiple models and select the best one.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.logger import get_logger
from src.utils.config import Config


logger = get_logger(__name__)


class ModelComparator:
    """Compare multiple trained models."""
    
    def __init__(self):
        """Initialize model comparator."""
        self.models = {}
        self.results = {}
    
    def load_models(self, models_dir: Path):
        """
        Load all models from directory.
        
        Args:
            models_dir: Directory containing model files
        """
        model_files = list(models_dir.glob("*.pkl"))
        
        for model_file in model_files:
            if "scaler" in model_file.name or "best_model" in model_file.name:
                continue
            
            model_name = model_file.stem
            try:
                self.models[model_name] = joblib.load(model_file)
                logger.info(f"Loaded model: {model_name}")
            except Exception as e:
                logger.warning(f"Failed to load {model_name}: {e}")
    
    def compare_models(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> pd.DataFrame:
        """
        Compare all loaded models on test data.
        
        Args:
            X_test: Test features
            y_test: Test labels
        
        Returns:
            DataFrame with comparison results
        """
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            roc_auc_score
        )
        
        logger.info("Comparing models...")
        
        comparison_data = []
        
        for model_name, model in self.models.items():
            try:
                # Make predictions
                y_pred = model.predict(X_test)
                y_proba = model.predict_proba(X_test)
                
                # Calculate metrics
                metrics = {
                    "Model": model_name,
                    "Accuracy": accuracy_score(y_test, y_pred),
                    "Precision": precision_score(y_test, y_pred, average='binary'),
                    "Recall": recall_score(y_test, y_pred, average='binary'),
                    "F1-Score": f1_score(y_test, y_pred, average='binary'),
                    "ROC-AUC": roc_auc_score(y_test, y_proba[:, 1])
                }
                
                comparison_data.append(metrics)
                self.results[model_name] = metrics
                
            except Exception as e:
                logger.error(f"Error evaluating {model_name}: {e}")
        
        df_comparison = pd.DataFrame(comparison_data)
        
        if not df_comparison.empty:
            df_comparison = df_comparison.sort_values("Accuracy", ascending=False)
            logger.info(f"\n{df_comparison.to_string(index=False)}")
        
        return df_comparison
    
    def plot_comparison(
        self,
        df_comparison: pd.DataFrame,
        output_path: Path
    ):
        """
        Create comparison visualization.
        
        Args:
            df_comparison: Comparison results DataFrame
            output_path: Path to save the plot
        """
        if df_comparison.empty:
            logger.warning("No comparison data to plot")
            return
        
        # Prepare data for plotting
        metrics = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
        df_plot = df_comparison.set_index("Model")[metrics]
        
        # Create subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        # Plot each metric
        for idx, metric in enumerate(metrics):
            ax = axes[idx]
            df_plot[metric].plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title(f'{metric} Comparison', fontsize=12, fontweight='bold')
            ax.set_ylabel(metric)
            ax.set_xlabel('Model')
            ax.set_ylim([0, 1])
            ax.grid(axis='y', alpha=0.3)
            ax.tick_params(axis='x', rotation=45)
        
        # Overall comparison
        ax = axes[5]
        df_plot.T.plot(kind='line', ax=ax, marker='o', linewidth=2)
        ax.set_title('Overall Metrics Comparison', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score')
        ax.set_xlabel('Metric')
        ax.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(alpha=0.3)
        ax.set_ylim([0, 1])
        
        plt.tight_layout()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Comparison plot saved to {output_path}")
    
    def select_best_model(
        self,
        df_comparison: pd.DataFrame,
        criterion: str = "F1-Score"
    ) -> str:
        """
        Select the best model based on a criterion.
        
        Args:
            df_comparison: Comparison results DataFrame
            criterion: Metric to use for selection
        
        Returns:
            Name of the best model
        """
        if df_comparison.empty:
            logger.error("No models to compare")
            return None
        
        best_model = df_comparison.loc[df_comparison[criterion].idxmax(), "Model"]
        best_score = df_comparison[criterion].max()
        
        logger.info(f"Best model: {best_model} with {criterion}={best_score:.4f}")
        
        return best_model
    
    def generate_comparison_report(
        self,
        df_comparison: pd.DataFrame,
        output_path: Path
    ):
        """
        Generate comprehensive comparison report.
        
        Args:
            df_comparison: Comparison results
            output_path: Path to save the report
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = {
            "comparison": df_comparison.to_dict(orient='records'),
            "best_model": {
                "by_accuracy": self.select_best_model(df_comparison, "Accuracy"),
                "by_f1": self.select_best_model(df_comparison, "F1-Score"),
                "by_roc_auc": self.select_best_model(df_comparison, "ROC-AUC")
            },
            "summary_statistics": {
                "mean": df_comparison.select_dtypes(include=[np.number]).mean().to_dict(),
                "std": df_comparison.select_dtypes(include=[np.number]).std().to_dict(),
                "min": df_comparison.select_dtypes(include=[np.number]).min().to_dict(),
                "max": df_comparison.select_dtypes(include=[np.number]).max().to_dict()
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Comparison report saved to {output_path}")


def main():
    """Main comparison function."""
    logger.info("Starting model comparison...")
    
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
    feature_engineer.engineer_features(pd.DataFrame())
    feature_names = feature_engineer.get_all_feature_names()
    
    # Prepare data
    X_test = test_df[feature_names].values
    y_test = np.where(test_df[Config.TARGET_COLUMN].values == "Candidate_A", 1, 0)
    
    # Initialize comparator
    comparator = ModelComparator()
    
    # Note: In a real scenario, you would have multiple trained models saved
    # For now, we'll compare if the best_model exists
    models_dir = Config.MODELS_DIR
    if not (models_dir / "best_model.pkl").exists():
        logger.error("No trained models found. Please run training first.")
        return
    
    comparator.models["best_model"] = joblib.load(models_dir / "best_model.pkl")
    
    # Compare models
    df_comparison = comparator.compare_models(X_test, y_test)
    
    # Generate visualizations
    plots_dir = Config.BASE_DIR / "reports" / "figures"
    plots_dir.mkdir(parents=True, exist_ok=True)
    comparator.plot_comparison(df_comparison, plots_dir / "model_comparison.png")
    
    # Generate report
    report_path = Config.BASE_DIR / "reports" / "model_comparison.json"
    comparator.generate_comparison_report(df_comparison, report_path)
    
    logger.info("Model comparison completed successfully!")


if __name__ == "__main__":
    main()
