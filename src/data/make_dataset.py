"""
Generate synthetic election dataset for training.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple

from src.utils.logger import get_logger
from src.utils.config import Config


logger = get_logger(__name__)


def generate_synthetic_election_data(
    n_samples: int = 10000,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Generate synthetic election data with realistic features.
    
    Args:
        n_samples: Number of samples to generate
        random_state: Random seed for reproducibility
    
    Returns:
        DataFrame with synthetic election data
    """
    np.random.seed(random_state)
    logger.info(f"Generating {n_samples} synthetic election records...")
    
    # Demographic features
    data = {
        "region_id": [f"R{i:05d}" for i in range(n_samples)],
        "population": np.random.randint(10000, 500000, n_samples),
        "median_age": np.random.normal(45, 10, n_samples).clip(25, 75),
        "median_income": np.random.normal(55000, 20000, n_samples).clip(20000, 150000),
        "education_rate": np.random.uniform(0.6, 0.95, n_samples),
        "urban_ratio": np.random.uniform(0.1, 0.9, n_samples),
    }
    
    # Voting history
    data["prev_election_turnout"] = np.random.uniform(0.45, 0.85, n_samples)
    data["prev_winner_margin"] = np.random.uniform(-0.3, 0.3, n_samples)
    data["voter_registration_rate"] = np.random.uniform(0.5, 0.95, n_samples)
    
    # Survey data
    data["poll_candidate_a"] = np.random.uniform(0.2, 0.6, n_samples)
    data["poll_candidate_b"] = 1 - data["poll_candidate_a"] - np.random.uniform(0.05, 0.15, n_samples)
    data["undecided_rate"] = 1 - data["poll_candidate_a"] - data["poll_candidate_b"]
    
    # Sentiment scores
    data["social_sentiment_score"] = np.random.uniform(-1, 1, n_samples)
    data["candidate_a_favorability"] = np.random.uniform(0.3, 0.7, n_samples)
    data["candidate_b_favorability"] = np.random.uniform(0.3, 0.7, n_samples)
    
    # Create target based on features with some noise
    # Higher poll numbers, favorability, and positive sentiment favor that candidate
    candidate_a_score = (
        data["poll_candidate_a"] * 0.4 +
        data["candidate_a_favorability"] * 0.3 +
        (data["social_sentiment_score"] + 1) / 2 * 0.2 +
        np.random.uniform(0, 0.1, n_samples)
    )
    
    candidate_b_score = (
        data["poll_candidate_b"] * 0.4 +
        data["candidate_b_favorability"] * 0.3 +
        (1 - (data["social_sentiment_score"] + 1) / 2) * 0.2 +
        np.random.uniform(0, 0.1, n_samples)
    )
    
    data["winning_candidate"] = np.where(
        candidate_a_score > candidate_b_score,
        "Candidate_A",
        "Candidate_B"
    )
    
    df = pd.DataFrame(data)
    logger.info(f"Generated dataset shape: {df.shape}")
    logger.info(f"Target distribution:\n{df['winning_candidate'].value_counts()}")
    
    return df


def save_dataset(df: pd.DataFrame, output_path: Path):
    """
    Save dataset to CSV file.
    
    Args:
        df: DataFrame to save
        output_path: Path to save the dataset
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Dataset saved to {output_path}")


def load_dataset(input_path: Path) -> pd.DataFrame:
    """
    Load dataset from CSV file.
    
    Args:
        input_path: Path to the dataset
    
    Returns:
        Loaded DataFrame
    """
    if not input_path.exists():
        logger.warning(f"Dataset not found at {input_path}. Generating new dataset...")
        df = generate_synthetic_election_data()
        save_dataset(df, input_path)
        return df
    
    logger.info(f"Loading dataset from {input_path}")
    df = pd.read_csv(input_path)
    logger.info(f"Loaded dataset shape: {df.shape}")
    return df


def main():
    """Main function to generate and save election dataset."""
    Config.create_directories()
    
    # Generate training dataset
    df = generate_synthetic_election_data(n_samples=10000)
    save_dataset(df, Config.RAW_DATA_PATH)
    
    # Generate additional validation dataset
    df_val = generate_synthetic_election_data(n_samples=2000, random_state=123)
    val_path = Config.DATA_DIR / "raw" / "election_data_validation.csv"
    save_dataset(df_val, val_path)
    
    logger.info("Dataset generation completed successfully!")


if __name__ == "__main__":
    main()
