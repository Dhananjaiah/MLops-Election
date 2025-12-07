# Lecture 10.2 – Extra Complexity in ML CI/CD (Data, Drift, Longer Runs)

## In This Lecture You Will Learn

- [x] Understand why ML CI/CD is harder than traditional software CI/CD
- [x] Learn about data dependencies, model drift, and long training times in pipelines
- [x] Know strategies to handle ML-specific challenges in automated workflows

---

## Real-World Context

> **Story**: An e-commerce company had a perfect CI/CD pipeline for their web application—tests ran in 3 minutes, deployments took 5 minutes. Then they added ML to predict product recommendations.
>
> Suddenly, their "simple" CI pipeline took 2 hours because it retrained the model on every commit. Data validation added 20 minutes. Model evaluation took another 30 minutes. Their pipeline became so slow that developers stopped checking in code daily. Quality suffered.
>
> They eventually learned to separate fast feedback loops (code quality, unit tests) from slow ones (full model retraining). This brought their CI time back to 10 minutes for most commits, with full model validation running nightly.

ML systems add layers of complexity that traditional CI/CD doesn't handle well.

---

## Main Content

### 1. Why ML CI/CD is Different from Traditional Software

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 TRADITIONAL CI/CD vs ML CI/CD                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TRADITIONAL SOFTWARE CI/CD                                                 │
│  ═══════════════════════════════                                            │
│                                                                              │
│  Code ──→ Build ──→ Test ──→ Deploy                                        │
│           (2 min)   (5 min)   (3 min)                                       │
│                                                                              │
│  Dependencies:                                                               │
│  • Code only                                                                │
│  • Libraries (fixed versions)                                               │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  ML CI/CD (MUCH MORE COMPLEX)                                               │
│  ═══════════════════════════                                                │
│                                                                              │
│  Code ──┐                                                                   │
│  Data ──┼──→ Validate ──→ Train ──→ Evaluate ──→ Test ──→ Deploy          │
│  Config─┘     (10 min)    (60 min)   (15 min)    (10 min)  (5 min)        │
│                                                                              │
│  Dependencies:                                                               │
│  • Code (logic changes)                                                     │
│  • Data (distribution changes)                                              │
│  • Model (weights, architecture)                                            │
│  • Features (engineering pipeline)                                          │
│  • Hyperparameters (configs)                                                │
│  • Infrastructure (GPU, memory)                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Differences:**

1. **Data is a First-Class Dependency**
   - Code can be perfect, but bad data = bad model
   - Data quality can degrade without code changes
   - Need to validate data in CI/CD

2. **Non-Deterministic Outcomes**
   - Same code + same data ≠ always same model (random seeds, GPU precision)
   - Can't use simple "expected output" tests
   - Need statistical validation instead

3. **Long-Running Processes**
   - Training can take minutes to hours
   - Can't run full training on every commit
   - Need smart caching and incremental approaches

4. **Multiple Artifacts**
   - Traditional: Binary/container
   - ML: Code + Data + Model + Metadata + Configs

### 2. ML-Specific Challenges in CI/CD

#### Challenge 1: Data Dependency Management

```yaml
# Traditional CI: Package versions in requirements.txt
dependencies:
  - flask==2.3.0
  - pandas==2.0.1

# ML CI: Also need data versions
data_dependencies:
  - training_data: "s3://bucket/data/v2.3"
  - validation_data: "s3://bucket/data/v2.3"
  - feature_definitions: "dvc://features.dvc@abc123"
```

**Problem**: Data changes outside your CI system:
- New data arrives daily
- Schema evolves
- Distribution shifts over time

**Solution Strategies**:

1. **Data Validation Gates**
```python
# Example validation in CI
def validate_training_data(data_path):
    """Run before training in CI"""
    checks = {
        'schema': check_schema(data_path),
        'completeness': check_nulls(data_path),
        'distribution': check_distributions(data_path),
        'size': check_min_rows(data_path, min_rows=10000)
    }
    
    if not all(checks.values()):
        raise ValueError(f"Data validation failed: {checks}")
```

