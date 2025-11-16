"""
Unit tests for preprocessing module.
"""

import pytest
import pandas as pd
import numpy as np
from src.data.preprocess import ElectionDataPreprocessor, split_data
from src.utils.config import Config


class TestPreprocessing:
    """Test cases for data preprocessing."""
    
    def test_preprocessor_initialization(self):
        """Test preprocessor initialization."""
        preprocessor = ElectionDataPreprocessor()
        
        assert preprocessor.scaler is not None
        assert len(preprocessor.feature_columns) > 0
        assert preprocessor.target_column == Config.TARGET_COLUMN
    
    def test_clean_data_removes_duplicates(self, sample_data):
        """Test that clean_data removes duplicates."""
        # Add duplicate row
        df_with_dup = pd.concat([sample_data, sample_data.iloc[:1]], ignore_index=True)
        
        preprocessor = ElectionDataPreprocessor()
        df_clean = preprocessor.clean_data(df_with_dup)
        
        assert len(df_clean) < len(df_with_dup)
    
    def test_validate_data_success(self, sample_data):
        """Test data validation with valid data."""
        preprocessor = ElectionDataPreprocessor()
        
        is_valid = preprocessor.validate_data(sample_data)
        assert is_valid is True
    
    def test_validate_data_missing_columns(self, sample_data):
        """Test data validation fails with missing columns."""
        df_invalid = sample_data.drop(columns=[Config.TARGET_COLUMN])
        
        preprocessor = ElectionDataPreprocessor()
        is_valid = preprocessor.validate_data(df_invalid)
        
        assert is_valid is False
    
    def test_validate_data_invalid_target(self, sample_data):
        """Test data validation fails with invalid target values."""
        df_invalid = sample_data.copy()
        df_invalid.loc[0, Config.TARGET_COLUMN] = "Invalid_Candidate"
        
        preprocessor = ElectionDataPreprocessor()
        is_valid = preprocessor.validate_data(df_invalid)
        
        assert is_valid is False
    
    def test_scale_features(self, sample_data):
        """Test feature scaling."""
        preprocessor = ElectionDataPreprocessor()
        df_scaled = preprocessor.scale_features(sample_data, fit=True)
        
        # Check that scaled features have mean close to 0 and std close to 1
        for col in preprocessor.feature_columns:
            mean = df_scaled[col].mean()
            std = df_scaled[col].std()
            assert abs(mean) < 0.1, f"Feature {col} mean not close to 0: {mean}"
            assert abs(std - 1.0) < 0.1, f"Feature {col} std not close to 1: {std}"
    
    def test_preprocess_pipeline(self, sample_data):
        """Test complete preprocessing pipeline."""
        preprocessor = ElectionDataPreprocessor()
        df_processed = preprocessor.preprocess(sample_data, fit_scaler=True)
        
        # Check no missing values
        assert df_processed.isnull().sum().sum() == 0
        
        # Check shape preserved
        assert len(df_processed) <= len(sample_data)  # May remove outliers
        
        # Check all columns present
        for col in Config.ALL_FEATURES + [Config.TARGET_COLUMN]:
            assert col in df_processed.columns
    
    def test_split_data(self, sample_data):
        """Test data splitting."""
        train_df, test_df = split_data(sample_data, test_size=0.2, random_state=42)
        
        # Check sizes
        total_size = len(sample_data)
        expected_test_size = int(total_size * 0.2)
        
        assert len(test_df) == expected_test_size
        assert len(train_df) == total_size - expected_test_size
        
        # Check no overlap
        train_indices = set(train_df.index)
        test_indices = set(test_df.index)
        assert len(train_indices.intersection(test_indices)) == 0
    
    def test_split_data_stratified(self, sample_data):
        """Test that data splitting maintains target distribution."""
        train_df, test_df = split_data(sample_data, test_size=0.2, random_state=42)
        
        # Check target distribution similar in train and test
        train_dist = train_df[Config.TARGET_COLUMN].value_counts(normalize=True)
        test_dist = test_df[Config.TARGET_COLUMN].value_counts(normalize=True)
        original_dist = sample_data[Config.TARGET_COLUMN].value_counts(normalize=True)
        
        for candidate in train_dist.index:
            assert abs(train_dist[candidate] - original_dist[candidate]) < 0.1
            assert abs(test_dist[candidate] - original_dist[candidate]) < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
