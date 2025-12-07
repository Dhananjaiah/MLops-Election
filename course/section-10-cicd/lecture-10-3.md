# Lecture 10.3 – Writing Tests for ML Code (Unit, Integration, Smoke)

## In This Lecture You Will Learn

- [x] Understand different types of tests for ML code (unit, integration, smoke)
- [x] Learn how to test ML-specific components (preprocessing, models, predictions)
- [x] Know testing best practices and common pitfalls in ML testing

---

## Real-World Context

> **Story**: An insurance company deployed a new claim fraud detection model. It worked perfectly in testing but failed catastrophically in production—predicting 95% of legitimate claims as fraud.
>
> The bug? A preprocessing step that normalized numeric features used training data statistics instead of inference-time statistics. The issue wasn't caught because they only tested the model, not the full inference pipeline.
>
> After adding end-to-end integration tests that validated the complete prediction flow, they caught these issues in CI before deployment.

Testing ML code is harder than traditional software—you need to test data, models, and pipelines together.

---

## Main Content

### 1. Types of Tests for ML Systems

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ML TESTING PYRAMID                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                           ┌──────────────┐                                   │
│                           │ SMOKE TESTS  │  ← Fast sanity checks            │
│                           │  (seconds)   │     Run on every commit          │
│                           └──────────────┘                                   │
│                         /                  \                                 │
│                       /                      \                               │
│              ┌──────────────┐          ┌──────────────┐                      │
│              │ INTEGRATION  │          │ MODEL EVAL   │  ← Slower validation │
│              │    TESTS     │          │    TESTS     │     Run on PR/nightly│
│              │  (minutes)   │          │  (minutes)   │                      │
│              └──────────────┘          └──────────────┘                      │
│            /                                          \                      │
│          /                                              \                    │
│  ┌──────────────┐                              ┌──────────────┐             │
│  │  UNIT TESTS  │                              │ DATA QUALITY │  ← Fastest  │
│  │  (millisec)  │                              │    TESTS     │     Most    │
│  └──────────────┘                              └──────────────┘     frequent│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Test Types Explained**:

1. **Unit Tests**: Test individual functions in isolation
   - Feature engineering functions
   - Data cleaning logic
   - Utility functions
   - Custom metrics

2. **Integration Tests**: Test components working together
   - Full prediction pipeline
   - Model loading + prediction
   - API endpoint tests

3. **Smoke Tests**: Quick sanity checks
   - Model loads
   - Can make one prediction
   - No immediate crashes

4. **Model Evaluation Tests**: Validate model quality
   - Performance on holdout set
   - Drift detection
   - Bias/fairness checks

### 2. Unit Testing ML Components

```python
# tests/test_preprocessing.py
import pytest
import pandas as pd
import numpy as np
from src.preprocessing import clean_age, normalize_income, encode_categories

def test_clean_age_handles_invalid_values():
    """Age cleaning should cap outliers and handle negatives"""
    ages = pd.Series([25, 150, -5, 45, 200, np.nan])
    result = clean_age(ages)
    
    # Check bounds
    assert result[result.notna()].min() >= 18
    assert result[result.notna()].max() <= 120
    
    # Check length preserved
    assert len(result) == len(ages)
    
    # Check NaN handling
    assert result.isna().sum() == 1  # Only original NaN

def test_normalize_income_preserves_scale():
    """Income normalization should be between 0 and 1"""
    incomes = pd.Series([0, 50000, 100000, 200000])
    result = normalize_income(incomes)
    
    assert result.min() >= 0
    assert result.max() <= 1
    assert len(result) == len(incomes)

def test_encode_categories_unknown_handling():
    """Unknown categories should map to 'OTHER'"""
    encoder = CategoryEncoder()
    encoder.fit(['cat_A', 'cat_B', 'cat_C'])
    
    # Test with unknown category
    result = encoder.transform(['cat_A', 'cat_UNKNOWN', 'cat_B'])
    
    assert result[0] == 'cat_A'
    assert result[1] == 'OTHER'  # Unknown mapped
    assert result[2] == 'cat_B'

def test_feature_engineering_output_shape():
    """Feature engineering should produce expected number of columns"""
    raw_data = pd.DataFrame({
        'age': [25, 35, 45],
        'income': [50000, 75000, 100000],
        'state': ['CA', 'NY', 'TX']
    })
    
    features = engineer_features(raw_data)
    
    # Should have original + engineered features
    assert features.shape[0] == 3  # Same rows
    assert features.shape[1] >= 3  # At least original columns
```

