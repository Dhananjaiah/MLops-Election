"""
Unit tests for API service.
"""

import pytest
from fastapi.testclient import TestClient
from src.serving.api import app, ElectionFeatures


class TestAPI:
    """Test cases for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        # Endpoints can be a dict or string
        assert isinstance(data["endpoints"], (dict, str))
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "model_version" in data
        assert "timestamp" in data
    
    def test_predict_endpoint(self, client):
        """Test prediction endpoint."""
        # Sample prediction request
        request_data = {
            "population": 150000,
            "median_age": 42.5,
            "median_income": 55000,
            "education_rate": 0.85,
            "urban_ratio": 0.7,
            "prev_election_turnout": 0.68,
            "prev_winner_margin": 0.05,
            "voter_registration_rate": 0.82,
            "social_sentiment_score": 0.15,
            "candidate_a_favorability": 0.55,
            "candidate_b_favorability": 0.48,
            "poll_candidate_a": 0.48,
            "poll_candidate_b": 0.45,
            "undecided_rate": 0.07
        }
        
        response = client.post("/predict", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "predicted_winner" in data
        assert "confidence" in data
        assert "probabilities" in data
        assert "model_version" in data
        
        # Check predicted winner is valid
        assert data["predicted_winner"] in ["Candidate_A", "Candidate_B"]
        
        # Check confidence is between 0 and 1
        assert 0 <= data["confidence"] <= 1
        
        # Check probabilities sum to 1
        probs = data["probabilities"]
        assert "Candidate_A" in probs
        assert "Candidate_B" in probs
        prob_sum = probs["Candidate_A"] + probs["Candidate_B"]
        assert abs(prob_sum - 1.0) < 0.01
    
    def test_predict_invalid_data(self, client):
        """Test prediction endpoint with invalid data."""
        request_data = {
            "population": "invalid",  # Should be numeric
            "median_age": 42.5,
        }
        
        response = client.post("/predict", json=request_data)
        
        # Should return 422 Unprocessable Entity for validation error
        assert response.status_code == 422
    
    def test_model_info_endpoint(self, client):
        """Test model info endpoint."""
        response = client.get("/model/info")
        
        assert response.status_code == 200
        data = response.json()
        assert "model_version" in data
    
    def test_metrics_endpoint(self, client):
        """Test Prometheus metrics endpoint."""
        response = client.get("/metrics")
        
        assert response.status_code == 200
        # Prometheus metrics are in text format
        assert "text/plain" in response.headers["content-type"]


class TestElectionFeatures:
    """Test ElectionFeatures model."""
    
    def test_valid_features(self):
        """Test creating valid features."""
        features = ElectionFeatures(
            population=150000,
            median_age=42.5,
            median_income=55000,
            education_rate=0.85,
            urban_ratio=0.7,
            prev_election_turnout=0.68,
            prev_winner_margin=0.05,
            voter_registration_rate=0.82,
            social_sentiment_score=0.15,
            candidate_a_favorability=0.55,
            candidate_b_favorability=0.48,
            poll_candidate_a=0.48,
            poll_candidate_b=0.45,
            undecided_rate=0.07
        )
        
        assert features.population == 150000
        assert features.median_age == 42.5
        assert features.education_rate == 0.85
    
    def test_features_to_dict(self):
        """Test converting features to dict."""
        features = ElectionFeatures(
            population=150000,
            median_age=42.5,
            median_income=55000,
            education_rate=0.85,
            urban_ratio=0.7,
            prev_election_turnout=0.68,
            prev_winner_margin=0.05,
            voter_registration_rate=0.82,
            social_sentiment_score=0.15,
            candidate_a_favorability=0.55,
            candidate_b_favorability=0.48,
            poll_candidate_a=0.48,
            poll_candidate_b=0.45,
            undecided_rate=0.07
        )
        
        features_dict = features.model_dump()
        
        assert isinstance(features_dict, dict)
        assert "population" in features_dict
        assert "median_age" in features_dict
        assert len(features_dict) == 14  # All features


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
