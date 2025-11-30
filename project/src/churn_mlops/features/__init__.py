"""
Feature Engineering Module
==========================

This module handles feature engineering for the Customer Churn Prediction project.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Feature engineering pipeline for churn prediction.
    
    This class handles:
    - Numerical feature scaling
    - Categorical encoding
    - Feature creation
    - Missing value handling
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.numeric_columns = []
        self.categorical_columns = []
        self._is_fitted = False
    
    def fit(self, df: pd.DataFrame, target_column: str = "churn") -> "FeatureEngineer":
        """
        Fit the feature engineering pipeline on training data.
        
        Args:
            df: Training DataFrame
            target_column: Name of the target column
            
        Returns:
            self
        """
        logger.info("Fitting feature engineering pipeline")
        
        # Identify column types
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = df.select_dtypes(include=["object", "category"]).columns.tolist()
        
        # Remove target from numeric columns if present
        if target_column in self.numeric_columns:
            self.numeric_columns.remove(target_column)
        
        # Fit scaler on numeric columns
        if self.numeric_columns:
            self.scaler.fit(df[self.numeric_columns])
        
        # Fit label encoders for categorical columns
        for col in self.categorical_columns:
            le = LabelEncoder()
            le.fit(df[col].astype(str))
            self.label_encoders[col] = le
        
        self._is_fitted = True
        logger.info(f"Fitted on {len(self.numeric_columns)} numeric and {len(self.categorical_columns)} categorical columns")
        
        return self
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform features using the fitted pipeline.
        
        Args:
            df: DataFrame to transform
            
        Returns:
            Transformed DataFrame
        """
        if not self._is_fitted:
            raise ValueError("FeatureEngineer must be fitted before transform")
        
        logger.info("Transforming features")
        df_transformed = df.copy()
        
        # Scale numeric columns
        if self.numeric_columns:
            df_transformed[self.numeric_columns] = self.scaler.transform(df[self.numeric_columns])
        
        # Encode categorical columns
        for col in self.categorical_columns:
            if col in df.columns:
                df_transformed[col] = self.label_encoders[col].transform(df[col].astype(str))
        
        return df_transformed
    
    def fit_transform(self, df: pd.DataFrame, target_column: str = "churn") -> pd.DataFrame:
        """
        Fit and transform in one step.
        
        Args:
            df: DataFrame to fit and transform
            target_column: Name of the target column
            
        Returns:
            Transformed DataFrame
        """
        self.fit(df, target_column)
        return self.transform(df)


def create_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create derived features from existing columns.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with additional derived features
    """
    logger.info("Creating derived features")
    df_new = df.copy()
    
    # Example derived features for churn prediction
    if "tenure" in df.columns and "monthly_charges" in df.columns:
        df_new["avg_monthly_spend"] = df["total_charges"] / (df["tenure"] + 1)
    
    if "monthly_charges" in df.columns and "total_charges" in df.columns:
        df_new["charge_ratio"] = df["monthly_charges"] / (df["total_charges"] + 1)
    
    if "tenure" in df.columns:
        df_new["tenure_group"] = pd.cut(
            df["tenure"],
            bins=[0, 12, 24, 48, 72],
            labels=["0-1yr", "1-2yr", "2-4yr", "4+yr"]
        )
    
    return df_new


def handle_missing_values(
    df: pd.DataFrame,
    numeric_strategy: str = "median",
    categorical_strategy: str = "mode"
) -> pd.DataFrame:
    """
    Handle missing values in the DataFrame.
    
    Args:
        df: Input DataFrame
        numeric_strategy: Strategy for numeric columns ('mean', 'median', 'zero')
        categorical_strategy: Strategy for categorical columns ('mode', 'unknown')
        
    Returns:
        DataFrame with handled missing values
    """
    logger.info(f"Handling missing values: numeric={numeric_strategy}, categorical={categorical_strategy}")
    df_clean = df.copy()
    
    # Handle numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            if numeric_strategy == "median":
                df_clean[col].fillna(df[col].median(), inplace=True)
            elif numeric_strategy == "mean":
                df_clean[col].fillna(df[col].mean(), inplace=True)
            elif numeric_strategy == "zero":
                df_clean[col].fillna(0, inplace=True)
    
    # Handle categorical columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in categorical_cols:
        if df[col].isnull().any():
            if categorical_strategy == "mode":
                df_clean[col].fillna(df[col].mode()[0], inplace=True)
            elif categorical_strategy == "unknown":
                df_clean[col].fillna("unknown", inplace=True)
    
    return df_clean