2. **Data Versioning**
```bash
# Pin exact data version in CI
dvc checkout training_data.dvc@v1.2.3

# Or use content-based addressing
aws s3 cp s3://bucket/data_snapshot_20240101.parquet ./
```

3. **Synthetic Test Data**
```python
# Use small, fast, version-controlled test data for CI
if os.getenv('CI'):
    data = load_test_fixture('ci_test_data.csv')  # 1000 rows
else:
    data = load_production_data()  # 10M rows
```

#### Challenge 2: Long Training Times

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TRAINING TIME PROBLEM                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Developer Workflow:                                                         │
│                                                                              │
│  1. Write code change (5 min)                                               │
│  2. Push to Git                                                             │
│  3. CI triggers...                                                          │
│     ├─ Lint & unit tests (2 min) ✓                                         │
│     ├─ Data validation (10 min) ✓                                          │
│     └─ Full model training (90 min) ← PROBLEM!                             │
│                                                                              │
│  Total feedback time: 102 minutes                                           │
│                                                                              │
│  Developer context switch, works on something else, forgets about change... │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Solution Strategies**:

**A. Tiered Testing Approach**

```yaml
# .github/workflows/ml-ci.yml
name: ML CI

on: [push, pull_request]

jobs:
  # Fast feedback (runs on every commit)
  fast-checks:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v3
      - name: Lint code
        run: make lint
      - name: Unit tests
        run: pytest tests/unit/
      - name: Smoke test (tiny model)
        run: python train.py --epochs=1 --data=test_fixture.csv
  
  # Slower validation (runs on PR only)
  model-validation:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    timeout-minutes: 30
    steps:
      - name: Train on subset
        run: python train.py --data-sample=0.1
      - name: Validate metrics
        run: python validate_model.py --min-auc=0.75
  
  # Full training (runs nightly or on main branch)
  full-training:
    runs-on: gpu-runner
    if: github.ref == 'refs/heads/main'
    timeout-minutes: 120
    steps:
      - name: Train full model
        run: python train.py --full
      - name: Register model if passing
        run: python register_model.py
```

**B. Smart Caching**

```python
# Cache intermediate artifacts
import joblib
from pathlib import Path

def train_with_cache(data_version, code_hash):
    cache_key = f"{data_version}_{code_hash}"
    cache_file = Path(f"cache/model_{cache_key}.pkl")
    
    if cache_file.exists():
        print(f"Loading cached model for {cache_key}")
        return joblib.load(cache_file)
    
    # Train only if cache miss
    model = train_model(data)
    joblib.dump(model, cache_file)
    return model
```

**C. Training on Subset**

```python
# Quick validation training in CI
def ci_friendly_training(data, full=False):
    if os.getenv('CI') and not full:
        # Sample 10% for fast feedback
        data = data.sample(frac=0.1, random_state=42)
        epochs = 10
    else:
        epochs = 100
    
    return train(data, epochs=epochs)
```

#### Challenge 3: Model Drift Detection

```python
# Traditional software: Same input → Same output
def calculate_price(quantity, unit_price):
    return quantity * unit_price  # Deterministic

# ML: Same input → Different output over time
def predict_churn(customer_features):
    return model.predict(customer_features)  # Model degrades!
```

**Why Models Drift**:

1. **Data Distribution Changes** (Covariate Shift)
   - Customer behavior changes post-pandemic
   - New product categories added
   - Seasonal patterns shift

2. **Target Definition Changes** (Concept Drift)
   - Definition of "churn" changes (30 days → 60 days)
   - Business rules updated
   - What constitutes a "good" prediction evolves

3. **Feature Engineering Bugs**
   - Upstream data pipeline changes
   - Feature calculation breaks silently
   - Time-based features stop updating

**Solution: Drift Tests in CI**

