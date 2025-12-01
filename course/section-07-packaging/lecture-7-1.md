# Lecture 7.1 – Turning Training Code into a Re-usable Python Package

## In This Lecture You Will Learn

- [x] Transform ML scripts into a properly structured Python package
- [x] Implement best practices for package organization, imports, and versioning
- [x] Create reusable, testable, and maintainable ML code

---

## Real-World Context

> **Story**: A data scientist at a healthcare startup built a great disease prediction model. It worked perfectly on her laptop. Then came the request: "Can we use this model in three other services?" She emailed the Jupyter notebook. Three teams each made their own copy, modified it, and within months there were five incompatible versions with no clear source of truth.
>
> If she had packaged the model properly from the start, all teams could have simply run `pip install disease-predictor` and imported from a single, maintained version.

Packaging is how you go from "one person's code" to "code everyone can use."

---

## Main Content

### 1. Why Package Your ML Code?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BENEFITS OF PROPER PACKAGING                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  WITHOUT PACKAGING                  │  WITH PACKAGING                       │
│  ─────────────────                  │  ──────────────                       │
│                                     │                                        │
│  • Copy-paste code between          │  • pip install my_package             │
│    projects                         │                                        │
│                                     │                                        │
│  • "Which version is this?"         │  • from my_package import Model       │
│                                     │    print(my_package.__version__)       │
│                                     │                                        │
│  • Broken imports when moving       │  • Imports work from anywhere         │
│    files                            │                                        │
│                                     │                                        │
│  • Untestable monolithic scripts    │  • Each module testable independently │
│                                     │                                        │
│  • No dependency management         │  • requirements.txt / pyproject.toml  │
│                                     │                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Package Structure Deep Dive

Our `churn_mlops` package:

```
project/
├── src/                          # Source root
│   └── churn_mlops/             # Package directory
│       ├── __init__.py          # Package initialization
│       ├── data/                # Data module
│       │   └── __init__.py
│       ├── features/            # Features module
│       │   └── __init__.py
│       ├── models/              # Models module
│       │   ├── __init__.py      # ChurnModel class
│       │   ├── train.py         # Training script
│       │   └── inference.py     # Inference class
│       ├── serving/             # API module
│       │   ├── __init__.py
│       │   └── app.py           # FastAPI app
│       └── pipelines/           # Pipeline module
│           └── __init__.py
├── pyproject.toml               # Package configuration
├── setup.py                     # (Optional) Legacy setup
└── requirements.txt             # Dependencies
```

### 3. The `__init__.py` Files

Each `__init__.py` controls what's exposed from that module:

```python
# src/churn_mlops/__init__.py
"""
Churn MLOps Package
===================

A production-ready Customer Churn Prediction system.

Example usage:
    from churn_mlops.models import ChurnModel
    from churn_mlops.data import generate_sample_data
    
    data = generate_sample_data(1000)
    model = ChurnModel(model_type="random_forest")
    model.fit(X, y)
"""

__version__ = "0.1.0"
__author__ = "MLOps Course"

# Expose key classes at package level (optional)
from churn_mlops.models import ChurnModel
from churn_mlops.data import generate_sample_data, validate_data
```

