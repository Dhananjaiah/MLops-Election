"""
Tests for Data Loading Module
=============================
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

from churn_mlops.data import (
    load_csv,
    validate_data,
    generate_sample_data,
)


class TestLoadCSV:
    """Tests for the load_csv function."""
    
    def test_load_csv_success(self):
        """Test loading a valid CSV file."""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("col1,col2,col3\n")
            f.write("1,2,3\n")
            f.write("4,5,6\n")
            temp_path = f.name
        
        try:
            df = load_csv(temp_path)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert list(df.columns) == ["col1", "col2", "col3"]
        finally:
            os.unlink(temp_path)
    
    def test_load_csv_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(FileNotFoundError):
            load_csv("/nonexistent/path/data.csv")


class TestValidateData:
    """Tests for the validate_data function."""
    
    def test_validate_data_success(self):
        """Test validation passes for valid data."""
        df = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": [4, 5, 6],
        })
        result = validate_data(df, required_columns=["col1", "col2"])
        assert result is True
    
    def test_validate_data_empty_dataframe(self):
        """Test validation fails for empty DataFrame."""
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="empty"):
            validate_data(df)
    
    def test_validate_data_missing_columns(self):
        """Test validation fails when required columns are missing."""
        df = pd.DataFrame({"col1": [1, 2, 3]})
        with pytest.raises(ValueError, match="Missing required columns"):
            validate_data(df, required_columns=["col1", "col2", "col3"])


class TestGenerateSampleData:
    """Tests for the generate_sample_data function."""
    
    def test_generate_sample_data_default(self):
        """Test generating sample data with default parameters."""
        df = generate_sample_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1000  # Default n_samples
        assert "customer_id" in df.columns
        assert "churn" in df.columns
    
    def test_generate_sample_data_custom_size(self):
        """Test generating sample data with custom size."""
        df = generate_sample_data(n_samples=500)
        assert len(df) == 500
    
    def test_generate_sample_data_columns(self):
        """Test that generated data has expected columns."""
        df = generate_sample_data(n_samples=100)
        expected_columns = [
            "customer_id", "tenure", "monthly_charges", "total_charges",
            "contract_type", "payment_method", "internet_service",
            "tech_support", "online_security", "churn"
        ]
        for col in expected_columns:
            assert col in df.columns
    
    def test_generate_sample_data_reproducible(self):
        """Test that generated data is reproducible (uses fixed seed)."""
        df1 = generate_sample_data(n_samples=100)
        df2 = generate_sample_data(n_samples=100)
        pd.testing.assert_frame_equal(df1, df2)
