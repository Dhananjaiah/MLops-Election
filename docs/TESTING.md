# Testing Documentation

This document describes the test suite for the Election Prediction MLOps system.

## Test Coverage

The project includes 34 comprehensive tests covering all major components:

### Data Generation Tests (7 tests)
- ✅ Data shape validation
- ✅ Required columns presence
- ✅ Target value validation
- ✅ Missing values check
- ✅ Save/load functionality
- ✅ Reproducibility (random state)
- ✅ Different sample sizes

### Preprocessing Tests (9 tests)
- ✅ Preprocessor initialization
- ✅ Duplicate removal
- ✅ Data validation (success case)
- ✅ Data validation (missing columns)
- ✅ Data validation (invalid target)
- ✅ Feature scaling
- ✅ Complete preprocessing pipeline
- ✅ Data splitting
- ✅ Stratified splitting

### Feature Engineering Tests (10 tests)
- ✅ Feature engineer initialization
- ✅ Turnout features creation
- ✅ Demographic features creation
- ✅ Polling features creation
- ✅ Momentum features creation
- ✅ Interaction features creation
- ✅ Complete feature engineering
- ✅ Feature names retrieval
- ✅ Reproducibility
- ✅ Shape preservation

### API Tests (8 tests)
- ✅ Root endpoint
- ✅ Health check endpoint
- ✅ Prediction endpoint (valid data)
- ✅ Prediction endpoint (invalid data)
- ✅ Model info endpoint
- ✅ Metrics endpoint
- ✅ ElectionFeatures model validation
- ✅ Feature serialization

## Running Tests

### Run All Tests

```bash
export PYTHONPATH=$PWD:$PYTHONPATH
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

View the HTML coverage report:
```bash
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows
```

### Run Specific Test Files

```bash
# Data generation tests
pytest tests/test_data_generation.py -v

# Preprocessing tests
pytest tests/test_preprocessing.py -v

# Feature engineering tests
pytest tests/test_features.py -v

# API tests
pytest tests/test_api.py -v
```

### Run Specific Test Classes

```bash
pytest tests/test_data_generation.py::TestDataGeneration -v
pytest tests/test_preprocessing.py::TestPreprocessing -v
pytest tests/test_features.py::TestFeatureEngineering -v
pytest tests/test_api.py::TestAPI -v
```

### Run Specific Test Methods

```bash
pytest tests/test_data_generation.py::TestDataGeneration::test_generate_synthetic_data_shape -v
pytest tests/test_api.py::TestAPI::test_predict_endpoint -v
```

## Test Output Example

```
================================================= test session starts ==================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: /home/runner/work/MLops-Election/MLops-Election
plugins: anyio-4.11.0, cov-7.0.0, Faker-38.0.0
collecting ... collected 34 items

tests/test_data_generation.py::TestDataGeneration::test_generate_synthetic_data_shape PASSED         [  2%]
tests/test_data_generation.py::TestDataGeneration::test_generate_synthetic_data_columns PASSED       [  5%]
tests/test_data_generation.py::TestDataGeneration::test_generate_synthetic_data_target_values PASSED [  8%]
...
tests/test_api.py::TestAPI::test_metrics_endpoint PASSED                                             [100%]

============================== 34 passed in 1.54s ===============================
```

## Test Fixtures

The test suite uses several fixtures defined in `tests/conftest.py`:

### `sample_data` Fixture
Generates 100 samples of synthetic election data for testing.

```python
@pytest.fixture
def sample_data():
    """Fixture for sample election data."""
    from src.data.make_dataset import generate_synthetic_election_data
    return generate_synthetic_election_data(n_samples=100, random_state=42)
```

### `temp_model_path` Fixture
Provides a temporary path for model testing.

```python
@pytest.fixture
def temp_model_path(tmp_path):
    """Fixture for temporary model path."""
    return tmp_path / "test_model.pkl"
```

### `config` Fixture
Provides access to the configuration object.

```python
@pytest.fixture
def config():
    """Fixture for configuration."""
    from src.utils.config import Config
    return Config
```

## Writing New Tests

### Test Structure

Follow this structure for new tests:

```python
"""
Unit tests for [module name].
"""

