"""
Data and prediction drift monitoring using Evidently.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
from datetime import datetime
import json

try:
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset, DataQualityPreset
    from evidently.metrics import DatasetDriftMetric, ColumnDriftMetric
    EVIDENTLY_AVAILABLE = True
except ImportError:
    EVIDENTLY_AVAILABLE = False

from src.utils.logger import get_logger
from src.utils.config import Config


logger = get_logger(__name__)


class DriftMonitor:
    """Monitor data and prediction drift."""
    
    def __init__(self, drift_threshold: float = None):
        """
        Initialize drift monitor.
        
        Args:
            drift_threshold: Threshold for drift detection
        """
        self.drift_threshold = drift_threshold or Config.DRIFT_THRESHOLD
        self.drift_detected = False
        self.drift_report = {}
        
        if not EVIDENTLY_AVAILABLE:
            logger.warning("Evidently not installed. Install with: pip install evidently")
    
    def detect_data_drift(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        feature_columns: list
    ) -> Dict[str, Any]:
        """
        Detect data drift between reference and current data.
        
        Args:
            reference_data: Reference dataset (training data)
            current_data: Current dataset (production data)
            feature_columns: List of feature columns to monitor
        
        Returns:
            Drift detection report
        """
        logger.info("Detecting data drift...")
        
        if not EVIDENTLY_AVAILABLE:
            logger.warning("Evidently not available. Using simple statistical drift detection.")
            return self._simple_drift_detection(reference_data, current_data, feature_columns)
        
        try:
            # Create Evidently report
            report = Report(metrics=[
                DataDriftPreset(),
                DataQualityPreset()
            ])
            
            # Run report
            report.run(
                reference_data=reference_data[feature_columns],
                current_data=current_data[feature_columns]
            )
            
            # Extract results
            report_dict = report.as_dict()
            
            # Check for drift
            metrics = report_dict.get('metrics', [])
            drift_metrics = [m for m in metrics if 'drift' in str(m.get('metric', '')).lower()]
            
            n_drifted = sum(1 for m in drift_metrics if m.get('result', {}).get('drift_detected', False))
            drift_share = n_drifted / len(feature_columns) if feature_columns else 0
            
            self.drift_detected = drift_share > self.drift_threshold
            
            from datetime import datetime, timezone
            
            self.drift_report = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "drift_detected": self.drift_detected,
                "drift_share": drift_share,
                "n_drifted_features": n_drifted,
                "n_features": len(feature_columns),
                "threshold": self.drift_threshold
            }
            
            logger.info(f"Drift detection completed. Drift detected: {self.drift_detected}")
            logger.info(f"Drifted features: {n_drifted}/{len(feature_columns)} ({drift_share:.2%})")
            
            return self.drift_report
            
        except Exception as e:
            logger.error(f"Error in Evidently drift detection: {e}")
            return self._simple_drift_detection(reference_data, current_data, feature_columns)
    
    def _simple_drift_detection(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        feature_columns: list
    ) -> Dict[str, Any]:
        """
        Simple statistical drift detection using KS test.
        
        Args:
            reference_data: Reference dataset
            current_data: Current dataset
            feature_columns: List of features to check
        
        Returns:
            Drift report
        """
        from scipy.stats import ks_2samp
        
        drifted_features = []
        drift_scores = {}
        
        for col in feature_columns:
            if col not in reference_data.columns or col not in current_data.columns:
                continue
            
            # KS test
            statistic, p_value = ks_2samp(
                reference_data[col].dropna(),
                current_data[col].dropna()
            )
            
            drift_scores[col] = {
                "statistic": float(statistic),
                "p_value": float(p_value)
            }
            
            # Drift detected if p-value < 0.05
            if p_value < 0.05:
                drifted_features.append(col)
        
        drift_share = len(drifted_features) / len(feature_columns) if feature_columns else 0
        self.drift_detected = drift_share > self.drift_threshold
        
        from datetime import datetime, timezone
        
        self.drift_report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "drift_detected": self.drift_detected,
            "drift_share": drift_share,
            "n_drifted_features": len(drifted_features),
            "n_features": len(feature_columns),
            "drifted_features": drifted_features,
            "drift_scores": drift_scores,
            "threshold": self.drift_threshold,
            "method": "ks_test"
        }
        
        logger.info(f"Simple drift detection completed. Drift detected: {self.drift_detected}")
        
        return self.drift_report
    
    def detect_prediction_drift(
        self,
        reference_predictions: np.ndarray,
        current_predictions: np.ndarray
    ) -> Dict[str, Any]:
        """
        Detect drift in model predictions.
        
        Args:
            reference_predictions: Reference predictions
            current_predictions: Current predictions
        
        Returns:
            Prediction drift report
        """
        logger.info("Detecting prediction drift...")
        
        from scipy.stats import ks_2samp, chisquare
        from datetime import datetime, timezone
        
        # Distribution comparison
        statistic, p_value = ks_2samp(reference_predictions, current_predictions)
        
        # Check class distribution shift (if binary)
        ref_dist = pd.Series(reference_predictions).value_counts(normalize=True)
        curr_dist = pd.Series(current_predictions).value_counts(normalize=True)
        
        prediction_drift_report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ks_statistic": float(statistic),
            "ks_p_value": float(p_value),
            "drift_detected": p_value < 0.05,
            "reference_distribution": ref_dist.to_dict(),
            "current_distribution": curr_dist.to_dict()
        }
        
        logger.info(f"Prediction drift detected: {prediction_drift_report['drift_detected']}")
        
        return prediction_drift_report
    
    def generate_html_report(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        feature_columns: list,
        output_path: Path
    ):
        """
        Generate HTML drift report.
        
        Args:
            reference_data: Reference dataset
            current_data: Current dataset
            feature_columns: Feature columns
            output_path: Path to save HTML report
        """
        if not EVIDENTLY_AVAILABLE:
            logger.warning("Evidently not available. Cannot generate HTML report.")
            return
        
        try:
            logger.info("Generating HTML drift report...")
            
            report = Report(metrics=[
                DataDriftPreset(),
                DataQualityPreset()
            ])
            
            report.run(
                reference_data=reference_data[feature_columns],
                current_data=current_data[feature_columns]
            )
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            report.save_html(str(output_path))
            
            logger.info(f"HTML report saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
    
    def save_drift_report(self, output_path: Path):
        """
        Save drift report to JSON file.
        
        Args:
            output_path: Path to save the report
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.drift_report, f, indent=2)
        
        logger.info(f"Drift report saved to {output_path}")
    
    def should_retrain(self) -> bool:
        """
        Determine if model should be retrained based on drift.
        
        Returns:
            True if retraining is recommended
        """
        return self.drift_detected


