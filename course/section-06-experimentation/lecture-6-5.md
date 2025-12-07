# Lecture 6.5 – Using MLflow (or Similar) to Track Experiments

## In This Lecture You Will Learn

- [x] Set up and use MLflow for experiment tracking
- [x] Log parameters, metrics, and artifacts programmatically
- [x] Compare experiments using MLflow UI

---

## Real-World Context

> **Story**: After manually tracking 100+ experiments in spreadsheets, Chen's team discovered MLflow. Setup took 30 minutes. The payoff: instant experiment comparison, automatic artifact storage, shareable links to runs. Their weekly "which experiment was best?" meeting went from 2 hours of spreadsheet archaeology to 5 minutes of clicking through the MLflow UI. The lesson: Don't reinvent experiment tracking. Use proven tools that solve this problem well.

In the real world, MLflow (or similar tools) are industry standard for experiment tracking. Learning one tool deeply is better than building custom solutions.

---

## Main Content

### 1. What Is MLflow?

**MLflow** is an open-source platform for the complete ML lifecycle, including:
- **MLflow Tracking**: Log and query experiments (we focus on this)
- **MLflow Projects**: Package code in reproducible format
- **MLflow Models**: Deploy models to various platforms
- **MLflow Registry**: Store and manage model versions

**Why MLflow?**
- ✅ Open source (no vendor lock-in)
- ✅ Language agnostic (Python, R, Java, etc.)
- ✅ Framework agnostic (scikit-learn, TensorFlow, PyTorch, etc.)
- ✅ Simple API
- ✅ Built-in UI for visualization
- ✅ Local or remote server deployment

### 2. MLflow Tracking Basics

**Core Concepts**:
- **Experiment**: A collection of related runs (e.g., "churn_model_2024")
- **Run**: A single execution with params, metrics, artifacts
- **Tracking Server**: Where data is stored (local files or remote database)

**Basic Usage**:
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# Set experiment name
mlflow.set_experiment("churn_prediction")

# Start a run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    mlflow.log_param("data_version", "v1")
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    
    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("training_samples", len(X_train))
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts (plots, files)
    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")
    
print(f"Run ID: {mlflow.active_run().info.run_id}")
```

### 3. MLflow UI - Exploring Experiments

**Starting the UI**:
```bash
# Local tracking (stores in ./mlruns/)
mlflow ui

# Custom location
mlflow ui --backend-store-uri file:///path/to/mlruns

# Remote tracking server
mlflow ui --backend-store-uri postgresql://user:pass@host/db
```

**UI Features**:
1. **Experiments List**: See all your experiments
2. **Runs Table**: Compare parameters and metrics side-by-side
3. **Run Details**: Deep dive into one run
4. **Plots**: Auto-generated comparison charts
5. **Artifacts**: Download models, plots, files
6. **Search/Filter**: Find runs by parameter values or metrics

**Example Comparison**:
```
Experiment: churn_prediction
─────────────────────────────────────────────────────────────
Run ID    | n_estimators | max_depth | accuracy | Best?
─────────────────────────────────────────────────────────────
abc123    | 100          | 10        | 0.89     | ❌
def456    | 200          | 10        | 0.91     | ✅  ← Winner
ghi789    | 100          | 20        | 0.90     | ❌
```

### 4. Advanced MLflow Features

**Nested Runs** (For hyperparameter tuning):
```python
with mlflow.start_run(run_name="hyperparam_search"):
    for n_est in [50, 100, 200]:
        with mlflow.start_run(nested=True):
            mlflow.log_param("n_estimators", n_est)
            # Train and log metrics
```

**Autologging** (Automatic parameter/metric capture):
```python
mlflow.sklearn.autolog()  # Auto-logs sklearn model info

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
# Parameters and metrics automatically logged!
```

**Tags** (Organize experiments):
```python
mlflow.set_tag("model_type", "baseline")
mlflow.set_tag("team", "data-science")
mlflow.set_tag("production_ready", "no")
```

**Model Registry Integration** (For production models):
```python
# Log model with signature
mlflow.sklearn.log_model(model, "model", registered_model_name="churn_model")

# Transition to production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="churn_model",
    version=3,
    stage="Production"
)
```

### 5. Alternatives to MLflow

| Tool | Type | Best For |
|------|------|----------|
| **MLflow** | Open Source | General purpose, self-hosted |
| **Weights & Biases** | Commercial | Deep learning, beautiful UI |
| **Neptune.ai** | Commercial | Team collaboration |
| **Comet.ml** | Commercial | Experiment comparison |
| **TensorBoard** | Open Source | TensorFlow/PyTorch specific |
| **Sacred** | Open Source | Academic research |

**Our Choice**: MLflow - free, popular, general-purpose

---

## Diagrams

```
┌───────────────────────────────────────────────────────────────┐
│                   MLflow Workflow                              │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  1. CODE: Your Training Script                                │
│     ┌────────────────────────────────────────┐               │
│     │ import mlflow                           │               │
│     │                                         │               │
│     │ with mlflow.start_run():                │               │
│     │   mlflow.log_param("n_estimators",100) │               │
│     │   model.fit(X,y)                        │               │
│     │   mlflow.log_metric("accuracy", 0.89)   │               │
│     │   mlflow.log_artifact("model.pkl")      │               │
│     └────────────────────────────────────────┘               │
│              ↓                                                 │
│  2. STORAGE: MLflow Tracking Server                           │
│     ┌────────────────────────────────────────┐               │
│     │  Experiments/                           │               │
│     │  └─ churn_prediction/                   │               │
│     │      ├─ Run abc123                      │               │
│     │      ├─ Run def456                      │               │
│     │      └─ Run ghi789                      │               │
│     └────────────────────────────────────────┘               │
│              ↓                                                 │
│  3. UI: MLflow Dashboard                                       │
│     ┌────────────────────────────────────────┐               │
│     │  Compare Runs                           │               │
│     │  ┌───────────────────────────────┐    │               │
│     │  │Run  │ n_est │max_d│ accuracy ││    │               │
│     │  │abc  │  100  │ 10  │   0.89   ││    │               │
│     │  │def  │  200  │ 10  │   0.91  ✓││    │               │
│     │  │ghi  │  100  │ 20  │   0.90   ││    │               │
│     │  └───────────────────────────────┘    │               │
│     └────────────────────────────────────────┘               │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-6-5-diagram.png)

