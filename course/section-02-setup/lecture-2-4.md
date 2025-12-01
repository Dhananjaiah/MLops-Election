# Lecture 2.4 – Project Structure for an MLOps Course Project

## In This Lecture You Will Learn

- [x] Understand the standard project structure for production ML projects
- [x] Know the purpose of each directory and file in our project
- [x] Apply software engineering best practices to ML code organization

---

## Real-World Context

> **Story**: A machine learning consultant was hired to audit a company's ML codebase. What he found: 47 Jupyter notebooks in a folder called "models", no documentation, files named `final_model_v2_FINAL_use_this.py`, and critical business logic buried in a notebook cell that hadn't been run in months.
>
> Six months later, after restructuring, the same team could onboard new members in days instead of weeks, and deploy models in hours instead of months. Structure matters.

A well-organized project is easier to understand, test, deploy, and maintain.

---

## Main Content

### 1. The Production ML Project Structure

Here's our project structure, which follows industry best practices:

```
project/
├── src/                          # Source code (the actual package)
│   └── churn_mlops/             # Main Python package
│       ├── __init__.py          # Package initialization
│       ├── data/                # Data loading and validation
│       │   └── __init__.py
│       ├── features/            # Feature engineering
│       │   └── __init__.py
│       ├── models/              # Model training and inference
│       │   ├── __init__.py
│       │   ├── train.py         # Training script
│       │   └── inference.py     # Inference wrapper
│       ├── serving/             # API layer
│       │   ├── __init__.py
│       │   └── app.py           # FastAPI application
│       └── pipelines/           # Orchestration (future)
│           └── __init__.py
├── tests/                       # Test files (mirrors src structure)
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_models.py
│   └── test_api.py
├── config/                      # Configuration files
│   └── config.yaml
├── notebooks/                   # Jupyter notebooks (exploration only)
│   └── exploration_notebook_template.ipynb
├── models/                      # Saved model artifacts
│   └── .gitkeep
├── data/                        # Data files (usually gitignored)
│   ├── raw/
│   └── processed/
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Multi-container orchestration
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Package metadata
└── README.md                    # Project documentation
```

### 2. Directory-by-Directory Explanation

#### **`src/churn_mlops/` - The Main Package**

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOURCE CODE ORGANIZATION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  src/churn_mlops/                                               │
│  ├── __init__.py      # Exposes package version and key classes│
│  │                                                               │
│  ├── data/            # DATA LAYER                              │
│  │   └── __init__.py  # load_csv(), validate_data(),           │
│  │                    # generate_sample_data()                  │
│  │                                                               │
│  ├── features/        # FEATURE LAYER                           │
│  │   └── __init__.py  # FeatureEngineer class,                 │
│  │                    # create_derived_features(),             │
│  │                    # handle_missing_values()                │
│  │                                                               │
│  ├── models/          # MODEL LAYER                             │
│  │   ├── __init__.py  # ChurnModel class, train_model()        │
│  │   ├── train.py     # CLI training script                    │
│  │   └── inference.py # ChurnPredictor class for serving       │
│  │                                                               │
│  ├── serving/         # API LAYER                               │
│  │   ├── __init__.py  #                                        │
│  │   └── app.py       # FastAPI app with /predict endpoint     │
│  │                                                               │
│  └── pipelines/       # ORCHESTRATION LAYER (future)           │
│      └── __init__.py  # Will contain pipeline definitions      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Why this structure?**
- **Separation of concerns**: Each module has one responsibility
- **Testability**: Each module can be tested independently
- **Reusability**: Import `from churn_mlops.models import ChurnModel`
- **Maintainability**: Easy to find and modify code

#### **`tests/` - Test Files**

```python
# tests/ mirrors src/ structure
tests/
├── __init__.py
├── test_data.py       # Tests for data/ module
├── test_models.py     # Tests for models/ module
└── test_api.py        # Tests for serving/ module

# This makes it easy to:
# - Find tests for a specific module
# - Run tests for just one component
# - Ensure every module has coverage
```

#### **`config/` - Configuration Files**

Configuration should be separate from code:

```yaml
# config/config.yaml
model:
  type: random_forest
  params:
    n_estimators: 100
    max_depth: 10

data:
  test_size: 0.2
  random_state: 42

api:
  host: 0.0.0.0
  port: 8000
```

