"""
Metrics collection and monitoring.
"""

import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
from datetime import datetime
import json
from pathlib import Path

from src.utils.logger import get_logger
from src.utils.config import Config


logger = get_logger(__name__)


class MetricsCollector:
    """Collect and track model and system metrics."""
    
    def __init__(self, registry: CollectorRegistry = None):
        """
        Initialize metrics collector.
        
        Args:
            registry: Prometheus registry
        """
        self.registry = registry or CollectorRegistry()
        self.metrics = {}
        self._initialize_metrics()
    
    def _initialize_metrics(self):
        """Initialize Prometheus metrics."""
        # Model performance metrics
        self.metrics['model_accuracy'] = Gauge(
            'election_model_accuracy',
            'Current model accuracy',
            registry=self.registry
        )
        
        self.metrics['model_predictions_total'] = Counter(
            'election_predictions_total',
            'Total number of predictions',
            ['winner'],
            registry=self.registry
        )
        
        self.metrics['prediction_latency'] = Histogram(
            'election_prediction_latency_seconds',
            'Prediction latency in seconds',
            registry=self.registry
        )
        
        # Drift metrics
        self.metrics['drift_detected'] = Gauge(
            'election_drift_detected',
            'Whether drift is currently detected (1=yes, 0=no)',
            registry=self.registry
        )
        
        self.metrics['drift_share'] = Gauge(
            'election_drift_share',
            'Share of features with detected drift',
            registry=self.registry
        )
        
        # Data quality metrics
        self.metrics['data_quality_score'] = Gauge(
            'election_data_quality_score',
            'Overall data quality score (0-1)',
            registry=self.registry
        )
        
        self.metrics['missing_values_count'] = Gauge(
            'election_missing_values_total',
            'Total number of missing values in recent data',
            registry=self.registry
        )
        
        # System metrics
        self.metrics['model_version'] = Gauge(
            'election_model_version_info',
            'Current model version',
            registry=self.registry
        )
    
    def record_prediction(self, winner: str, latency: float):
        """
        Record a prediction event.
        
        Args:
            winner: Predicted winner
            latency: Prediction latency in seconds
        """
        self.metrics['model_predictions_total'].labels(winner=winner).inc()
        self.metrics['prediction_latency'].observe(latency)
    
    def update_model_accuracy(self, accuracy: float):
        """
        Update model accuracy metric.
        
        Args:
            accuracy: Current accuracy value
        """
        self.metrics['model_accuracy'].set(accuracy)
    
    def update_drift_metrics(self, drift_detected: bool, drift_share: float):
        """
        Update drift detection metrics.
        
        Args:
            drift_detected: Whether drift is detected
            drift_share: Share of drifted features
        """
        self.metrics['drift_detected'].set(1.0 if drift_detected else 0.0)
        self.metrics['drift_share'].set(drift_share)
    
    def update_data_quality(self, quality_score: float, missing_count: int):
        """
        Update data quality metrics.
        
        Args:
            quality_score: Overall quality score
            missing_count: Number of missing values
        """
        self.metrics['data_quality_score'].set(quality_score)
        self.metrics['missing_values_count'].set(missing_count)
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Get current values of all metrics.
        
        Returns:
            Dictionary of current metrics
        """
        # This is a simplified version; in production use Prometheus client API
        current_metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {}
        }
        
        # Note: Getting actual values from Prometheus metrics requires specific API calls
        # This is a placeholder structure
        
        return current_metrics
    
    def export_metrics(self, output_path: Path):
        """
        Export metrics to file.
        
        Args:
            output_path: Path to save metrics
        """
        metrics = self.get_current_metrics()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info(f"Metrics exported to {output_path}")


class PerformanceTracker:
    """Track model performance over time."""
    
    def __init__(self):
        """Initialize performance tracker."""
        self.performance_history = []
    
    def record_performance(
        self,
        accuracy: float,
        precision: float,
        recall: float,
        f1_score: float,
        timestamp: str = None
    ):
        """
        Record performance metrics.
        
        Args:
            accuracy: Accuracy value
            precision: Precision value
            recall: Recall value
            f1_score: F1 score value
            timestamp: Timestamp (defaults to current time)
        """
        record = {
            "timestamp": timestamp or datetime.utcnow().isoformat(),
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        }
        
        self.performance_history.append(record)
        logger.info(f"Performance recorded: Accuracy={accuracy:.4f}, F1={f1_score:.4f}")
    
    def get_performance_trend(self) -> Dict[str, Any]:
        """
        Analyze performance trends.
        
        Returns:
            Performance trend analysis
        """
        if not self.performance_history:
            return {"status": "no_data"}
        
        import numpy as np
        
        accuracies = [r['accuracy'] for r in self.performance_history]
        
        trend = {
            "n_records": len(self.performance_history),
            "latest_accuracy": accuracies[-1],
            "mean_accuracy": np.mean(accuracies),
            "std_accuracy": np.std(accuracies),
            "min_accuracy": min(accuracies),
            "max_accuracy": max(accuracies),
            "trend": "improving" if len(accuracies) > 1 and accuracies[-1] > accuracies[0] else "stable"
        }
        
        return trend
    
    def save_history(self, output_path: Path):
        """
        Save performance history.
        
        Args:
            output_path: Path to save history
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.performance_history, f, indent=2)
        
        logger.info(f"Performance history saved to {output_path}")


def main():
    """Main metrics collection function."""
    logger.info("Metrics collection example...")
    
    # Initialize collector
    collector = MetricsCollector()
    
    # Simulate some metrics
    collector.update_model_accuracy(0.92)
    collector.update_drift_metrics(drift_detected=False, drift_share=0.05)
    collector.update_data_quality(quality_score=0.95, missing_count=12)
    
    # Export metrics
    output_path = Config.BASE_DIR / "reports" / "metrics.json"
    collector.export_metrics(output_path)
    
    # Initialize performance tracker
    tracker = PerformanceTracker()
    tracker.record_performance(
        accuracy=0.92,
        precision=0.91,
        recall=0.93,
        f1_score=0.92
    )
    
    # Save performance history
    history_path = Config.BASE_DIR / "reports" / "performance_history.json"
    tracker.save_history(history_path)
    
    logger.info("Metrics collection completed!")


if __name__ == "__main__":
    main()
