"""
Tests for Models Module
=======================
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from churn_mlops.models import ChurnModel, train_model
from churn_mlops.data import generate_sample_data


@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    df = generate_sample_data(n_samples=500)
    # Use only numeric columns for simplicity
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    X = df[[c for c in numeric_cols if c not in ['churn', 'customer_id']]]
    y = df['churn']
    return X, y


@pytest.fixture
def train_test_data(sample_data):
    """Split sample data into train and test sets."""
    from sklearn.model_selection import train_test_split
    X, y = sample_data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test


class TestChurnModel:
    """Tests for the ChurnModel class."""
    
    def test_init_random_forest(self):
        """Test initializing a random forest model."""
        model = ChurnModel(model_type="random_forest")
        assert model.model_type == "random_forest"
        assert not model._is_fitted
    
    def test_init_logistic_regression(self):
        """Test initializing a logistic regression model."""
        model = ChurnModel(model_type="logistic_regression")
        assert model.model_type == "logistic_regression"
    
    def test_init_invalid_model_type(self):
        """Test that invalid model type raises error."""
        with pytest.raises(ValueError, match="Unknown model type"):
            ChurnModel(model_type="invalid_model")
    
    def test_fit(self, sample_data):
        """Test model fitting."""
        X, y = sample_data
        model = ChurnModel(model_type="random_forest")
        model.fit(X, y)
        assert model._is_fitted
    
    def test_predict_before_fit(self, sample_data):
        """Test that predict before fit raises error."""
        X, y = sample_data
        model = ChurnModel(model_type="random_forest")
        with pytest.raises(ValueError, match="must be fitted"):
            model.predict(X)
    
    def test_predict(self, train_test_data):
        """Test model predictions."""
        X_train, X_test, y_train, y_test = train_test_data
        model = ChurnModel(model_type="random_forest")
        model.fit(X_train, y_train)
        
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)
        assert all(p in [0, 1] for p in predictions)
    
    def test_predict_proba(self, train_test_data):
        """Test probability predictions."""
        X_train, X_test, y_train, y_test = train_test_data
        model = ChurnModel(model_type="random_forest")
        model.fit(X_train, y_train)
        
        probas = model.predict_proba(X_test)
        assert probas.shape == (len(X_test), 2)
        assert np.allclose(probas.sum(axis=1), 1.0)
    
    def test_evaluate(self, train_test_data):
        """Test model evaluation."""
        X_train, X_test, y_train, y_test = train_test_data
        model = ChurnModel(model_type="random_forest")
        model.fit(X_train, y_train)
        
        metrics = model.evaluate(X_test, y_test)
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics
        assert "roc_auc" in metrics
        
        # All metrics should be between 0 and 1
        for metric, value in metrics.items():
            assert 0 <= value <= 1
    
    def test_save_and_load(self, train_test_data):
        """Test model saving and loading."""
        X_train, X_test, y_train, y_test = train_test_data
        model = ChurnModel(model_type="random_forest")
        model.fit(X_train, y_train)
        
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as f:
            temp_path = f.name
        
        try:
            # Save
            model.save(temp_path)
            assert os.path.exists(temp_path)
            
            # Load
            loaded_model = ChurnModel.load(temp_path)
            assert loaded_model._is_fitted
            assert loaded_model.model_type == "random_forest"
            
            # Predictions should be identical
            original_preds = model.predict(X_test)
            loaded_preds = loaded_model.predict(X_test)
            np.testing.assert_array_equal(original_preds, loaded_preds)
        finally:
            os.unlink(temp_path)


class TestTrainModel:
    """Tests for the train_model function."""
    
    def test_train_model_default(self, train_test_data):
        """Test training with default parameters."""
        X_train, X_test, y_train, y_test = train_test_data
        model, metrics = train_model(X_train, y_train, X_test, y_test)
        
        assert model._is_fitted
        assert isinstance(metrics, dict)
        assert metrics["accuracy"] > 0.5  # Should be better than random
    
    def test_train_model_logistic_regression(self, train_test_data):
        """Test training with logistic regression."""
        X_train, X_test, y_train, y_test = train_test_data
        model, metrics = train_model(
            X_train, y_train, X_test, y_test,
            model_type="logistic_regression"
        )
        
        assert model.model_type == "logistic_regression"
        assert model._is_fitted