```python
# src/churn_mlops/models/__init__.py
"""
Models Module
=============

Training and inference for churn prediction models.
"""

from churn_mlops.models.inference import ChurnPredictor
import pickle
import logging
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)

logger = logging.getLogger(__name__)


class ChurnModel:
    """
    Wrapper class for churn prediction models.
    
    This class provides a consistent interface for different model types,
    with built-in methods for training, prediction, evaluation, and persistence.
    
    Example:
        >>> model = ChurnModel(model_type="random_forest", n_estimators=100)
        >>> model.fit(X_train, y_train)
        >>> predictions = model.predict(X_test)
        >>> metrics = model.evaluate(X_test, y_test)
        >>> model.save("models/churn_model.pkl")
    """
    
    MODEL_TYPES = {
        "logistic_regression": LogisticRegression,
        "random_forest": RandomForestClassifier,
    }
    
    def __init__(self, model_type: str = "random_forest", **kwargs):
        """Initialize the model with specified type and parameters."""
        if model_type not in self.MODEL_TYPES:
            raise ValueError(f"Unknown model type: {model_type}")
        
        self.model_type = model_type
        self.params = kwargs
        self.model = self.MODEL_TYPES[model_type](**kwargs)
        self._is_fitted = False
        self.feature_names = None
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> "ChurnModel":
        """Train the model on the provided data."""
        logger.info(f"Training {self.model_type} on {len(X)} samples")
        self.feature_names = list(X.columns) if isinstance(X, pd.DataFrame) else None
        self.model.fit(X, y)
        self._is_fitted = True
        return self
    
    def predict(self, X) -> np.ndarray:
        """Make predictions."""
        if not self._is_fitted:
            raise ValueError("Model must be fitted before prediction")
        return self.model.predict(X)
    
    def predict_proba(self, X) -> np.ndarray:
        """Get prediction probabilities."""
        if not self._is_fitted:
            raise ValueError("Model must be fitted before prediction")
        return self.model.predict_proba(X)
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Evaluate model performance with standard metrics."""
        y_pred = self.predict(X)
        y_proba = self.predict_proba(X)[:, 1]
        
        return {
            "accuracy": accuracy_score(y, y_pred),
            "precision": precision_score(y, y_pred),
            "recall": recall_score(y, y_pred),
            "f1": f1_score(y, y_pred),
            "roc_auc": roc_auc_score(y, y_proba),
        }
    
    def save(self, filepath: str) -> None:
        """Save model to disk."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> "ChurnModel":
        """Load model from disk."""
        with open(filepath, "rb") as f:
            return pickle.load(f)


def train_model(
    X_train, y_train, X_test, y_test,
    model_type: str = "random_forest", **params
) -> Tuple[ChurnModel, Dict[str, float]]:
    """
    Convenience function to train and evaluate a model.
    
    Returns:
        Tuple of (trained model, evaluation metrics)
    """
    model = ChurnModel(model_type=model_type, **params)
    model.fit(X_train, y_train)
    metrics = model.evaluate(X_test, y_test)
    return model, metrics


# Make key classes available at module level
__all__ = ["ChurnModel", "train_model", "ChurnPredictor"]
```

### 4. Package Configuration with `pyproject.toml`

Modern Python packaging uses `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "churn_mlops"
version = "0.1.0"
description = "Customer Churn Prediction MLOps Project"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "MLOps Course", email = "mlops@example.com"}
]
requires-python = ">=3.9"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "numpy>=1.21.0,<2.0.0",
    "pandas>=1.3.0,<3.0.0",
    "scikit-learn>=1.0.0,<2.0.0",
    "pyyaml>=5.4.0,<7.0.0",
]

[project.optional-dependencies]
api = [
    "fastapi>=0.68.0,<1.0.0",
    "uvicorn[standard]>=0.15.0,<1.0.0",
    "pydantic>=2.0.0,<3.0.0",
]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=3.0.0",
    "black>=22.0.0",
    "flake8>=4.0.0",
]

[project.scripts]
churn-train = "churn_mlops.models.train:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"

[tool.black]
line-length = 100
target-version = ['py39']
```

### 5. Installing Your Package

```bash
# Install in development mode (editable)
# Changes to source code immediately reflected
pip install -e .

# Install with optional dependencies
pip install -e ".[api,dev]"

# Install for production (non-editable)
pip install .

# Now you can import from anywhere:
python -c "from churn_mlops.models import ChurnModel; print('Success!')"
```

### 6. Package Design Principles

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PYTHON PACKAGE DESIGN PRINCIPLES                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1️⃣  SINGLE RESPONSIBILITY                                                  │
│      Each module should do one thing well                                   │
│      data/ → loading, features/ → engineering, models/ → training          │
│                                                                              │
│  2️⃣  EXPLICIT IMPORTS                                                       │
│      Use __all__ to control what's exported                                 │
│      Users should know exactly what's public API                            │
│                                                                              │
│  3️⃣  SENSIBLE DEFAULTS                                                      │
│      model = ChurnModel()  # Works out of the box                           │
│      model = ChurnModel(n_estimators=200)  # Customizable                   │
│                                                                              │
│  4️⃣  FAIL FAST WITH CLEAR ERRORS                                           │
│      if not self._is_fitted:                                                │
│          raise ValueError("Model must be fitted before prediction")         │
│                                                                              │
│  5️⃣  DOCUMENT EVERYTHING                                                    │
│      Docstrings, type hints, examples                                       │
│      Users shouldn't need to read source code                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrams

```
Import Resolution Flow:
═══════════════════════

from churn_mlops.models import ChurnModel

        ┌─────────────────────────────────────────────┐
        │  Python looks for 'churn_mlops' package    │
        └─────────────────┬───────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────┐
        │  Found in src/churn_mlops/__init__.py      │
        │  (because we did pip install -e .)         │
        └─────────────────┬───────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────┐
        │  Navigate to .models submodule             │
        │  src/churn_mlops/models/__init__.py        │
        └─────────────────┬───────────────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────────────┐
        │  Import ChurnModel class                    │
        │  (defined in models/__init__.py)           │
        └─────────────────────────────────────────────┘
```

