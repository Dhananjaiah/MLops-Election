"""
Feature engineering for election prediction.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict

from src.utils.logger import get_logger
from src.utils.config import Config


logger = get_logger(__name__)


class ElectionFeatureEngineering:
    """Engineer features for election prediction."""
    
    def __init__(self):
        """Initialize feature engineer."""
        self.engineered_features = []
    
    def create_turnout_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create features related to voter turnout.
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with turnout features
        """
        logger.info("Creating turnout features...")
        df_new = df.copy()
        
        # Turnout trend
        df_new["turnout_trend"] = (
            df_new["prev_election_turnout"] * df_new["voter_registration_rate"]
        )
        
        # Expected turnout based on demographics
        df_new["expected_turnout"] = (
            df_new["education_rate"] * 0.4 +
            df_new["urban_ratio"] * 0.3 +
            df_new["voter_registration_rate"] * 0.3
        )
        
        # Turnout surprise (actual vs expected)
        df_new["turnout_surprise"] = (
            df_new["prev_election_turnout"] - df_new["expected_turnout"]
        )
        
        self.engineered_features.extend([
            "turnout_trend",
            "expected_turnout",
            "turnout_surprise"
        ])
        
        return df_new
    
    def create_demographic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create demographic-related features.
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with demographic features
        """
        logger.info("Creating demographic features...")
        df_new = df.copy()
        
        # Demographic score
        df_new["demographic_score"] = (
            df_new["education_rate"] * df_new["median_income"] / 50000
        )
        
        # Age-income interaction
        df_new["age_income_interaction"] = (
            df_new["median_age"] * df_new["median_income"] / 1000000
        )
        
        # Urban-education interaction
        df_new["urban_education"] = (
            df_new["urban_ratio"] * df_new["education_rate"]
        )
        
        # Population density proxy
        df_new["population_density"] = np.log1p(df_new["population"])
        
        self.engineered_features.extend([
            "demographic_score",
            "age_income_interaction",
            "urban_education",
            "population_density"
        ])
        
        return df_new
    
    def create_polling_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create polling and survey features.
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with polling features
        """
        logger.info("Creating polling features...")
        df_new = df.copy()
        
        # Poll margin
        df_new["poll_margin"] = df_new["poll_candidate_a"] - df_new["poll_candidate_b"]
        
        # Poll confidence (inverse of undecided rate)
        df_new["poll_confidence"] = 1 - df_new["undecided_rate"]
        
        # Favorability difference
        df_new["favorability_diff"] = (
            df_new["candidate_a_favorability"] - df_new["candidate_b_favorability"]
        )
        
        # Poll-favorability alignment for candidate A
        df_new["poll_favorability_alignment"] = (
            df_new["poll_candidate_a"] * df_new["candidate_a_favorability"]
        )
        
        self.engineered_features.extend([
            "poll_margin",
            "poll_confidence",
            "favorability_diff",
            "poll_favorability_alignment"
        ])
        
        return df_new
    
    def create_momentum_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create momentum and trend features.
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with momentum features
        """
        logger.info("Creating momentum features...")
        df_new = df.copy()
        
        # Incumbent advantage (based on prev_winner_margin)
        df_new["incumbent_advantage"] = np.where(
            df_new["prev_winner_margin"] > 0,
            df_new["prev_winner_margin"],
            0
        )
        
        # Challenger momentum
        df_new["challenger_momentum"] = np.where(
            df_new["prev_winner_margin"] < 0,
            abs(df_new["prev_winner_margin"]),
            0
        )
        
        # Overall momentum score
        df_new["momentum_score"] = (
            df_new["social_sentiment_score"] * 0.5 +
            df_new["poll_margin"] * 0.5
        )
        
        self.engineered_features.extend([
            "incumbent_advantage",
            "challenger_momentum",
            "momentum_score"
        ])
        
        return df_new
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create interaction features between key variables.
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with interaction features
        """
        logger.info("Creating interaction features...")
        df_new = df.copy()
        
        # Poll × Turnout interaction
        df_new["poll_turnout"] = (
            df_new["poll_candidate_a"] * df_new["prev_election_turnout"]
        )
        
        # Sentiment × Favorability interaction
        df_new["sentiment_favorability"] = (
            df_new["social_sentiment_score"] * df_new["candidate_a_favorability"]
        )
        
        # Urban × Income interaction
        df_new["urban_income"] = (
            df_new["urban_ratio"] * df_new["median_income"] / 50000
        )
        
        self.engineered_features.extend([
            "poll_turnout",
            "sentiment_favorability",
            "urban_income"
        ])
        
        return df_new
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply all feature engineering transformations.
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with engineered features
        """
        logger.info("Starting feature engineering pipeline...")
        
        df_features = df.copy()
        
        # Apply all feature engineering steps
        df_features = self.create_turnout_features(df_features)
        df_features = self.create_demographic_features(df_features)
        df_features = self.create_polling_features(df_features)
        df_features = self.create_momentum_features(df_features)
        df_features = self.create_interaction_features(df_features)
        
        logger.info(f"Feature engineering completed. New features: {len(self.engineered_features)}")
        logger.info(f"Engineered features: {self.engineered_features}")
        
        return df_features
    
    def get_all_feature_names(self) -> List[str]:
        """Get list of all features including engineered ones."""
        return Config.ALL_FEATURES + self.engineered_features


def main():
    """Main feature engineering function."""
    Config.create_directories()
    
    # Load processed data
    train_path = Config.DATA_DIR / "processed" / "train.csv"
    test_path = Config.DATA_DIR / "processed" / "test.csv"
    
    if not train_path.exists() or not test_path.exists():
        logger.error("Processed data not found. Please run preprocessing first.")
        return
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    logger.info(f"Loaded train data: {train_df.shape}")
    logger.info(f"Loaded test data: {test_df.shape}")
    
    # Initialize feature engineer
    feature_engineer = ElectionFeatureEngineering()
    
    # Engineer features
    train_features = feature_engineer.engineer_features(train_df)
    test_features = feature_engineer.engineer_features(test_df)
    
    # Save feature-engineered data
    train_features_path = Config.DATA_DIR / "features" / "train_features.csv"
    test_features_path = Config.DATA_DIR / "features" / "test_features.csv"
    
    train_features.to_csv(train_features_path, index=False)
    test_features.to_csv(test_features_path, index=False)
    
    logger.info(f"Train features saved to {train_features_path}")
    logger.info(f"Test features saved to {test_features_path}")
    
    # Save feature names
    feature_names_path = Config.DATA_DIR / "features" / "feature_names.txt"
    with open(feature_names_path, 'w') as f:
        for feature in feature_engineer.get_all_feature_names():
            f.write(f"{feature}\n")
    
    logger.info(f"Feature names saved to {feature_names_path}")
    logger.info("Feature engineering completed successfully!")


if __name__ == "__main__":
    main()
