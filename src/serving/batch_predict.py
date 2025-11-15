"""
Batch prediction for election outcomes.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict
import joblib
from datetime import datetime

from src.utils.logger import get_logger
from src.utils.config import Config
from src.data.features import ElectionFeatureEngineering


logger = get_logger(__name__)


class BatchPredictor:
    """Batch prediction service for election data."""
    
    def __init__(self, model_path: Path = None):
        """
        Initialize batch predictor.
        
        Args:
            model_path: Path to the trained model
        """
        self.model_path = model_path or Config.MODELS_DIR / "best_model.pkl"
        self.model = None
        self.feature_engineer = ElectionFeatureEngineering()
        self.load_model()
    
    def load_model(self):
        """Load the trained model."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        self.model = joblib.load(self.model_path)
        logger.info(f"Model loaded from {self.model_path}")
    
    def predict_batch(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Make predictions on a batch of data.
        
        Args:
            df: DataFrame with election features
        
        Returns:
            DataFrame with predictions
        """
        logger.info(f"Making batch predictions for {len(df)} records...")
        
        # Engineer features
        df_features = self.feature_engineer.engineer_features(df)
        
        # Get feature columns
        feature_names = self.feature_engineer.get_all_feature_names()
        X = df_features[feature_names].values
        
        # Make predictions
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        # Add predictions to DataFrame
        df_results = df.copy()
        df_results['predicted_winner'] = np.where(
            predictions == 1,
            "Candidate_A",
            "Candidate_B"
        )
        df_results['confidence'] = np.max(probabilities, axis=1)
        df_results['probability_candidate_a'] = probabilities[:, 1]
        df_results['probability_candidate_b'] = probabilities[:, 0]
        df_results['prediction_timestamp'] = datetime.utcnow().isoformat()
        
        logger.info("Batch predictions completed successfully")
        
        return df_results
    
    def predict_from_file(
        self,
        input_path: Path,
        output_path: Path
    ):
        """
        Make predictions from input file and save to output file.
        
        Args:
            input_path: Path to input CSV file
            output_path: Path to save predictions
        """
        logger.info(f"Reading data from {input_path}")
        df = pd.read_csv(input_path)
        
        # Make predictions
        df_predictions = self.predict_batch(df)
        
        # Save predictions
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_predictions.to_csv(output_path, index=False)
        logger.info(f"Predictions saved to {output_path}")
        
        # Log summary statistics
        winner_counts = df_predictions['predicted_winner'].value_counts()
        logger.info(f"\nPrediction Summary:")
        logger.info(f"Total predictions: {len(df_predictions)}")
        for winner, count in winner_counts.items():
            percentage = (count / len(df_predictions)) * 100
            logger.info(f"{winner}: {count} ({percentage:.2f}%)")
        
        avg_confidence = df_predictions['confidence'].mean()
        logger.info(f"Average confidence: {avg_confidence:.4f}")
    
    def predict_streaming(
        self,
        input_path: Path,
        output_path: Path,
        batch_size: int = 1000
    ):
        """
        Make predictions in streaming mode for large datasets.
        
        Args:
            input_path: Path to input CSV file
            output_path: Path to save predictions
            batch_size: Number of records to process at once
        """
        logger.info(f"Starting streaming predictions with batch_size={batch_size}")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Process in chunks
        first_chunk = True
        total_processed = 0
        
        for chunk in pd.read_csv(input_path, chunksize=batch_size):
            # Make predictions
            chunk_predictions = self.predict_batch(chunk)
            
            # Write to file
            mode = 'w' if first_chunk else 'a'
            header = first_chunk
            chunk_predictions.to_csv(output_path, mode=mode, header=header, index=False)
            
            total_processed += len(chunk)
            logger.info(f"Processed {total_processed} records")
            
            first_chunk = False
        
        logger.info(f"Streaming predictions completed. Total records: {total_processed}")


def main():
    """Main batch prediction function."""
    logger.info("Starting batch prediction...")
    
    # Initialize predictor
    predictor = BatchPredictor()
    
    # Example: Predict on validation data
    input_path = Config.DATA_DIR / "raw" / "election_data_validation.csv"
    output_path = Config.BASE_DIR / "predictions" / "batch_predictions.csv"
    
    if not input_path.exists():
        logger.warning(f"Input file not found: {input_path}")
        logger.info("Generating sample data for batch prediction...")
        
        from src.data.make_dataset import generate_synthetic_election_data, save_dataset
        df_sample = generate_synthetic_election_data(n_samples=100, random_state=999)
        save_dataset(df_sample, input_path)
    
    # Make predictions
    predictor.predict_from_file(input_path, output_path)
    
    logger.info("Batch prediction completed successfully!")


if __name__ == "__main__":
    main()