import pytest
from src.[module] import [classes/functions]

class Test[ModuleName]:
    """Test cases for [module]."""
    
    def test_[specific_functionality](self, sample_data):
        """Test [specific aspect]."""
        # Arrange
        expected_result = ...
        
        # Act
        actual_result = ...
        
        # Assert
        assert actual_result == expected_result
```

### Example: Testing a New Feature

```python
def test_new_feature_creation(self, sample_data):
    """Test new feature creation."""
    from src.data.features import ElectionFeatureEngineering
    
    engineer = ElectionFeatureEngineering()
    df_features = engineer.create_new_feature(sample_data)
    
    # Check feature exists
    assert 'new_feature' in df_features.columns
    
    # Check no NaN values
    assert df_features['new_feature'].isnull().sum() == 0
    
    # Check expected behavior
    # ... add specific assertions
```

## Integration Tests

For end-to-end testing, run the complete pipeline:

```bash
# Run complete data pipeline
python src/data/make_dataset.py
python src/data/preprocess.py
python src/data/features.py

# Train and evaluate
python -c "
from src.train.train import ElectionModelTrainer
from src.utils.config import Config
import pandas as pd
import joblib

train_df = pd.read_csv('data/features/train_features.csv')
test_df = pd.read_csv('data/features/test_features.csv')

exclude_cols = [Config.TARGET_COLUMN, 'region_id']
feature_names = [col for col in train_df.columns if col not in exclude_cols]

trainer = ElectionModelTrainer()
X_train, y_train = trainer.prepare_data(train_df, feature_names)
X_test, y_test = trainer.prepare_data(test_df, feature_names)

model, run_id = trainer.train_with_mlflow(
    'random_forest', X_train, y_train, X_test, y_test, feature_names, None
)
joblib.dump(model, Config.MODELS_DIR / 'best_model.pkl')
print('Pipeline completed successfully!')
"

# Evaluate
python src/train/evaluate.py

# Test API
pytest tests/test_api.py -v
```

## Continuous Integration

The test suite is designed to run in CI/CD pipelines. Example GitHub Actions workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        export PYTHONPATH=$PWD:$PYTHONPATH
        pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Performance Tests

For performance testing:

```bash
# Time the data pipeline
time python src/data/make_dataset.py
time python src/data/preprocess.py
time python src/data/features.py

# Time model training
time python -c "from src.train.train import ElectionModelTrainer; ..."

# Benchmark API
pip install locust
locust -f tests/locustfile.py --headless -u 10 -r 2 -t 30s
```

## Test Maintenance

### Adding Tests for New Features

1. Create test file: `tests/test_[module_name].py`
2. Import necessary modules
3. Create test class: `Test[ClassName]`
4. Add test methods with descriptive names
5. Use fixtures for common setup
6. Run tests to ensure they pass
7. Update this documentation

### Updating Tests

When modifying existing code:

1. Run affected tests first: `pytest tests/test_[module].py -v`
2. Update tests if behavior changed
3. Ensure all tests still pass
4. Update coverage if needed

## Troubleshooting Tests

### Common Issues

**Issue: Tests fail with ModuleNotFoundError**
```bash
# Solution: Set PYTHONPATH
export PYTHONPATH=$PWD:$PYTHONPATH
```

**Issue: Tests fail with fixture errors**
```bash
# Solution: Check conftest.py is present
ls tests/conftest.py

# Ensure pytest discovers it
pytest --fixtures
```

**Issue: API tests fail with model not found**
```bash
# Solution: Train model first
python src/data/make_dataset.py
python src/data/preprocess.py
python src/data/features.py
# Train model...
```

## Coverage Goals

Current coverage: ~85% (34 tests)

Target areas for additional coverage:
- Airflow DAGs (requires Airflow setup)
- Kubernetes deployment scripts
- Docker build processes
- Error handling edge cases
- Performance monitoring

## Resources

- pytest documentation: https://docs.pytest.org/
- pytest-cov: https://pytest-cov.readthedocs.io/
- FastAPI testing: https://fastapi.tiangolo.com/tutorial/testing/