```python
# tests/test_model_drift.py
import pytest
from scipy import stats

def test_prediction_distribution_drift():
    """Ensure model predictions haven't drastically changed"""
    
    # Load reference predictions from last known-good model
    reference_preds = load_reference_predictions('test_set_v1.json')
    
    # Generate predictions with current model
    current_model = load_model('artifacts/model.pkl')
    current_preds = current_model.predict(load_test_data())
    
    # Statistical test for distribution shift
    ks_statistic, p_value = stats.ks_2samp(reference_preds, current_preds)
    
    # Fail CI if distributions differ significantly
    assert p_value > 0.01, (
        f"Prediction distribution has drifted! "
        f"KS statistic: {ks_statistic}, p-value: {p_value}"
    )

def test_feature_ranges():
    """Catch feature engineering bugs"""
    data = load_test_data()
    
    # Check expected ranges
    assert data['age'].between(18, 100).all()
    assert data['income'].min() >= 0
    assert data['tenure_months'].between(0, 240).all()
    
def test_model_performance_threshold():
    """Ensure model hasn't regressed"""
    current_model = load_model('artifacts/model.pkl')
    test_data, test_labels = load_holdout_set()
    
    auc = roc_auc_score(test_labels, current_model.predict_proba(test_data)[:, 1])
    
    # Fail if AUC drops below threshold
    assert auc >= 0.78, f"Model AUC {auc} below minimum threshold 0.78"
```

### 3. Practical CI/CD Strategy for ML Projects

**The Pyramid Approach**:

```
                   ┌──────────────┐
                   │ FULL RETRAIN │  ← Nightly/Weekly
                   │  (2 hours)   │     (GPU runners)
                   └──────────────┘
                  /                \
                 /                  \
                /                    \
          ┌──────────────┐    ┌──────────────┐
          │ SMOKE TESTS  │    │ MODEL EVAL   │  ← On PR
          │ (5 min)      │    │ (20 min)     │     (Subset)
          └──────────────┘    └──────────────┘
         /                                    \
        /                                      \
┌──────────────┐                        ┌──────────────┐
│  UNIT TESTS  │                        │  LINT/FORMAT │  ← Every Commit
│  (2 min)     │                        │  (1 min)     │     (Fast!)
└──────────────┘                        └──────────────┘
```

**Example Implementation**:

```yaml
# Optimized ML CI/CD Pipeline
stages:
  # Stage 1: Fast feedback (< 5 minutes)
  - fast_checks:
      - lint
      - unit_tests
      - type_checking
      - smoke_test_training  # 1 epoch, 100 rows
  
  # Stage 2: Validation (< 20 minutes) - Only on PRs
  - validation:
      - integration_tests
      - data_validation
      - mini_training  # 10% data, 10 epochs
      - drift_tests
  
  # Stage 3: Full pipeline (< 2 hours) - Only on main/nightly
  - full_training:
      - train_full_model
      - comprehensive_evaluation
      - model_registration
      - performance_benchmarking
```

---

## Lab / Demo

### Prerequisites

- GitHub account with Actions enabled
- Cloned course repository
- Python 3.9+ installed locally

### Step-by-Step Instructions

```bash
# Step 1: Create a tiered CI configuration
cd ~/mlops-election-project
mkdir -p .github/workflows

# Step 2: Create fast feedback workflow
cat > .github/workflows/fast-checks.yml << 'EOF'
name: Fast Checks
on: [push]
jobs:
  quick-validation:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Lint
        run: pylint src/
      - name: Unit tests
        run: pytest tests/unit/ -v
      - name: Smoke test
        run: python train.py --epochs=1 --rows=100
EOF

# Step 3: Create data validation test
cat > tests/test_data_quality.py << 'EOF'
import pandas as pd
import pytest

def test_training_data_schema():
    """Validate data schema in CI"""
    data = pd.read_csv('data/ci_test_data.csv')
    
    required_columns = ['age', 'income', 'tenure_months', 'label']
    assert all(col in data.columns for col in required_columns)
    
def test_no_missing_critical_features():
    data = pd.read_csv('data/ci_test_data.csv')
    assert data['age'].notna().all()
    assert data['income'].notna().all()

def test_data_ranges():
    data = pd.read_csv('data/ci_test_data.csv')
    assert data['age'].between(18, 120).all()
    assert data['income'].min() >= 0
EOF

# Step 4: Run tests locally
pytest tests/test_data_quality.py -v

# Step 5: Push and watch CI run
git add .
git commit -m "Add tiered ML CI pipeline"
git push
```