**What to Unit Test in ML**:
- ✅ Input validation (nulls, types, ranges)
- ✅ Transformation logic (scaling, encoding)
- ✅ Feature engineering functions
- ✅ Custom metrics and loss functions
- ✅ Data loading utilities

### 3. Integration Testing ML Pipelines

```python
# tests/test_integration.py
import pytest
from src.pipeline import load_data, preprocess, train_model, predict

def test_end_to_end_prediction_pipeline():
    """Test complete flow from raw data to prediction"""
    # Load test data
    raw_data = load_data('tests/fixtures/test_data.csv')
    
    # Run preprocessing
    preprocessed = preprocess(raw_data)
    assert preprocessed is not None
    assert len(preprocessed) == len(raw_data)
    
    # Load model and predict
    model = load_model('tests/fixtures/test_model.pkl')
    predictions = model.predict(preprocessed)
    
    # Validate output
    assert len(predictions) == len(raw_data)
    assert all(0 <= p <= 1 for p in predictions)  # Valid probabilities
    assert predictions.dtype == float

def test_model_serialization_roundtrip():
    """Model should save and load correctly"""
    # Train a simple model
    X, y = load_training_data()
    original_model = train_model(X, y)
    original_predictions = original_model.predict(X[:10])
    
    # Save and load
    save_model(original_model, '/tmp/test_model.pkl')
    loaded_model = load_model('/tmp/test_model.pkl')
    loaded_predictions = loaded_model.predict(X[:10])
    
    # Predictions should match
    np.testing.assert_array_almost_equal(
        original_predictions, 
        loaded_predictions, 
        decimal=5
    )

def test_prediction_api_endpoint():
    """Test API can handle prediction requests"""
    from fastapi.testclient import TestClient
    from src.api import app
    
    client = TestClient(app)
    
    # Send prediction request
    response = client.post('/predict', json={
        'age': 35,
        'income': 75000,
        'tenure_months': 24
    })
    
    assert response.status_code == 200
    data = response.json()
    assert 'prediction' in data
    assert 0 <= data['prediction'] <= 1

def test_batch_prediction_performance():
    """Batch predictions should be reasonably fast"""
    import time
    
    model = load_model('artifacts/model.pkl')
    test_data = create_test_samples(n=1000)
    
    start = time.time()
    predictions = model.predict(test_data)
    duration = time.time() - start
    
    # Should process 1000 samples in < 1 second
    assert duration < 1.0
    assert len(predictions) == 1000
```

### 4. Smoke Tests for Quick Validation

```python
# tests/test_smoke.py
import pytest

def test_model_artifact_exists():
    """Model file should exist"""
    from pathlib import Path
    model_path = Path('artifacts/model.pkl')
    assert model_path.exists(), "Model artifact not found"

def test_model_loads_without_error():
    """Model should load successfully"""
    model = load_model('artifacts/model.pkl')
    assert model is not None

def test_can_make_single_prediction():
    """Basic prediction should work"""
    model = load_model('artifacts/model.pkl')
    sample = pd.DataFrame({
        'age': [35],
        'income': [75000],
        'tenure_months': [24]
    })
    
    prediction = model.predict(sample)
    
    assert len(prediction) == 1
    assert isinstance(prediction[0], (int, float))

def test_prediction_output_format():
    """Predictions should have correct format"""
    model = load_model('artifacts/model.pkl')
    samples = create_test_samples(n=5)
    
    predictions = model.predict(samples)
    
    # Should return array-like
    assert hasattr(predictions, '__len__')
    assert len(predictions) == 5
    
    # All values should be numbers
    assert all(isinstance(p, (int, float, np.number)) for p in predictions)

def test_no_crashes_on_typical_inputs():
    """Model should handle typical inputs without crashing"""
    model = load_model('artifacts/model.pkl')
    
    typical_cases = pd.DataFrame({
        'age': [25, 35, 45, 55, 65],
        'income': [30000, 50000, 75000, 100000, 150000],
        'tenure_months': [1, 12, 24, 36, 60]
    })
    
    # Should not raise exception
    predictions = model.predict(typical_cases)
    assert len(predictions) == 5
```

---

## Lab / Demo

### Prerequisites

- Python 3.9+ with pytest installed
- Course repository cloned
- Virtual environment activated

### Step-by-Step Instructions

