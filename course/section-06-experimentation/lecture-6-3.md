# Lecture 6.3 – Structuring Experiments (Folders, Scripts, Configs)

## In This Lecture You Will Learn

- [x] Organize ML experiments with proper folder structure
- [x] Separate concerns (data, features, models, configs)
- [x] Use configuration files to make experiments reproducible

---

## Real-World Context

> **Story**: Lisa's team had 47 experiment folders: `churn_final`, `churn_final_v2`, `churn_REALLY_final`, `churn_jan15_test`, `churn_production_candidate`... Nobody knew which was which. When the CEO asked "Which model are we using?" it took 3 days to figure out. Then they adopted a standard structure: date-based folders, config files for every run, README for each experiment. Finding experiments went from hours to seconds. Organization isn't glamorous, but it's the difference between chaos and productivity.

In the real world, poor organization kills more ML projects than bad algorithms. A well-structured experiment setup enables fast iteration, easy comparison, and painless handoffs.

---

## Main Content

### 1. Standard ML Project Structure

```
project/
├── data/
│   ├── raw/                    # Original, immutable data
│   ├── processed/              # Cleaned, transformed data
│   └── features/               # Engineered features
│
├── notebooks/
│   ├── 01_exploration.ipynb   # EDA, initial analysis
│   ├── 02_modeling.ipynb      # Prototyping models
│   └── README.md              # Index of notebooks
│
├── src/                        # Source code (not notebooks!)
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── make_dataset.py    # Data loading functions
│   ├── features/
│   │   ├── __init__.py
│   │   └── build_features.py  # Feature engineering
│   └── models/
│       ├── __init__.py
│       ├── train_model.py     # Training logic
│       └── predict_model.py   # Inference logic
│
├── models/                     # Trained model artifacts
│   ├── 2024-01-15_rf_v1/
│   │   ├── model.pkl
│   │   ├── config.yaml
│   │   ├── metrics.json
│   │   └── README.md
│   └── 2024-01-20_xgb_v2/
│
├── experiments/                # Experiment tracking
│   ├── 2024-01-15_baseline/
│   │   ├── config.yaml
│   │   ├── results.json
│   │   └── notes.md
│   └── 2024-01-20_feature_eng/
│
├── tests/                      # Unit tests
│   ├── test_data.py
│   ├── test_features.py
│   └── test_models.py
│
├── config/                     # Configuration files
│   ├── default.yaml           # Default parameters
│   ├── experiment1.yaml       # Experiment-specific
│   └── production.yaml        # Production config
│
├── requirements.txt            # Python dependencies
├── setup.py                    # Make project pip-installable
├── README.md                   # Project documentation
└── Makefile                    # Common commands

```

### 2. Configuration-Driven Experiments

**Why Config Files?**
- Parameters in code = hard to track what changed
- Config files = clear history of all experiments
- Easy to run same experiment with different params

**Example config.yaml**:
```yaml
# config/experiment_2024-01-15.yaml
experiment:
  name: "churn_rf_baseline"
  date: "2024-01-15"
  author: "lisa@company.com"
  description: "Baseline Random Forest with default params"

data:
  train: "data/processed/train_2024-01-01.parquet"
  val: "data/processed/val_2024-01-01.parquet"
  test: "data/processed/test_2024-01-01.parquet"

features:
  - customer_id
  - tenure_months
  - monthly_charges
  - total_charges
  - contract_type
  - payment_method

model:
  type: "RandomForestClassifier"
  params:
    n_estimators: 100
    max_depth: 10
    min_samples_split: 5
    random_state: 42

training:
  batch_size: null  # Not applicable for RF
  epochs: null
  validation_split: 0.2
  
output:
  model_path: "models/2024-01-15_rf_v1/"
  metrics_path: "experiments/2024-01-15_baseline/metrics.json"
```

### 3. Experiment Naming Conventions

**Good Naming**:
- `2024-01-15_rf_baseline` - Date + model + purpose
- `2024-01-20_xgb_feature_eng_v2` - Clear what changed
- `2024-02-01_final_production_candidate` - Intent clear

**Bad Naming**:
- `experiment1`, `test`, `final`, `final_v2`, `final_REALLY`
- No dates, no context, unusable

**Folder Naming Pattern**:
```
YYYY-MM-DD_model-type_description/
  ├── config.yaml      # All parameters
  ├── results.json     # Metrics
  ├── model.pkl        # Trained model
  └── README.md        # Notes, insights, next steps
```

### 4. Separation of Concerns

**Principle**: Each file/module has ONE job

**data/make_dataset.py**: Load and clean data only
```python
def load_raw_data(path):
    return pd.read_csv(path)

def clean_data(df):
    df = df.dropna()
    df = df[df['age'] > 0]
    return df
```

**features/build_features.py**: Feature engineering only
```python
def engineer_temporal_features(df):
    df['days_since_signup'] = (pd.Timestamp.now() - df['signup_date']).dt.days
    return df
```

**models/train_model.py**: Training logic only
```python
def train_model(X, y, config):
    model = RandomForestClassifier(**config['model']['params'])
    model.fit(X, y)
    return model
```

