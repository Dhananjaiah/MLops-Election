"""
Unit tests for feature engineering module.
"""

import pytest
import pandas as pd
import numpy as np
from src.data.features import ElectionFeatureEngineering
from src.utils.config import Config


class TestFeatureEngineering:
    """Test cases for feature engineering."""
    
    def test_feature_engineer_initialization(self):
        """Test feature engineer initialization."""
        engineer = ElectionFeatureEngineering()
        
        assert engineer.engineered_features == []
    
    def test_create_turnout_features(self, sample_data):
        """Test turnout feature creation."""
        engineer = ElectionFeatureEngineering()
        df_features = engineer.create_turnout_features(sample_data)
        
        # Check new features added
        assert 'turnout_trend' in df_features.columns
        assert 'expected_turnout' in df_features.columns
        assert 'turnout_surprise' in df_features.columns
        
        # Check no NaN values
        assert df_features[['turnout_trend', 'expected_turnout', 'turnout_surprise']].isnull().sum().sum() == 0
    
    def test_create_demographic_features(self, sample_data):
        """Test demographic feature creation."""
        engineer = ElectionFeatureEngineering()
        df_features = engineer.create_demographic_features(sample_data)
        
        # Check new features added
        assert 'demographic_score' in df_features.columns
        assert 'age_income_interaction' in df_features.columns
        assert 'urban_education' in df_features.columns
        assert 'population_density' in df_features.columns
        
        # Check no NaN values
        new_features = ['demographic_score', 'age_income_interaction', 'urban_education', 'population_density']
        assert df_features[new_features].isnull().sum().sum() == 0
    
    def test_create_polling_features(self, sample_data):
        """Test polling feature creation."""
        engineer = ElectionFeatureEngineering()
        df_features = engineer.create_polling_features(sample_data)
        
        # Check new features added
        assert 'poll_margin' in df_features.columns
        assert 'poll_confidence' in df_features.columns
        assert 'favorability_diff' in df_features.columns
        
        # Check poll margin calculation
        expected_margin = sample_data['poll_candidate_a'] - sample_data['poll_candidate_b']
        np.testing.assert_array_almost_equal(df_features['poll_margin'], expected_margin)
    
    def test_create_momentum_features(self, sample_data):
        """Test momentum feature creation."""
        engineer = ElectionFeatureEngineering()
        # Need to create poll_margin first as it's used in momentum calculation
        df_with_poll = engineer.create_polling_features(sample_data)
        df_features = engineer.create_momentum_features(df_with_poll)
        
        # Check new features added
        assert 'incumbent_advantage' in df_features.columns
        assert 'challenger_momentum' in df_features.columns
        assert 'momentum_score' in df_features.columns
    
    def test_create_interaction_features(self, sample_data):
        """Test interaction feature creation."""
        engineer = ElectionFeatureEngineering()
        df_features = engineer.create_interaction_features(sample_data)
        
        # Check new features added
        assert 'poll_turnout' in df_features.columns
        assert 'sentiment_favorability' in df_features.columns
        assert 'urban_income' in df_features.columns
    
    def test_engineer_features_complete(self, sample_data):
        """Test complete feature engineering pipeline."""
        engineer = ElectionFeatureEngineering()
        df_features = engineer.engineer_features(sample_data)
        
        # Check that engineered features were created
        assert len(engineer.engineered_features) > 0
        
        # Check all engineered features are in dataframe
        for feature in engineer.engineered_features:
            assert feature in df_features.columns, f"Missing feature: {feature}"
        
        # Check no NaN values in engineered features
        nan_count = df_features[engineer.engineered_features].isnull().sum().sum()
        assert nan_count == 0, f"Found {nan_count} NaN values in engineered features"
    
    def test_get_all_feature_names(self, sample_data):
        """Test getting all feature names."""
        engineer = ElectionFeatureEngineering()
        engineer.engineer_features(sample_data)
        
        all_features = engineer.get_all_feature_names()
        
        # Check includes original features
        for feature in Config.ALL_FEATURES:
            assert feature in all_features
        
        # Check includes engineered features
        for feature in engineer.engineered_features:
            assert feature in all_features
    
    def test_feature_engineering_reproducibility(self, sample_data):
        """Test that feature engineering is reproducible."""
        engineer1 = ElectionFeatureEngineering()
        engineer2 = ElectionFeatureEngineering()
        
        df_features1 = engineer1.engineer_features(sample_data.copy())
        df_features2 = engineer2.engineer_features(sample_data.copy())
        
        # Check same features created
        assert engineer1.engineered_features == engineer2.engineered_features
        
        # Check same values
        for feature in engineer1.engineered_features:
            np.testing.assert_array_almost_equal(
                df_features1[feature].values,
                df_features2[feature].values
            )
    
    def test_feature_engineering_preserves_shape(self, sample_data):
        """Test that feature engineering preserves number of rows."""
        engineer = ElectionFeatureEngineering()
        df_features = engineer.engineer_features(sample_data)
        
        assert len(df_features) == len(sample_data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
