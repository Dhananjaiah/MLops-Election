# Quick Start Guide - Election Prediction MLOps System

This guide provides tested, working commands to get started with the Election Prediction MLOps system.

## Prerequisites

- Python 3.9, 3.10, 3.11, or 3.12
- pip (latest version recommended)
- 2GB+ RAM
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MLops-Election.git
cd MLops-Election
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

## Running the Complete Pipeline

### Step 1: Generate Data

```bash
export PYTHONPATH=$PWD:$PYTHONPATH  # On Windows: set PYTHONPATH=%CD%;%PYTHONPATH%
python src/data/make_dataset.py
```

Expected output: Generates 10,000 training samples and 2,000 validation samples.

### Step 2: Preprocess Data

```bash
python src/data/preprocess.py
```

Expected output: Creates cleaned, scaled, and split train/test datasets.

### Step 3: Engineer Features

```bash
python src/data/features.py
```

Expected output: Creates 31 total features (14 original + 17 engineered).

### Step 4: Train Models

For quick training without hyperparameter tuning:

```bash
export MLFLOW_TRACKING_URI=file:///tmp/mlruns  # On Windows: set MLFLOW_TRACKING_URI=file:///tmp/mlruns

python -c "
from src.train.train import ElectionModelTrainer
from src.utils.config import Config
import pandas as pd

# Load data
train_df = pd.read_csv('data/features/train_features.csv')
test_df = pd.read_csv('data/features/test_features.csv')

# Get features
exclude_cols = [Config.TARGET_COLUMN, 'region_id']
feature_names = [col for col in train_df.columns if col not in exclude_cols]

# Prepare data
trainer = ElectionModelTrainer()
X_train, y_train = trainer.prepare_data(train_df, feature_names)
X_test, y_test = trainer.prepare_data(test_df, feature_names)

# Train model
print('Training Random Forest model...')
model, run_id = trainer.train_with_mlflow(
    'random_forest',
    X_train, y_train, X_test, y_test,
    feature_names,
    hyperparameters=None
)

# Save model
import joblib
Config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(model, Config.MODELS_DIR / 'best_model.pkl')
print(f'Model saved to {Config.MODELS_DIR / \"best_model.pkl\"}')
"
```

Expected output: Model trained with ~91% accuracy.

### Step 5: Evaluate Model

```bash
python src/train/evaluate.py
```

Expected output: Evaluation metrics, confusion matrix, and ROC curve saved to `reports/`.

## Running the API

### Start the API Server

```bash
uvicorn src.serving.api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

### Test the API

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Make a Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "population": 150000,
    "median_age": 42.5,
    "median_income": 55000,
    "education_rate": 0.85,
    "urban_ratio": 0.7,
    "prev_election_turnout": 0.68,
    "prev_winner_margin": 0.05,
    "voter_registration_rate": 0.82,
    "social_sentiment_score": 0.15,
    "candidate_a_favorability": 0.55,
    "candidate_b_favorability": 0.48,
    "poll_candidate_a": 0.48,
    "poll_candidate_b": 0.45,
    "undecided_rate": 0.07
  }'
```

#### View API Documentation

Open your browser to:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Monitoring

### Check for Data Drift

```bash
python src/monitoring/drift_monitoring.py
```

Expected output: Drift detection report saved to `reports/drift_report.json`.

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

Expected output: 34 tests passing.

### Run Tests with Coverage

```bash
pytest tests/ -v --cov=src --cov-report=term --cov-report=html
```

Coverage report will be available in `htmlcov/index.html`.

### Run Specific Test Files

```bash
# Test data generation
pytest tests/test_data_generation.py -v

# Test preprocessing
pytest tests/test_preprocessing.py -v

# Test feature engineering
pytest tests/test_features.py -v

# Test API
pytest tests/test_api.py -v
```

## Performance Metrics

Based on actual test runs:

- **Model Accuracy**: 91.15%
- **F1 Score**: 89.12%
- **ROC-AUC**: 97.62%
- **Training Time**: ~3-5 seconds (without hyperparameter tuning)
- **API Latency**: <100ms per prediction

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'src'

**Solution**: Set the PYTHONPATH:
```bash
export PYTHONPATH=$PWD:$PYTHONPATH  # On Windows: set PYTHONPATH=%CD%;%PYTHONPATH%
```

Or install in development mode:
```bash
pip install -e .
```

### Issue: Model not found

**Solution**: Make sure you've run the training step first:
```bash
python src/data/make_dataset.py
python src/data/preprocess.py
python src/data/features.py
# Then train the model as shown above
```

### Issue: MLflow warnings

**Solution**: These are warnings about filesystem backend deprecation. They don't affect functionality. To suppress:
```bash
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db
```

## Project Structure

```
MLops-Election/
├── data/                   # Data files (raw, processed, features)
│   ├── raw/               # Raw generated data
│   ├── processed/         # Cleaned and split data
│   └── features/          # Feature-engineered data
├── models/                # Trained models and scalers
├── reports/               # Evaluation reports and plots
│   └── figures/          # Generated plots
├── src/                   # Source code
│   ├── data/             # Data pipeline
│   ├── train/            # Model training
│   ├── serving/          # API service
│   ├── monitoring/       # Drift monitoring
│   └── utils/            # Utilities
├── tests/                # Test suite
├── requirements.txt      # Dependencies
├── setup.py             # Package setup
└── README.md            # Documentation
```

## Next Steps

1. Explore the Jupyter notebooks (if available) for detailed analysis
2. Customize the model hyperparameters in `src/utils/config.py`
3. Add your own data sources
4. Deploy to production using Docker/Kubernetes
5. Set up continuous monitoring with Prometheus/Grafana

## Support

For issues or questions:
- Open an issue on GitHub
- Check the main [README.md](README.md) for detailed documentation
- Review the test files for usage examples
