# Lecture 1.8 – Sneak Peek: Our End-to-End MLOps Project (What We're Building)

## In This Lecture You Will Learn

- [x] Get an exciting preview of the complete Customer Churn Prediction system
- [x] See the actual code and architecture we'll build together
- [x] Understand how each component connects to create a production-ready system

---

## Real-World Context

> **Story**: Imagine you're starting your first day as an MLOps engineer at a SaaS company. Your manager says, "We lose $200,000 every month to customer churn. Build me a system that predicts which customers are about to leave so we can intervene."
>
> You gulp. Where do you even start?
>
> This project IS that system. By the end of this course, you'll know exactly how to build it, deploy it, and keep it running. Let's take a sneak peek at what we're building.

This isn't a toy project—it's the kind of system you'll build in real companies.

---

## Main Content

### 1. The Business Problem

**Customer Churn Prediction** is one of the most common ML use cases in industry:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CUSTOMER CHURN: THE BUSINESS PROBLEM                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SCENARIO:                                                                   │
│  ─────────                                                                   │
│  • You run a subscription service (SaaS, streaming, telecom, etc.)          │
│  • 5% of customers cancel every month                                        │
│  • Each lost customer = $500/year in revenue                                │
│  • You have 100,000 customers                                               │
│                                                                              │
│  THE MATH:                                                                   │
│  ─────────                                                                   │
│  • 5,000 customers churn monthly                                            │
│  • $500 × 5,000 × 12 months = $30 MILLION lost annually                     │
│                                                                              │
│  THE OPPORTUNITY:                                                            │
│  ────────────────                                                            │
│  • If you could predict churn and intervene...                              │
│  • Retention offers cost ~$50/customer                                       │
│  • Save even 20% of churners = $6M saved annually                           │
│                                                                              │
│  THIS IS WHY ML MATTERS FOR BUSINESS.                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. What Our System Does

```
User Journey with Our System:
═════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  1. DAILY BATCH PREDICTION                                                   │
│     ─────────────────────                                                    │
│     Every morning at 6 AM, our pipeline:                                    │
│     • Pulls latest customer data                                            │
│     • Generates predictions for all active customers                        │
│     • Outputs: "These 347 customers are likely to churn"                    │
│                                                                              │
│  2. REAL-TIME API                                                            │
│     ─────────────                                                            │
│     When a customer calls support:                                          │
│     • Support agent clicks "Check Churn Risk"                               │
│     • API returns: "High risk (78%)"                                        │
│     • Agent offers a retention deal immediately                             │
│                                                                              │
│  3. MONITORING DASHBOARD                                                     │
│     ────────────────────                                                     │
│     Business team sees:                                                      │
│     • Model accuracy over time                                              │
│     • Intervention success rate                                             │
│     • ROI of the ML system                                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. Technical Architecture Preview

Here's what we're building:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 CUSTOMER CHURN PREDICTION SYSTEM                             │
│                     (Final Architecture)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         DATA LAYER                                    │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │   │
│  │  │  Customer   │    │   Feature   │    │    Data     │               │   │
│  │  │  Database   │───▶│ Engineering │───▶│ Validation  │               │   │
│  │  │  (Source)   │    │             │    │             │               │   │
│  │  └─────────────┘    └─────────────┘    └──────┬──────┘               │   │
│  └───────────────────────────────────────────────┼──────────────────────┘   │
│                                                   │                          │
│  ┌───────────────────────────────────────────────┼──────────────────────┐   │
│  │                      TRAINING LAYER            │                      │   │
│  │                                                ▼                      │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │   │
│  │  │  Training   │    │  Experiment │    │   Model     │               │   │
│  │  │  Pipeline   │───▶│  Tracking   │───▶│  Registry   │               │   │
│  │  │  (Automated)│    │  (MLflow)   │    │  (Versions) │               │   │
│  │  └─────────────┘    └─────────────┘    └──────┬──────┘               │   │
│  └───────────────────────────────────────────────┼──────────────────────┘   │
│                                                   │                          │
│  ┌───────────────────────────────────────────────┼──────────────────────┐   │
│  │                      SERVING LAYER             │                      │   │
│  │                                                ▼                      │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │   │
│  │  │   FastAPI   │    │   Docker    │    │ Kubernetes  │               │   │
│  │  │   Server    │───▶│  Container  │───▶│ Deployment  │               │   │
│  │  │ /predict    │    │             │    │ (3 replicas)│               │   │
│  │  └─────────────┘    └─────────────┘    └──────┬──────┘               │   │
│  └───────────────────────────────────────────────┼──────────────────────┘   │
│                                                   │                          │
│  ┌───────────────────────────────────────────────┼──────────────────────┐   │
│  │                    OPERATIONS LAYER            │                      │   │
│  │                                                ▼                      │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │   │
│  │  │   GitHub    │    │ Prometheus  │    │   Alerts    │               │   │
│  │  │  Actions    │    │  + Grafana  │    │  + On-call  │               │   │
│  │  │   CI/CD     │    │ Dashboards  │    │             │               │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘               │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. Code Preview

Let's look at actual code from our project:

#### **Data Loading (Section 5)**

```python
# src/churn_mlops/data/__init__.py

