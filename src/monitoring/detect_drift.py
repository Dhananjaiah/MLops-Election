"""
Detect drift and trigger alerts.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any
import json
from datetime import datetime

from src.monitoring.drift_monitoring import DriftMonitor
from src.utils.logger import get_logger
from src.utils.config import Config


logger = get_logger(__name__)


class DriftDetector:
    """High-level drift detection orchestrator."""
    
    def __init__(self):
        """Initialize drift detector."""
        self.monitor = DriftMonitor()
        self.alerts = []
    
    def check_drift(
        self,
        reference_data_path: Path,
        current_data_path: Path,
        feature_columns: list
    ) -> Dict[str, Any]:
        """
        Check for drift and generate alerts.
        
        Args:
            reference_data_path: Path to reference data
            current_data_path: Path to current data
            feature_columns: List of features to monitor
        
        Returns:
            Drift detection results with alerts
        """
        logger.info("Checking for drift...")
        
        # Load data
        reference_data = pd.read_csv(reference_data_path)
        current_data = pd.read_csv(current_data_path)
        
        # Detect drift
        drift_report = self.monitor.detect_data_drift(
            reference_data,
            current_data,
            feature_columns
        )
        
        # Generate alerts if drift detected
        if drift_report['drift_detected']:
            alert = self.create_alert(drift_report)
            self.alerts.append(alert)
            logger.warning(f"ALERT: {alert['message']}")
        
        return {
            "drift_report": drift_report,
            "alerts": self.alerts,
            "action_required": drift_report['drift_detected']
        }
    
    def create_alert(self, drift_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an alert for drift detection.
        
        Args:
            drift_report: Drift detection report
        
        Returns:
            Alert dictionary
        """
        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "severity": "high" if drift_report['drift_share'] > 0.3 else "medium",
            "type": "data_drift",
            "message": f"Data drift detected! {drift_report['n_drifted_features']} out of {drift_report['n_features']} features have drifted.",
            "details": drift_report,
            "action": "Model retraining recommended"
        }
        
        return alert
    
    def save_alerts(self, output_path: Path):
        """
        Save alerts to file.
        
        Args:
            output_path: Path to save alerts
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.alerts, f, indent=2)
        
        logger.info(f"Alerts saved to {output_path}")
    
    def export_metrics_for_prometheus(self) -> Dict[str, float]:
        """
        Export drift metrics for Prometheus.
        
        Returns:
            Dictionary of metrics
        """
        if not self.monitor.drift_report:
            return {}
        
        metrics = {
            "drift_detected": 1.0 if self.monitor.drift_detected else 0.0,
            "drift_share": self.monitor.drift_report.get('drift_share', 0.0),
            "n_drifted_features": float(self.monitor.drift_report.get('n_drifted_features', 0)),
        }
        
        return metrics


def main():
    """Main drift detection function."""
    logger.info("Starting drift detection...")
    
    # Initialize detector
    detector = DriftDetector()
    
    # Define paths
    reference_path = Config.DATA_DIR / "features" / "train_features.csv"
    current_path = Config.DATA_DIR / "features" / "test_features.csv"  # In production, use recent data
    
    if not reference_path.exists() or not current_path.exists():
        logger.error("Required data files not found.")
        return
    
    # Get feature names
    from src.data.features import ElectionFeatureEngineering
    feature_engineer = ElectionFeatureEngineering()
    feature_engineer.engineer_features(pd.DataFrame())
    feature_columns = feature_engineer.get_all_feature_names()
    
    # Check for drift
    results = detector.check_drift(
        reference_path,
        current_path,
        feature_columns
    )
    
    # Save alerts
    if results['alerts']:
        alerts_path = Config.BASE_DIR / "reports" / "drift_alerts.json"
        detector.save_alerts(alerts_path)
    
    # Export Prometheus metrics
    metrics = detector.export_metrics_for_prometheus()
    logger.info(f"Prometheus metrics: {metrics}")
    
    # Save metrics for Prometheus scraping
    metrics_path = Config.BASE_DIR / "reports" / "drift_metrics.json"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    logger.info("Drift detection completed!")


if __name__ == "__main__":
    main()