**scripts/run_experiment.py**: Orchestration only
```python
def main(config_path):
    config = load_config(config_path)
    data = load_raw_data(config['data']['train'])
    data = clean_data(data)
    features = engineer_features(data)
    model = train_model(features, config)
    metrics = evaluate_model(model, val_data)
    save_results(model, metrics, config)
```

---

## Diagrams

```
┌──────────────────────────────────────────────────────────────────┐
│              Well-Structured ML Project                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  📂 project/                                                     │
│  ├── 📊 data/            (raw, processed, features)            │
│  ├── 📓 notebooks/       (exploration only)                     │
│  ├── 💻 src/             (production code)                      │
│  │   ├── data/          (load & clean)                          │
│  │   ├── features/      (engineer)                              │
│  │   └── models/        (train & predict)                       │
│  ├── 🤖 models/          (saved artifacts + configs)            │
│  │   └── 2024-01-15_rf_v1/                                      │
│  │       ├── model.pkl                                          │
│  │       ├── config.yaml                                        │
│  │       └── metrics.json                                       │
│  ├── 🔬 experiments/     (experiment tracking)                  │
│  ├── ⚙️  config/          (parameter files)                      │
│  └── ✅ tests/           (unit tests)                            │
│                                                                   │
│  Every piece has its place. Easy to navigate and maintain.      │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-6-3-diagram.png)

> Diagram shows organized project structure with clear separation of concerns

---

## Lab / Demo

### Prerequisites

- Completed Lectures 6.1-6.2
- Cookiecutter installed (optional)

### Step-by-Step Instructions

```bash
# Step 1: Create project structure
cd project
mkdir -p data/{raw,processed,features} src/{data,features,models} models experiments config tests

# Step 2: Create a sample config file
cat > config/baseline.yaml << EOF
experiment:
  name: baseline_rf
  date: $(date +%Y-%m-%d)

model:
  type: RandomForestClassifier
  params:
    n_estimators: 100
    random_state: 42
EOF

# Step 3: Create training script
cat > src/models/train_model.py << 'EOF'
import yaml
import pickle
from sklearn.ensemble import RandomForestClassifier

def train(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    model = RandomForestClassifier(**config['model']['params'])
    # Training logic here
    return model

if __name__ == '__main__':
    import sys
    train(sys.argv[1])
EOF

# Step 4: Run experiment
python src/models/train_model.py config/baseline.yaml
```

### Expected Output

```
Project Structure Created:
data/
  raw/
  processed/
  features/
src/
  data/
  features/
  models/
    train_model.py ✓
models/
experiments/
config/
  baseline.yaml ✓
tests/

Training:
Loading config: config/baseline.yaml
Experiment: baseline_rf
Date: 2024-01-15
Training Random Forest with n_estimators=100...
Model saved to: models/2024-01-15_baseline_rf/
```

### Explanation

1. **Step 1**: Set up organized folder structure
2. **Step 2**: Create config file (all parameters documented)
3. **Step 3**: Write modular training code
4. **Step 4**: Run experiment using config (fully reproducible)

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Over-organizing too early. Don't create 20 folders on day 1. Grow structure as project grows.

- ⚠️ **Pitfall 2**: Mixing code and data. Never commit data to Git. Use `.gitignore` for data folders.

- ⚠️ **Pitfall 3**: Hard-coding paths. Use relative paths or config files. `../../data/file.csv` breaks when shared.

---

## Homework / Practice

1. **Exercise 1**: Take your current ML project (or create a toy one). Reorganize it using the structure from this lecture. Time: 1 hour.

2. **Exercise 2**: Create a config file for 3 different experiments: baseline, feature engineering, hyperparameter tuning. Run all 3 and compare results.

3. **Stretch Goal**: Use Cookiecutter Data Science template to scaffold a new project. Explore how professionals structure ML projects.

---

## Quick Quiz

1. **Why use config files instead of hard-coding parameters?**
   - A) Config files run faster
   - B) Makes experiments reproducible and trackable
   - C) Required by MLflow
   - D) Config files are easier to write

2. **What should go in the `src/` directory?**
   - A) Trained models
   - B) Raw data
   - C) Production-ready code (functions, classes)
   - D) Jupyter notebooks

3. **True or False: You should commit your `data/` folder to Git.**

<details>
<summary>Answers</summary>

1. **B** - Config files document all parameters, making experiments reproducible
2. **C** - `src/` contains production code (functions, modules), not data or notebooks
3. **False** - Data files are large and change often. Use `.gitignore` and store data externally (S3, etc.)

</details>

---

## Summary

- Standard structure: data/, src/, models/, experiments/, config/, tests/
- Separate concerns: one file/module = one responsibility
- Use config files for all parameters (not hard-coded)
- Name experiments with dates + descriptive names
- Keep notebooks for exploration, scripts for production
- Grow structure incrementally—don't over-organize on day 1

---

## Next Steps

→ Continue to **Lecture 6.4**: Experiment Tracking Concepts (Runs, Params, Metrics, Artifacts)

---

## Additional Resources

- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) - Standard project template
- [Hydra](https://hydra.cc/) - Advanced configuration management
- [DVC](https://dvc.org/) - Data version control