def load_csv(filepath: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    logger.info(f"Loading data from {filepath}")
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df

def validate_data(df: pd.DataFrame, required_columns: list) -> bool:
    """Validate that the dataframe contains required columns."""
    if df.empty:
        raise ValueError("DataFrame is empty")
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True
```

#### **Model Training (Section 7)**

```python
# src/churn_mlops/models/__init__.py

class ChurnModel:
    """Wrapper class for churn prediction models."""
    
    MODEL_TYPES = {
        "logistic_regression": LogisticRegression,
        "random_forest": RandomForestClassifier,
    }
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "ChurnModel":
        """Train the model."""
        logger.info(f"Training model on {len(X)} samples")
        self.feature_names = list(X.columns)
        self.model.fit(X, y)
        self._is_fitted = True
        return self
    
    def predict(self, X) -> np.ndarray:
        """Make predictions."""
        if not self._is_fitted:
            raise ValueError("Model must be fitted before prediction")
        return self.model.predict(X)
    
    def save(self, filepath: str) -> None:
        """Save the model to disk."""
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
```

#### **API Endpoint (Section 7)**

```python
# src/churn_mlops/serving/app.py

@app.post("/predict", response_model=PredictionResponse)
async def predict_single(customer: CustomerFeatures):
    """Make a prediction for a single customer."""
    try:
        predictor = get_predictor()
        features = customer.model_dump()
        result = predictor.predict(features)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### **CI/CD Pipeline (Section 10)**

```yaml
# infra/ci/github-actions-mlops-pipeline.yml

name: MLOps CI/CD Pipeline
on:
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=churn_mlops
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: churn-prediction-api:latest
```

#### **Kubernetes Deployment (Section 11)**

```yaml
# infra/k8s/k8s-manifests.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-prediction-api
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: churn-api
          image: churn-prediction-api:latest
          ports:
            - containerPort: 8000
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
```

### 5. Live Demo Preview

Here's what the running system looks like:

```
API Demo:
═════════

$ curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "tenure": 12,
        "monthly_charges": 65.50,
        "total_charges": 786.00,
        "contract_type": "month-to-month",
        "payment_method": "electronic_check",
        "internet_service": "fiber_optic",
        "tech_support": "no",
        "online_security": "no"
    }'

Response:
{
    "prediction": 1,
    "will_churn": true,
    "churn_probability": 0.78,
    "confidence": 0.78
}

Interpretation:
→ This customer has a 78% probability of churning
→ Short tenure + month-to-month contract + no support = high risk
→ ACTION: Reach out with a retention offer!
```

### 6. What Makes This Production-Grade?

| Aspect | Our Implementation |
|--------|-------------------|
| **Reproducibility** | Git for code, config files for parameters |
| **Testability** | Unit tests, integration tests, API tests |
| **Deployability** | Docker container, Kubernetes manifests |
| **Scalability** | Multiple replicas, load balancing |
| **Monitoring** | Health checks, metrics, logging |
| **Maintainability** | Clear structure, documentation, CI/CD |

---

## Diagrams

```
Project File Structure (Final):
═══════════════════════════════

project/
├── src/
│   └── churn_mlops/          # Python package
│       ├── __init__.py       # Package version, docstring
│       ├── data/             # Data loading & validation
│       │   └── __init__.py   # load_csv, validate_data
│       ├── features/         # Feature engineering
│       │   └── __init__.py   # FeatureEngineer class
│       ├── models/           # Model training & inference
│       │   ├── __init__.py   # ChurnModel class
│       │   ├── train.py      # Training script
│       │   └── inference.py  # ChurnPredictor class
│       ├── serving/          # API layer
│       │   └── app.py        # FastAPI application
│       └── pipelines/        # Orchestration
│           └── __init__.py   # Pipeline definitions
├── tests/                    # Test suite
│   ├── test_api.py
│   ├── test_data.py
│   └── test_models.py
├── config/
│   └── config.yaml           # Configuration
├── notebooks/                # Exploration notebooks
├── models/                   # Saved models (.pkl)
├── Dockerfile                # Container definition
├── docker-compose.yml        # Local orchestration
├── requirements.txt          # Dependencies
└── pyproject.toml            # Package metadata

infra/
├── ci/
│   └── github-actions-mlops-pipeline.yml
└── k8s/
    └── k8s-manifests.yaml
```

---

## Lab / Demo

### Prerequisites

- Course repository cloned
- Python environment ready (we'll set this up in Section 2)

### Step-by-Step Instructions

Let's explore the actual project code:

```bash
# Step 1: Navigate to the project
cd project

# Step 2: See the package structure
echo "=== PACKAGE STRUCTURE ==="
find src -name "*.py" | head -20

# Step 3: Preview the model class
echo ""
echo "=== MODEL CLASS (what we'll build) ==="
head -50 src/churn_mlops/models/__init__.py

# Step 4: Preview the API
echo ""
echo "=== API ENDPOINT (what we'll deploy) ==="
grep -A 15 "@app.post" src/churn_mlops/serving/app.py

# Step 5: Preview the tests
echo ""
echo "=== TESTS (how we ensure quality) ==="
head -30 tests/test_models.py

# Step 6: Preview the CI/CD
echo ""
echo "=== CI/CD PIPELINE (how we automate) ==="
head -40 ../infra/ci/github-actions-mlops-pipeline.yml

# Step 7: Preview Kubernetes
echo ""
echo "=== KUBERNETES (how we deploy) ==="
head -50 ../infra/k8s/k8s-manifests.yaml
```

### Expected Output

```
=== PACKAGE STRUCTURE ===
src/churn_mlops/__init__.py
src/churn_mlops/data/__init__.py
src/churn_mlops/features/__init__.py
src/churn_mlops/models/__init__.py
src/churn_mlops/models/train.py
src/churn_mlops/models/inference.py
src/churn_mlops/serving/__init__.py
src/churn_mlops/serving/app.py
...

=== MODEL CLASS (what we'll build) ===
"""
Models Module
=============
...
```

### Explanation

1. **Package Structure**: Clean separation of concerns (data, features, models, serving)
2. **Model Class**: Reusable, testable, saveable model wrapper
3. **API Endpoint**: Production-ready FastAPI with validation
4. **Tests**: Comprehensive test coverage
5. **CI/CD**: Automated testing and deployment
6. **Kubernetes**: Production deployment configuration

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Getting intimidated by the final system. Remember: we build this incrementally, one piece at a time. By Section 14, it will all make sense.

- ⚠️ **Pitfall 2**: Trying to understand everything now. This is a preview, not a deep dive. Each component gets its own detailed section.

- ⚠️ **Pitfall 3**: Thinking "I could never build this." Yes, you can. We'll do it together, step by step.

---

## Homework / Practice

1. **Exercise 1**: Explore the `project/` directory. Count how many Python files exist. List the top-level modules.

2. **Exercise 2**: Read the README.md in the project folder. What technologies does it mention?

3. **Stretch Goal**: Try to understand one function in `src/churn_mlops/data/__init__.py`. What does `load_csv()` do? Why does it log messages?

---

## Quick Quiz

1. **What business problem does our project solve?**
   - A) Detecting fraudulent transactions
   - B) Predicting which customers will cancel their subscription
   - C) Recommending products to customers
   - D) Classifying customer support tickets