**Why separate config?**
- Change behavior without changing code
- Different configs for dev/staging/production
- Easy to audit what parameters were used

#### **`notebooks/` - Exploration Only**

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOTEBOOK RULES                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ DO use notebooks for:                                       │
│     • Initial data exploration                                  │
│     • Visualization experiments                                 │
│     • Quick prototyping                                         │
│     • Documenting analysis results                              │
│                                                                  │
│  ❌ DON'T use notebooks for:                                    │
│     • Production model training                                 │
│     • Code that needs to run automatically                      │
│     • Anything deployed to production                           │
│     • Code reviewed by teammates                                │
│                                                                  │
│  RULE: "If it needs to run twice, move it to src/"            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Key Files Explained

#### **`requirements.txt`**

```txt
# Pin major versions for reproducibility
numpy>=1.21.0,<2.0.0
pandas>=1.3.0,<3.0.0
scikit-learn>=1.0.0,<2.0.0
fastapi>=0.68.0,<1.0.0
uvicorn[standard]>=0.15.0,<1.0.0
pydantic>=2.0.0,<3.0.0
pyyaml>=5.4.0,<7.0.0

# Testing
pytest>=7.0.0
pytest-cov>=3.0.0
```

**Best practices:**
- Pin major versions (`>=1.0,<2.0`) for stability
- Separate dev dependencies if needed
- Comment purpose of unusual packages

#### **`pyproject.toml`**

Modern Python packaging configuration:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "churn_mlops"
version = "0.1.0"
description = "Customer Churn Prediction MLOps Project"
requires-python = ">=3.9"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
```

#### **`Dockerfile`**

Container definition for deployment:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY config/ ./config/
EXPOSE 8000
CMD ["uvicorn", "churn_mlops.serving.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Anti-Patterns to Avoid

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT STRUCTURE ANTI-PATTERNS               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ BAD: Flat structure                                         │
│  my_project/                                                     │
│  ├── train.py                                                   │
│  ├── model.py                                                   │
│  ├── utils.py                                                   │
│  ├── helpers.py                                                 │
│  └── more_utils.py                                              │
│  → Problem: No clear organization, hard to navigate             │
│                                                                  │
│  ❌ BAD: Version numbers in filenames                           │
│  models/                                                         │
│  ├── model_v1.py                                                │
│  ├── model_v2_final.py                                          │
│  └── model_v2_final_REAL.py                                     │
│  → Problem: Use Git for versioning!                             │
│                                                                  │
│  ❌ BAD: Notebooks as production code                           │
│  src/                                                            │
│  └── train_model.ipynb  # Runs via papermill in production     │
│  → Problem: Notebooks are hard to test, review, debug           │
│                                                                  │
│  ❌ BAD: Mixing concerns                                        │
│  src/model.py                                                    │
│  # Contains: data loading, feature eng, training, API, logging │
│  → Problem: 2000 lines, impossible to test or maintain         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Diagrams

```
Data Flow Through Project Structure:
════════════════════════════════════

                     ┌───────────────┐
                     │  Raw Data     │
                     │  (data/raw/)  │
                     └───────┬───────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     src/churn_mlops/                             │
│                                                                  │
│  ┌──────────────┐                                               │
│  │    data/     │  ← Load & Validate                            │
│  │  __init__.py │                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │  features/   │  ← Transform & Engineer                       │
│  │  __init__.py │                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐      ┌──────────────┐                        │
│  │   models/    │ ───▶ │   models/    │  ← Save                │
│  │   train.py   │      │ churn_model  │   (models/)            │
│  └──────────────┘      │    .pkl      │                        │
│         │              └──────────────┘                        │
│         ▼                     │                                 │
│  ┌──────────────┐            │                                 │
│  │  serving/    │ ◀──────────┘  ← Load                         │
│  │   app.py     │                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
└─────────┼────────────────────────────────────────────────────────┘
          │
          ▼
    ┌───────────┐
    │  /predict │
    │   API     │
    └───────────┘
