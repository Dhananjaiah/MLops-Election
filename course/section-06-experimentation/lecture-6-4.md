# Lecture 6.4 – Experiment Tracking Concepts (Runs, Params, Metrics, Artifacts)

## In This Lecture You Will Learn

- [x] Understand the core concepts of experiment tracking
- [x] Differentiate between parameters, metrics, and artifacts
- [x] Design a tracking strategy for ML experiments

---

## Real-World Context

> **Story**: Mike ran 50 experiments over 3 months. When asked "Which model performed best?", he opened 50 spreadsheets, compared numbers manually, and realized he forgot to record the hyperparameters for experiment #23 (which had the best accuracy). He spent a week trying to reproduce it—failed. Enter experiment tracking: Every run automatically logged parameters, metrics, artifacts. Comparisons became instant. No more lost experiments. The lesson: Your memory is not an experiment tracker.

In the real world, experiment tracking is the difference between "I think model X was better" and "Model X achieved 0.89 AUC with these exact parameters." Professionalism requires systematic tracking.

---

## Main Content

### 1. The Four Pillars of Experiment Tracking

**1. Runs** (The Experiment Itself)
- A single execution of your training code
- Unique ID: `run_abc123`
- Timestamp: When it started/ended
- Status: Running, Completed, Failed
- Author: Who ran it

**2. Parameters** (Inputs)
- Model hyperparameters: `n_estimators=100`
- Feature selections: `features=['age', 'tenure']`
- Training config: `learning_rate=0.01`
- Data version: `train_data_v3`
- **Immutable**: Set once at start, never change

**3. Metrics** (Outputs)
- Model performance: accuracy, precision, recall, AUC
- Training metrics: loss, training_time
- Business metrics: predicted_churn_rate
- **Can log multiple times**: e.g., validation loss per epoch

**4. Artifacts** (Files)
- Trained model: `model.pkl`
- Plots: `confusion_matrix.png`, `feature_importance.png`
- Data samples: `predictions_sample.csv`
- Logs: `training.log`

**Example Experiment**:
```yaml
Run ID: abc123
Start: 2024-01-15 10:30:00
End: 2024-01-15 10:45:00
Status: Completed

Parameters:
  model_type: RandomForestClassifier
  n_estimators: 100
  max_depth: 10
  features: [age, tenure, charges]
  data_version: train_2024-01-01
  
Metrics:
  accuracy: 0.89
  precision: 0.85
  recall: 0.87
  auc_roc: 0.92
  training_time_sec: 45.2
  
Artifacts:
  - model.pkl (15 MB)
  - confusion_matrix.png (50 KB)
  - feature_importance.png (30 KB)
  - training.log (5 KB)
```

### 2. Why Each Pillar Matters

**Parameters**: "What did I try?"
- Without: "I think I used 100 trees... or was it 200?"
- With: "Run abc123 used n_estimators=100, run def456 used 200"

**Metrics**: "How well did it work?"
- Without: "The model was pretty good"
- With: "Run abc123: 89% accuracy, run def456: 91% accuracy"

**Artifacts**: "Can I inspect the results?"
- Without: "I remember the confusion matrix looked good"
- With: Download `confusion_matrix.png` for run abc123

**Runs**: "When did I try this?"
- Without: "I ran this experiment... sometime last month?"
- With: "Run abc123 on 2024-01-15 at 10:30 AM"

### 3. Designing a Tracking Strategy

**What to Track**:
```python
# Minimum viable tracking
track_params({
    'model_type': 'RandomForest',
    'n_estimators': 100,
    'data_version': 'v1',
    'features': feature_list
})

track_metrics({
    'accuracy': 0.89,
    'precision': 0.85,
    'recall': 0.87
})

track_artifacts([
    'model.pkl',
    'confusion_matrix.png'
])
```

**What NOT to Track** (Keep it lean):
- ❌ Every intermediate variable
- ❌ Gigabytes of data
- ❌ Redundant information
- ✅ Track what you need to reproduce + evaluate

**Comparison Example**:
| Run ID | Model | n_estimators | Accuracy | Precision | Recall | Best? |
|--------|-------|--------------|----------|-----------|--------|-------|
| abc123 | RF | 100 | 0.89 | 0.85 | 0.87 | ❌ |
| def456 | RF | 200 | 0.91 | 0.88 | 0.89 | ✅ |
| ghi789 | XGB | 100 | 0.90 | 0.87 | 0.88 | ❌ |

**Instantly see**: def456 (RF with 200 trees) performed best

### 4. Tracking in Practice

**Manual Tracking** (Level 2):
```python
# experiments/2024-01-15_run1.yaml
run_id: abc123
parameters:
  n_estimators: 100
metrics:
  accuracy: 0.89
```
**Pro**: Simple, no dependencies
**Con**: Manual, error-prone, hard to compare

**Tool-Based Tracking** (Level 4):
```python
import mlflow

with mlflow.start_run():
    # Auto-generates run_id
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", 0.89)
    mlflow.log_artifact("model.pkl")
```
**Pro**: Automatic, UI for comparison, shareable
**Con**: Requires setup

---

## Diagrams