def main():
    """Main drift monitoring function."""
    logger.info("Starting drift monitoring...")
    
    # Load reference data (training data)
    train_path = Config.DATA_DIR / "features" / "train_features.csv"
    
    if not train_path.exists():
        logger.error("Training data not found. Please run feature engineering first.")
        return
    
    reference_data = pd.read_csv(train_path)
    logger.info(f"Loaded reference data: {reference_data.shape}")
    
    # Simulate current data (in production, this would be recent data)
    # For demo, we'll use validation data
    current_path = Config.DATA_DIR / "raw" / "election_data_validation.csv"
    
    if not current_path.exists():
        logger.info("Generating current data for drift monitoring...")
        from src.data.make_dataset import generate_synthetic_election_data, save_dataset
        current_data_raw = generate_synthetic_election_data(n_samples=1000, random_state=456)
        save_dataset(current_data_raw, current_path)
    else:
        current_data_raw = pd.read_csv(current_path)
    
    # Preprocess current data
    from src.data.preprocess import ElectionDataPreprocessor
    from src.data.features import ElectionFeatureEngineering
    
    preprocessor = ElectionDataPreprocessor()
    scaler_path = Config.MODELS_DIR / "scaler.pkl"
    if scaler_path.exists():
        preprocessor.load_scaler(scaler_path)
    
    current_data_processed = preprocessor.preprocess(current_data_raw, fit_scaler=False)
    
    feature_engineer = ElectionFeatureEngineering()
    current_data = feature_engineer.engineer_features(current_data_processed)
    
    logger.info(f"Loaded current data: {current_data.shape}")
    
    # Get feature columns
    feature_columns = feature_engineer.get_all_feature_names()
    
    # Initialize drift monitor
    monitor = DriftMonitor()
    
    # Detect data drift
    drift_report = monitor.detect_data_drift(
        reference_data,
        current_data,
        feature_columns
    )
    
    # Save drift report
    report_path = Config.BASE_DIR / "reports" / "drift_report.json"
    monitor.save_drift_report(report_path)
    
    # Generate HTML report
    html_path = Config.BASE_DIR / "reports" / "drift_report.html"
    monitor.generate_html_report(
        reference_data,
        current_data,
        feature_columns,
        html_path
    )
    
    # Check if retraining is needed
    if monitor.should_retrain():
        logger.warning("⚠️  DRIFT DETECTED! Model retraining recommended.")
    else:
        logger.info("✓ No significant drift detected. Model is stable.")
    
    logger.info("Drift monitoring completed successfully!")


if __name__ == "__main__":
    main()
