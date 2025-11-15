"""
Unit tests for data generation module.
"""

import pytest
import pandas as pd
from src.data.make_dataset import generate_synthetic_election_data, save_dataset
from src.utils.config import Config
import tempfile
from pathlib import Path


class TestDataGeneration:
    """Test cases for data generation."""
    
    def test_generate_synthetic_data_shape(self):
        """Test that generated data has correct shape."""
        n_samples = 100
        df = generate_synthetic_election_data(n_samples=n_samples)
        
        assert df.shape[0] == n_samples
        assert df.shape[1] > 10  # Should have multiple columns
    
    def test_generate_synthetic_data_columns(self):
        """Test that generated data has required columns."""
        df = generate_synthetic_election_data(n_samples=100)
        
        required_columns = Config.ALL_FEATURES + [Config.TARGET_COLUMN]
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_generate_synthetic_data_target_values(self):
        """Test that target column has valid values."""
        df = generate_synthetic_election_data(n_samples=100)
        
        valid_targets = ["Candidate_A", "Candidate_B"]
        assert df[Config.TARGET_COLUMN].isin(valid_targets).all()
    
    def test_generate_synthetic_data_no_missing(self):
        """Test that generated data has no missing values."""
        df = generate_synthetic_election_data(n_samples=100)
        
        assert df.isnull().sum().sum() == 0
    
    def test_save_and_load_dataset(self):
        """Test saving and loading dataset."""
        df = generate_synthetic_election_data(n_samples=50)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test_data.csv"
            save_dataset(df, file_path)
            
            # Check file exists
            assert file_path.exists()
            
            # Load and verify
            df_loaded = pd.read_csv(file_path)
            assert df_loaded.shape == df.shape
            assert list(df_loaded.columns) == list(df.columns)
    
    def test_generate_synthetic_data_random_state(self):
        """Test that random state produces reproducible results."""
        df1 = generate_synthetic_election_data(n_samples=100, random_state=42)
        df2 = generate_synthetic_election_data(n_samples=100, random_state=42)
        
        pd.testing.assert_frame_equal(df1, df2)
    
    def test_generate_synthetic_data_different_sizes(self):
        """Test generating data with different sample sizes."""
        sizes = [10, 50, 100, 500]
        
        for size in sizes:
            df = generate_synthetic_election_data(n_samples=size)
            assert len(df) == size


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