```

---

## Lab / Demo

### Prerequisites

- Environment set up from Lecture 2.3
- Course repository cloned

### Step-by-Step Instructions

```bash
# Step 1: Navigate to project and explore structure
cd project
find . -type f -name "*.py" | head -20

# Step 2: Understand module imports
python3 -c "
# This shows how our package structure enables clean imports
from churn_mlops.data import load_csv, validate_data, generate_sample_data
from churn_mlops.features import FeatureEngineer, create_derived_features
from churn_mlops.models import ChurnModel, train_model
from churn_mlops.serving.app import app

print('✅ All imports work!')
print()
print('Available in data module:', dir())
"

# Step 3: See how tests mirror source structure
echo "=== Source Structure ==="
ls -la src/churn_mlops/

echo ""
echo "=== Test Structure ==="
ls -la tests/

# Step 4: Run tests for a specific module
PYTHONPATH=src pytest tests/test_data.py -v

# Step 5: Check configuration
cat config/config.yaml
```

### Expected Output

```
=== Source Structure ===
total 8
drwxr-xr-x  8 user  staff  256 Jan 15 10:30 .
drwxr-xr-x  3 user  staff   96 Jan 15 10:30 ..
-rw-r--r--  1 user  staff  358 Jan 15 10:30 __init__.py
drwxr-xr-x  3 user  staff   96 Jan 15 10:30 data
drwxr-xr-x  3 user  staff   96 Jan 15 10:30 features
drwxr-xr-x  5 user  staff  160 Jan 15 10:30 models
drwxr-xr-x  3 user  staff   96 Jan 15 10:30 pipelines
drwxr-xr-x  4 user  staff  128 Jan 15 10:30 serving

=== Test Structure ===
total 24
-rw-r--r--  1 user  staff  1234 Jan 15 10:30 test_api.py
-rw-r--r--  1 user  staff  1567 Jan 15 10:30 test_data.py
-rw-r--r--  1 user  staff  3456 Jan 15 10:30 test_models.py
```

### Explanation

1. **Source structure**: Clear separation of concerns by module
2. **Import check**: Verifies package is properly installed
3. **Test structure**: Tests mirror source for easy navigation
4. **Module tests**: Can test components independently
5. **Configuration**: External config for flexibility

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Missing `__init__.py` files. Every directory that should be importable needs an `__init__.py`, even if it's empty.

- ⚠️ **Pitfall 2**: Circular imports. If module A imports from B and B imports from A, you'll get errors. Design your dependency direction carefully.

- ⚠️ **Pitfall 3**: Hardcoding paths. Use `pathlib.Path` and relative paths, not `/Users/myname/project/data/file.csv`.

---

## Homework / Practice

1. **Exercise 1**: Draw the import dependency graph for our project. Which modules depend on which?

2. **Exercise 2**: Add a new module `src/churn_mlops/utils/__init__.py` with a function `get_project_root()` that returns the project root path.

3. **Stretch Goal**: Create a `src/churn_mlops/config.py` module that loads `config/config.yaml` and exposes settings as a Python object.

---

## Quick Quiz

1. **Where should production model training code live?**
   - A) `notebooks/`
   - B) `src/churn_mlops/models/`
   - C) `scripts/`
   - D) `models/`

2. **What is the purpose of `__init__.py` files?**
   - A) Initialize variables
   - B) Make directories importable as Python packages
   - C) Run at startup
   - D) Store configuration

3. **True or False: Notebooks are appropriate for production model training.**

<details>
<summary>Answers</summary>

1. **B** - Production code lives in `src/` package
2. **B** - `__init__.py` marks directories as Python packages
3. **False** - Notebooks are for exploration; production code goes in `.py` files

</details>

---

## Summary

- Use a clear directory structure: `src/`, `tests/`, `config/`, `notebooks/`
- Separate concerns: data, features, models, serving in different modules
- Tests should mirror source structure for easy navigation
- Keep configuration external from code
- Notebooks for exploration only; production code in `.py` files
- Avoid anti-patterns: flat structure, version numbers in filenames, notebooks in production

---

## Next Steps

→ Continue to **Lecture 2.5**: Installing Required Python Packages & Virtual Environments

---

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/) - Official packaging docs
- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) - Popular ML project template
- [Real Python Project Structure](https://realpython.com/python-application-layouts/) - Best practices guide