> Diagram shows MLflow workflow from code to storage to UI comparison

---

## Lab / Demo

### Prerequisites

- Completed Lectures 6.1-6.4
- Python with MLflow installed: `pip install mlflow`

### Step-by-Step Instructions

```bash
# Step 1: Install MLflow
pip install mlflow scikit-learn pandas

# Step 2: Create simple training script with MLflow
cat > train_with_mlflow.py << 'EOF'
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Generate sample data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Set experiment
mlflow.set_experiment("churn_prediction_demo")

# Run experiment
with mlflow.start_run():
    # Log parameters
    n_estimators = 100
    max_depth = 10
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    
    # Train
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X_train, y_train)
    
    # Predict and evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    print(f"Run ID: {mlflow.active_run().info.run_id}")
    print(f"Accuracy: {accuracy:.3f}")
EOF

# Step 3: Run the experiment
python train_with_mlflow.py

# Step 4: Start MLflow UI
mlflow ui

# Step 5: Open browser to http://localhost:5000
```

### Expected Output

```
$ python train_with_mlflow.py
Run ID: abc123def456ghi789
Accuracy: 0.890

$ mlflow ui
[2024-01-15 10:30:00] INFO: Starting MLflow server
[2024-01-15 10:30:00] INFO: Listening on http://localhost:5000

# In browser at http://localhost:5000:
Experiments:
  └─ churn_prediction_demo
      └─ Run abc123def456ghi789
          Parameters:
            n_estimators: 100
            max_depth: 10
          Metrics:
            accuracy: 0.890
            precision: 0.875
            recall: 0.905
          Artifacts:
            model/ (sklearn model)
```

### Explanation

1. **Step 1**: Install MLflow and dependencies
2. **Step 2**: Create training script with MLflow logging
3. **Step 3**: Run experiment (automatically logs to ./mlruns/)
4. **Step 4**: Start web UI to visualize experiments
5. **Step 5**: Browse experiments, compare runs, download artifacts

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Not setting experiment name. Runs go to "Default" experiment making them hard to find. Always `mlflow.set_experiment("name")`.

- ⚠️ **Pitfall 2**: Forgetting to call `mlflow.start_run()`. Logging outside a run context fails silently.

- ⚠️ **Pitfall 3**: Logging too many metrics. MLflow can get slow with thousands of metrics per run. Log what matters.

---

## Homework / Practice

1. **Exercise 1**: Install MLflow, run the example above, explore the UI. Click through runs, compare parameters, download a model.

2. **Exercise 2**: Modify the script to run 5 experiments with different `n_estimators` values (50, 100, 150, 200, 250). Compare which performs best in MLflow UI.

3. **Stretch Goal**: Add autologging (`mlflow.sklearn.autolog()`) and see what gets logged automatically. Compare with manual logging.

---

## Quick Quiz

1. **What does MLflow Tracking do?**
   - A) Train models faster
   - B) Log and query experiments (params, metrics, artifacts)
   - C) Deploy models to production
   - D) Clean your data

2. **How do you start the MLflow UI?**
   - A) `mlflow start`
   - B) `mlflow dashboard`
   - C) `mlflow ui`
   - D) `python mlflow.py`

3. **True or False: MLflow only works with scikit-learn models.**

<details>
<summary>Answers</summary>

1. **B** - MLflow Tracking logs experiments for comparison and reproducibility
2. **C** - Run `mlflow ui` to start the web interface
3. **False** - MLflow is framework-agnostic (works with TensorFlow, PyTorch, XGBoost, etc.)

</details>

---

## Summary

- MLflow is open-source experiment tracking platform
- Key features: log params/metrics/artifacts, compare runs via UI
- Basic usage: `mlflow.start_run()` → `log_param()` → `log_metric()` → `log_artifact()`
- MLflow UI provides visualization and comparison tools
- Alternatives exist (W&B, Neptune, Comet) but MLflow is industry standard
- Start local (`./mlruns`), scale to remote server as team grows

---

## Next Steps

→ Continue to **Lecture 6.6**: Reproducing Results End-to-End (Same Code, Same Data, Same Model)

---

## Additional Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow Quickstart Tutorial](https://mlflow.org/docs/latest/quickstart.html)
- [Databricks: MLflow Best Practices](https://www.databricks.com/blog/2020/04/14/ml-ops-best-practices-using-mlflow.html)