```
┌────────────────────────────────────────────────────────────────┐
│           Experiment Tracking Components                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🏃 RUN (The Experiment)                                       │
│  ├─ ID: abc123                                                 │
│  ├─ Timestamp: 2024-01-15 10:30                                │
│  ├─ Status: Completed                                          │
│  └─ Author: mike@company.com                                   │
│      │                                                          │
│      ├──> ⚙️  PARAMETERS (Inputs)                             │
│      │     ├─ model_type: RandomForest                         │
│      │     ├─ n_estimators: 100                                │
│      │     ├─ max_depth: 10                                    │
│      │     └─ data_version: v1                                 │
│      │                                                          │
│      ├──> 📊 METRICS (Outputs)                                │
│      │     ├─ accuracy: 0.89                                   │
│      │     ├─ precision: 0.85                                  │
│      │     ├─ recall: 0.87                                     │
│      │     └─ training_time: 45.2s                             │
│      │                                                          │
│      └──> 📦 ARTIFACTS (Files)                                │
│            ├─ model.pkl                                         │
│            ├─ confusion_matrix.png                              │
│            └─ feature_importance.png                            │
│                                                                 │
│  Compare runs instantly, reproduce any experiment             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-6-4-diagram.png)

> Diagram shows the relationship between runs, parameters, metrics, and artifacts

---

## Lab / Demo

### Prerequisites

- Completed Lectures 6.1-6.3
- Python with basic ML libraries

### Step-by-Step Instructions

```bash
# Step 1: Create manual tracking example
cd project/experiments
cat > track_experiment.py << 'EOF'
import json
from datetime import datetime

def log_experiment(run_id, params, metrics, artifacts):
    experiment = {
        'run_id': run_id,
        'timestamp': datetime.now().isoformat(),
        'parameters': params,
        'metrics': metrics,
        'artifacts': artifacts
    }
    with open(f'runs/{run_id}.json', 'w') as f:
        json.dump(experiment, f, indent=2)
    print(f"Logged experiment: {run_id}")

# Example usage
log_experiment(
    run_id='abc123',
    params={'n_estimators': 100, 'max_depth': 10},
    metrics={'accuracy': 0.89, 'precision': 0.85},
    artifacts=['model.pkl', 'plot.png']
)
EOF

# Step 2: Run it
python track_experiment.py

# Step 3: View logged experiment
cat runs/abc123.json

# Step 4: Compare multiple runs
python compare_runs.py runs/abc123.json runs/def456.json
```

### Expected Output

```json
{
  "run_id": "abc123",
  "timestamp": "2024-01-15T10:30:00",
  "parameters": {
    "n_estimators": 100,
    "max_depth": 10
  },
  "metrics": {
    "accuracy": 0.89,
    "precision": 0.85
  },
  "artifacts": [
    "model.pkl",
    "plot.png"
  ]
}
```

### Explanation

1. **Step 1**: Create simple manual tracking system
2. **Step 2**: Log an experiment (parameters, metrics, artifacts)
3. **Step 3**: See structured experiment data
4. **Step 4**: Compare experiments side-by-side

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Tracking too much. Don't log every variable—track what you need to reproduce and compare experiments.

- ⚠️ **Pitfall 2**: Tracking too little. Missing key parameters means you can't reproduce successful experiments.

- ⚠️ **Pitfall 3**: Inconsistent naming. Use consistent keys: `n_estimators` vs `num_estimators` vs `numTrees` makes comparison impossible.

---

## Homework / Practice

1. **Exercise 1**: Design a tracking schema for our churn project. What parameters, metrics, and artifacts should be logged?

2. **Exercise 2**: Run 3 experiments manually, log them to JSON files. Compare which performed best.

3. **Stretch Goal**: Build a simple Python script that reads multiple experiment JSON files and generates a comparison table.

---

## Quick Quiz

1. **What are the four pillars of experiment tracking?**
   - A) Code, Data, Models, Tests
   - B) Runs, Parameters, Metrics, Artifacts
   - C) Training, Validation, Testing, Deployment
   - D) Notebooks, Scripts, Configs, Logs

2. **What's the difference between parameters and metrics?**
   - A) There is no difference
   - B) Parameters are inputs (config), metrics are outputs (performance)
   - C) Parameters are for classification, metrics for regression
   - D) Metrics are more important

3. **True or False: You should log every variable and intermediate result for complete tracking.**

<details>
<summary>Answers</summary>

1. **B** - Runs (experiments), Parameters (inputs), Metrics (outputs), Artifacts (files)
2. **B** - Parameters are what you SET (hyperparameters), metrics are what you MEASURE (accuracy)
3. **False** - Track what's needed to reproduce and compare. Too much tracking creates noise and wastes storage.

</details>

---

## Summary

- Four pillars: Runs (experiments), Parameters (inputs), Metrics (outputs), Artifacts (files)
- Parameters: hyperparameters, data versions, feature sets (immutable)
- Metrics: performance measures, can log multiple times during training
- Artifacts: models, plots, logs (files to inspect)
- Track enough to reproduce + compare, but not everything
- Can start with manual JSON files, graduate to tools like MLflow

---

## Next Steps

→ Continue to **Lecture 6.5**: Using MLflow (or Similar) to Track Experiments

---

## Additional Resources

- [MLflow Tracking Documentation](https://mlflow.org/docs/latest/tracking.html)
- [Weights & Biases: Experiment Tracking Guide](https://docs.wandb.ai/guides/track)
- [Neptune.ai: Experiment Tracking Best Practices](https://neptune.ai/blog/ml-experiment-tracking)