2. **What framework do we use to build the prediction API?**
   - A) Flask
   - B) Django
   - C) FastAPI
   - D) Express.js

3. **True or False: Our project uses Docker and Kubernetes for deployment.**

<details>
<summary>Answers</summary>

1. **B** - Customer churn prediction helps retain at-risk customers
2. **C** - FastAPI provides modern, fast, auto-documented APIs
3. **True** - Docker for containerization, Kubernetes for orchestration

</details>

---

## Summary

- We're building a Customer Churn Prediction system—a common, valuable ML use case
- The system includes: data loading, training, API serving, and monitoring
- All code is production-grade: tested, documented, containerized, automated
- The project structure follows software engineering best practices
- Don't worry if it seems complex—we build it piece by piece over 15 sections

---

## Next Steps

🎉 **Congratulations! You've completed Section 1!**

→ Continue to **Section 2, Lecture 2.1**: Skills You Need (and Don't Need) Before Starting

Before moving on:
- [ ] Take the Section 1 Quiz in `/quizzes/section-01-quiz.md`
- [ ] Review any lectures where you scored below 80%
- [ ] Get excited—you're about to start building!

---

## Additional Resources

- [project/README.md](../../project/README.md) - Full project documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Framework we use for APIs
- [Docker Getting Started](https://docs.docker.com/get-started/) - Container fundamentals
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/) - Orchestration fundamentals