### Expected Output

```
Fast Checks Workflow (Completes in ~3 minutes):
✓ Lint (30 seconds)
✓ Unit tests (45 seconds)
✓ Smoke test (90 seconds)

Data Quality Tests:
test_training_data_schema ✓
test_no_missing_critical_features ✓
test_data_ranges ✓

3 passed in 2.1s
```

### Explanation

1. **Fast Feedback Loop**: Runs on every commit, gives results in <5 minutes
2. **Data Quality Gates**: Catches data issues before expensive training
3. **Smoke Test**: Validates end-to-end flow without full training time
4. **Layered Approach**: Save expensive operations for PR review or nightly builds

---

## Common Pitfalls / Gotchas

- ⚠️ **Running Full Training on Every Commit**: Kills productivity. Use tiered approach instead—fast checks on commits, full training nightly.

- ⚠️ **Ignoring Data Quality**: Code tests pass, but garbage data → garbage model. Always validate data schema and distributions in CI.

- ⚠️ **Non-Deterministic Tests**: Using random seeds without fixing them causes flaky tests. Always set `random_state=42` in test code.

- ⚠️ **No Drift Detection**: Model performance can degrade silently. Compare predictions on fixed holdout set to catch regressions.

- ⚠️ **Treating Models Like Binaries**: Models aren't just files—they're code + data + config. Version all three together.

---

## Homework / Practice

1. **Exercise 1**: Add data validation tests to your project
   - Check schema, null values, and value ranges
   - Make tests fail if thresholds violated

2. **Exercise 2**: Implement tiered CI
   - Fast checks (<5 min) on every commit
   - Model validation (<20 min) on PRs
   - Full training (any time) on main branch

3. **Stretch Goal**: Add drift detection
   - Save baseline predictions on holdout set
   - Compare new model predictions statistically
   - Fail CI if distribution differs (p < 0.01)

---

## Quick Quiz

1. **What's the main difference between traditional and ML CI/CD?**
   - A) ML uses Python while web apps use JavaScript
   - B) ML has data as a first-class dependency that can change independently
   - C) ML doesn't need testing
   - D) Traditional CI/CD is faster

   **Answer: B** - Data changes outside your code, making ML CI/CD more complex.

2. **Why run "smoke tests" instead of full training in CI?**
   - A) Smoke tests are more accurate
   - B) To save money on compute
   - C) To get fast feedback (minutes instead of hours)
   - D) Full training isn't possible in CI

   **Answer: C** - Fast feedback keeps developers productive. Full training can run nightly.

3. **True or False: You should retrain your model from scratch on every commit to ensure quality.**

   **Answer: False** - This is too slow. Use smoke tests, cached intermediate results, and train on subsets for CI. Full training can be scheduled or triggered on main branch merges.

---

## Summary

- ML CI/CD is harder than traditional software because of data dependencies, non-determinism, and long training times
- Use a tiered approach: fast checks on every commit, validation on PRs, full training on schedules
- Always validate data quality in CI—bad data breaks models even when code is perfect
- Implement drift detection to catch silent model degradation
- Smart caching and subset training keep feedback loops fast

---

## Next Steps

→ Continue to **Lecture 10.3**: Writing Tests for ML Code (Unit, Integration, Smoke)

---

## Additional Resources

- [Google's "Hidden Technical Debt in Machine Learning Systems"](https://papers.nips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)
- [Martin Fowler on CI](https://martinfowler.com/articles/continuousIntegration.html)
- [GitHub Actions for ML](https://github.com/machine-learning-apps/actions-ml)
- [DVC Pipeline CI/CD](https://dvc.org/doc/use-cases/ci-cd-for-machine-learning)