```bash
# Step 1: Install testing dependencies
pip install pytest pytest-cov pytest-xdist

# Step 2: Create test directory structure
mkdir -p tests/{unit,integration,smoke}
mkdir -p tests/fixtures

# Step 3: Create a simple unit test
cat > tests/unit/test_preprocessing.py << 'PYTEST'
import pandas as pd
from src.preprocessing import clean_age

def test_clean_age():
    ages = pd.Series([25, 150, -5, 45])
    result = clean_age(ages)
    
    assert result.min() >= 18
    assert result.max() <= 120
PYTEST

# Step 4: Create an integration test
cat > tests/integration/test_pipeline.py << 'PYTEST'
from src.pipeline import predict

def test_end_to_end():
    data = {'age': 35, 'income': 75000}
    result = predict(data)
    assert 0 <= result <= 1
PYTEST

# Step 5: Run all tests
pytest tests/ -v

# Step 6: Run with coverage
pytest tests/ --cov=src --cov-report=html

# Step 7: Run only fast tests
pytest tests/unit tests/smoke -v

# Step 8: Run in parallel (faster)
pytest tests/ -n auto
```

### Expected Output

```
================================ test session starts =================================
tests/unit/test_preprocessing.py::test_clean_age PASSED                       [ 25%]
tests/integration/test_pipeline.py::test_end_to_end PASSED                    [ 50%]
tests/smoke/test_model.py::test_model_loads PASSED                            [ 75%]
tests/smoke/test_model.py::test_can_predict PASSED                            [100%]

================================= 4 passed in 2.34s ==================================

---------- coverage: platform linux, python 3.9.7 -----------
Name                    Stmts   Miss  Cover
-------------------------------------------
src/__init__.py            0      0   100%
src/preprocessing.py      45      2    96%
src/pipeline.py           67      5    93%
-------------------------------------------
TOTAL                    112      7    94%
```

---

## Common Pitfalls / Gotchas

- ⚠️ **Testing Only the Model**: Test the entire pipeline (data loading → preprocessing → prediction → output formatting). Most bugs are in glue code.

- ⚠️ **Non-Deterministic Tests**: Random seeds, GPU precision, and async operations cause flaky tests. Always set `random_state=42` and use `torch.manual_seed()`.

- ⚠️ **Testing on Training Data**: Use separate test fixtures. Never test on data the model was trained on.

- ⚠️ **Ignoring Edge Cases**: Test nulls, empty inputs, extreme values, and single-row inputs. These break in production.

- ⚠️ **Slow Test Suites**: Keep unit tests fast (<100ms each). Use fixtures and mocking for external dependencies.

---

## Homework / Practice

1. **Exercise 1**: Add unit tests for your preprocessing functions
   - Test each transformation function
   - Include edge cases (nulls, extremes, empty inputs)
   - Aim for >90% code coverage

2. **Exercise 2**: Create integration tests for your prediction pipeline
   - Test full flow from raw data to prediction
   - Validate output format and ranges
   - Test error handling

3. **Stretch Goal**: Implement property-based testing
   - Use `hypothesis` library
   - Generate random valid inputs
   - Check invariants hold (e.g., output always between 0-1)

---

## Quick Quiz

1. **What should you test in ML code that's different from traditional software?**
   - A) Only the model training code
   - B) Data quality, preprocessing, and the full prediction pipeline
   - C) Just the API endpoints
   - D) Only unit tests are needed

   **Answer: B** - ML requires testing data, preprocessing, models, and pipelines together.

2. **Why are smoke tests important in ML CI/CD?**
   - A) They test everything thoroughly
   - B) They're not important
   - C) They quickly catch obvious breaks (model loads, can predict) in seconds
   - D) They replace unit tests

   **Answer: C** - Smoke tests provide fast feedback that the system isn't completely broken.

3. **True or False: It's okay to test ML models on the same data they were trained on.**

   **Answer: False** - This gives false confidence. Always use separate test data or holdout sets.

---

## Summary

- ML systems need multiple test types: unit (fast, isolated), integration (pipeline), smoke (sanity), and model evaluation
- Test the full pipeline, not just the model—most bugs are in preprocessing and glue code
- Keep unit tests fast (<100ms), use fixtures for test data, set random seeds for reproducibility
- Smoke tests catch obvious breaks quickly; save expensive model training tests for nightly runs
- Use tiered testing: fast checks on every commit, slower validation on PRs, full evaluation nightly

---

## Next Steps

→ Continue to **Lecture 10.4**: Building Docker Images & Pushing to Registry in CI

---

## Additional Resources

- [Google's Testing ML Systems](https://developers.google.com/machine-learning/testing-debugging)
- [pytest Documentation](https://docs.pytest.org/)
- [Effective Testing for Machine Learning](https://www.jeremyjordan.me/testing-ml/)
- [Property-Based Testing with Hypothesis](https://hypothesis.readthedocs.io/)
