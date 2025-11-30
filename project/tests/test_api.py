"""
Tests for API Endpoints
=======================
"""

import pytest
from pathlib import Path
import tempfile
import os

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Test imports
from fastapi.testclient import TestClient


class TestAPIBasic:
    """Basic API tests that don't require a trained model."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        from churn_mlops.serving.app import app
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs" in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
    
    def test_docs_available(self, client):
        """Test that OpenAPI docs are available."""
        response = client.get("/docs")
        assert response.status_code == 200


class TestAPIPredictions:
    """Tests for prediction endpoints (require trained model)."""
    
    @pytest.fixture
    def trained_model(self, tmp_path):
        """Create and save a trained model for testing."""
        from churn_mlops.data import generate_sample_data
        from churn_mlops.models import ChurnModel
        import numpy as np
        
        # Generate data
        df = generate_sample_data(n_samples=500)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        X = df[[c for c in numeric_cols if c not in ['churn', 'customer_id']]]
        y = df['churn']
        
        # Train and save model
        model = ChurnModel(model_type="random_forest")
        model.fit(X, y)
        
        model_path = tmp_path / "test_model.pkl"
        model.save(str(model_path))
        
        return str(model_path)
    
    @pytest.fixture
    def client_with_model(self, trained_model):
        """Create test client with trained model."""
        # Set model path environment variable BEFORE importing the app
        os.environ["MODEL_PATH"] = trained_model
        
        # Need to reimport the app module to pick up the new MODEL_PATH
        import importlib
        import churn_mlops.serving.app as app_module
        
        # Reset global predictor and reload the module
        app_module._predictor = None
        importlib.reload(app_module)
        
        return TestClient(app_module.app)
    
    def test_predict_single(self, client_with_model):
        """Test single prediction endpoint."""
        payload = {
            "tenure": 24,
            "monthly_charges": 65.50,
            "total_charges": 1572.00,
        }
        
        response = client_with_model.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert "prediction" in data
        assert "will_churn" in data
        assert "churn_probability" in data
        assert "confidence" in data
        
        assert data["prediction"] in [0, 1]
        assert 0 <= data["churn_probability"] <= 1
        assert 0 <= data["confidence"] <= 1
    
    def test_predict_batch(self, client_with_model):
        """Test batch prediction endpoint."""
        payload = {
            "customers": [
                {"tenure": 12, "monthly_charges": 50.0, "total_charges": 600.0},
                {"tenure": 36, "monthly_charges": 80.0, "total_charges": 2880.0},
            ]
        }
        
        response = client_with_model.post("/predict/batch", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert "predictions" in data
        assert "total_customers" in data
        assert data["total_customers"] == 2
        assert len(data["predictions"]) == 2