---

## Lab / Demo

### Prerequisites

- Completed Sections 1-6
- Python environment set up

### Step-by-Step Instructions

```bash
# Step 1: Navigate to project
cd project

# Step 2: Install package in development mode
pip install -e ".[dev]"

# Step 3: Verify installation
python -c "
import churn_mlops
print(f'Package version: {churn_mlops.__version__}')

from churn_mlops.data import generate_sample_data, validate_data
from churn_mlops.features import FeatureEngineer
from churn_mlops.models import ChurnModel, train_model

print('✅ All imports successful!')
"

# Step 4: Test the model class
python -c "
from churn_mlops.data import generate_sample_data
from churn_mlops.models import ChurnModel, train_model
from sklearn.model_selection import train_test_split

# Generate sample data
df = generate_sample_data(1000)
X = df[['tenure', 'monthly_charges', 'total_charges']]
y = df['churn']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train using the package
model, metrics = train_model(X_train, y_train, X_test, y_test)

print('Model trained successfully!')
print(f'Accuracy: {metrics[\"accuracy\"]:.3f}')
print(f'F1 Score: {metrics[\"f1\"]:.3f}')
"

# Step 5: Run package tests
PYTHONPATH=src pytest tests/test_models.py -v
```

### Expected Output

```
$ python -c "import churn_mlops..."
Package version: 0.1.0
✅ All imports successful!

$ python -c "from churn_mlops.data..."
Model trained successfully!
Accuracy: 0.735
F1 Score: 0.542

$ pytest tests/test_models.py -v
============================= test session starts =============================
tests/test_models.py::TestChurnModel::test_init_random_forest PASSED
tests/test_models.py::TestChurnModel::test_fit PASSED
tests/test_models.py::TestChurnModel::test_predict PASSED
tests/test_models.py::TestChurnModel::test_save_and_load PASSED
...
============================= 10 passed in 1.54s ==============================
```

### Explanation

1. **Editable install**: Changes to code immediately work without reinstall
2. **Import verification**: Confirms package structure is correct
3. **End-to-end test**: Uses the package like a real user would
4. **Unit tests**: Validates each component works correctly

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Forgetting to reinstall after changing `pyproject.toml`. After changing package metadata, run `pip install -e .` again.

- ⚠️ **Pitfall 2**: Circular imports. If `models` imports from `data` and `data` imports from `models`, you'll get errors. Design one-way dependencies.

- ⚠️ **Pitfall 3**: Not using `src/` layout. Without `src/`, you might accidentally import from the local directory instead of the installed package.

---

## Homework / Practice

1. **Exercise 1**: Add a `__repr__` method to `ChurnModel` that shows model type and whether it's fitted.

2. **Exercise 2**: Create a new submodule `churn_mlops.utils` with a `timing` decorator that logs how long a function takes.

3. **Stretch Goal**: Add type hints to all public methods in `ChurnModel` and run `mypy` to check them.

---

## Quick Quiz

1. **What does `pip install -e .` do?**
   - A) Installs the package in a virtual environment
   - B) Installs the package in "editable" mode so changes reflect immediately
   - C) Installs all dependencies
   - D) Creates an executable

2. **What file controls modern Python package configuration?**
   - A) setup.py only
   - B) requirements.txt
   - C) pyproject.toml
   - D) __init__.py

3. **True or False: Every Python package directory needs an `__init__.py` file.**

<details>
<summary>Answers</summary>

1. **B** - Editable install creates a link to your source, so changes work immediately
2. **C** - `pyproject.toml` is the modern standard; `setup.py` is legacy
3. **True** - `__init__.py` marks a directory as a Python package

</details>

---

## Summary

- Python packages enable code reuse, versioning, and proper imports
- Use `src/` layout to avoid import confusion
- `__init__.py` files control what each module exports
- `pyproject.toml` is the modern way to configure packages
- Install in editable mode during development: `pip install -e .`
- Follow design principles: single responsibility, explicit imports, sensible defaults

---

## Next Steps

→ Continue to **Lecture 7.2**: Writing a Clean Inference Function (predict())

---

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/) - Official documentation
- [pyproject.toml Reference](https://peps.python.org/pep-0621/) - PEP 621 specification
- [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) - Best practices guide
