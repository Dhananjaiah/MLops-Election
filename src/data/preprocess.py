"""
Data preprocessing for election prediction.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

from src.utils.logger import get_logger
from src.utils.config import Config


logger = get_logger(__name__)


class ElectionDataPreprocessor:
    """Preprocess election data for modeling."""
    
    def __init__(self):
        """Initialize preprocessor."""
        self.scaler = StandardScaler()
        self.feature_columns = Config.ALL_FEATURES
        self.target_column = Config.TARGET_COLUMN
        
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the raw election data.
        
        Args:
            df: Raw DataFrame
        
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning election data...")
        df_clean = df.copy()
        
        # Remove duplicates
        initial_rows = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        logger.info(f"Removed {initial_rows - len(df_clean)} duplicate rows")
        
        # Handle missing values
        missing_counts = df_clean[self.feature_columns].isnull().sum()
        if missing_counts.sum() > 0:
            logger.warning(f"Missing values found:\n{missing_counts[missing_counts > 0]}")
            # Fill missing values with median for numeric columns
            for col in self.feature_columns:
                if df_clean[col].isnull().sum() > 0:
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
        
        # Remove outliers using IQR method
        for col in self.feature_columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            outliers = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).sum()
            if outliers > 0:
                logger.info(f"Removing {outliers} outliers from {col}")
                df_clean = df_clean[
                    (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)
                ]
        
        logger.info(f"Data cleaning completed. Final shape: {df_clean.shape}")
        return df_clean
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate data quality.
        
        Args:
            df: DataFrame to validate
        
        Returns:
            True if validation passes
        """
        logger.info("Validating data quality...")
        
        # Check required columns
        missing_cols = set(self.feature_columns + [self.target_column]) - set(df.columns)
        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            return False
        
        # Check data types
        for col in self.feature_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                logger.error(f"Column {col} is not numeric")
                return False
        
        # Check target values
        valid_targets = ["Candidate_A", "Candidate_B"]
        invalid_targets = ~df[self.target_column].isin(valid_targets)
        if invalid_targets.sum() > 0:
            logger.error(f"Found {invalid_targets.sum()} invalid target values")
            return False
        
        # Check for infinite values
        inf_count = np.isinf(df[self.feature_columns].values).sum()
        if inf_count > 0:
            logger.error(f"Found {inf_count} infinite values")
            return False
        
        logger.info("Data validation passed!")
        return True
    
    def scale_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Scale features using StandardScaler.
        
        Args:
            df: DataFrame with features
            fit: Whether to fit the scaler
        
        Returns:
            DataFrame with scaled features
        """
        logger.info("Scaling features...")
        df_scaled = df.copy()
        
        if fit:
            self.scaler.fit(df[self.feature_columns])
            logger.info("Scaler fitted on training data")
        
        df_scaled[self.feature_columns] = self.scaler.transform(df[self.feature_columns])
        
        return df_scaled
    
    def preprocess(
        self,
        df: pd.DataFrame,
        fit_scaler: bool = True
    ) -> pd.DataFrame:
        """
        Complete preprocessing pipeline.
        
        Args:
            df: Raw DataFrame
            fit_scaler: Whether to fit the scaler
        
        Returns:
            Preprocessed DataFrame
        """
        logger.info("Starting preprocessing pipeline...")
        
        # Clean data
        df_clean = self.clean_data(df)
        
        # Validate data
        if not self.validate_data(df_clean):
            raise ValueError("Data validation failed")
        
        # Scale features
        df_processed = self.scale_features(df_clean, fit=fit_scaler)
        
        logger.info("Preprocessing completed successfully!")
        return df_processed
    
    def save_scaler(self, path: Path):
        """Save the fitted scaler."""
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.scaler, path)
        logger.info(f"Scaler saved to {path}")
    
    def load_scaler(self, path: Path):
        """Load a fitted scaler."""
        self.scaler = joblib.load(path)
        logger.info(f"Scaler loaded from {path}")


def split_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into train and test sets.
    
    Args:
        df: DataFrame to split
        test_size: Proportion of test set
        random_state: Random seed
    
    Returns:
        Tuple of (train_df, test_df)
    """
    logger.info(f"Splitting data with test_size={test_size}")
    
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[Config.TARGET_COLUMN]
    )
    
    logger.info(f"Train set size: {len(train_df)}")
    logger.info(f"Test set size: {len(test_df)}")
    
    return train_df, test_df


def main():
    """Main preprocessing function."""
    from src.data.make_dataset import load_dataset
    
    Config.create_directories()
    
    # Load raw data
    df = load_dataset(Config.RAW_DATA_PATH)
    
    # Initialize preprocessor
    preprocessor = ElectionDataPreprocessor()
    
    # Preprocess data
    df_processed = preprocessor.preprocess(df, fit_scaler=True)
    
    # Split data
    train_df, test_df = split_data(df_processed, test_size=Config.TEST_SIZE)
    
    # Save processed data
    train_path = Config.DATA_DIR / "processed" / "train.csv"
    test_path = Config.DATA_DIR / "processed" / "test.csv"
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    logger.info(f"Train data saved to {train_path}")
    logger.info(f"Test data saved to {test_path}")
    
    # Save scaler
    scaler_path = Config.MODELS_DIR / "scaler.pkl"
    preprocessor.save_scaler(scaler_path)
    
    logger.info("Preprocessing completed successfully!")


if __name__ == "__main__":
    main()
