"""
Data Loading Module
===================

This module handles loading data from various sources (CSV, databases, etc.)
for the Customer Churn Prediction project.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def load_csv(filepath: str) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing the loaded data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        pd.errors.EmptyDataError: If the file is empty
    """
    logger.info(f"Loading data from {filepath}")
    
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    df = pd.read_csv(filepath)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    
    return df


def load_train_test_split(
    data_dir: str,
    train_file: str = "train.csv",
    test_file: str = "test.csv"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load pre-split train and test datasets.
    
    Args:
        data_dir: Directory containing the data files
        train_file: Name of the training file
        test_file: Name of the test file
        
    Returns:
        Tuple of (train_df, test_df)
    """
    data_path = Path(data_dir)
    
    train_df = load_csv(str(data_path / train_file))
    test_df = load_csv(str(data_path / test_file))
    
    return train_df, test_df


def validate_data(df: pd.DataFrame, required_columns: Optional[list] = None) -> bool:
    """
    Validate that the dataframe contains required columns and has valid data.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If validation fails
    """
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    
    logger.info("Data validation passed")
    return True


# Sample data generator for testing/demos
def generate_sample_data(n_samples: int = 1000) -> pd.DataFrame:
    """
    Generate synthetic customer churn data for demos and testing.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        DataFrame with synthetic churn data
    """
    import numpy as np
    
    np.random.seed(42)
    
    data = {
        "customer_id": range(1, n_samples + 1),
        "tenure": np.random.randint(1, 72, n_samples),
        "monthly_charges": np.random.uniform(20, 100, n_samples),
        "total_charges": np.random.uniform(100, 5000, n_samples),
        "contract_type": np.random.choice(["month-to-month", "one_year", "two_year"], n_samples),
        "payment_method": np.random.choice(["credit_card", "bank_transfer", "electronic_check"], n_samples),
        "internet_service": np.random.choice(["dsl", "fiber_optic", "no"], n_samples),
        "tech_support": np.random.choice(["yes", "no"], n_samples),
        "online_security": np.random.choice(["yes", "no"], n_samples),
        "churn": np.random.choice([0, 1], n_samples, p=[0.73, 0.27]),
    }
    
    df = pd.DataFrame(data)
    logger.info(f"Generated {n_samples} synthetic samples")
    
    return df
