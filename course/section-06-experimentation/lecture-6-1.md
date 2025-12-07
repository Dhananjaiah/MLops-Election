# Lecture 6.1 – The Reproducibility Ladder: Experiments, Versioning & Pipelines

## In This Lecture You Will Learn

- [x] Understand the reproducibility ladder (from chaos to full automation)
- [x] Identify where your current ML work sits on the ladder
- [x] Plan a path to move up the reproducibility ladder incrementally

---

## Real-World Context

> **Story**: Sarah trained a model with 89% accuracy. Her manager loved it: "Can you retrain this next week with fresh data?" Sarah tried. Same code, same data source, different result: 76% accuracy. She spent 3 days debugging, discovered she forgot to set a random seed, used a slightly different data pull, and couldn't remember which hyperparameters she used. The lesson: An experiment you can't reproduce is worthless. One-time success doesn't count in production systems. Reproducibility isn't optional—it's the foundation of reliable ML.

In the real world, irreproducible experiments waste time, erode trust, and block production deployment. Moving up the reproducibility ladder is how teams go from "works on my laptop once" to "works reliably for everyone, always."

---

## Main Content

### 1. The Reproducibility Ladder (5 Levels)

```
Level 5: Full Pipeline Automation ←─── Goal
  ↑     • One command reproduces everything
  │     • Versioned data, code, config, environment
  │     • CI/CD runs experiments automatically
  │
Level 4: Tracked Experiments
  ↑     • All experiments logged (MLflow, W&B)
  │     • Can compare runs, see what changed
  │     • Still some manual steps
  │
Level 3: Scripted Experiments
  ↑     • Code in .py files, not notebooks
  │     • Config files for hyperparameters
  │     • Version controlled
  │
Level 2: Organized Notebooks
  ↑     • Notebooks have structure, comments
  │     • Some versioning
  │     • Still hard to reproduce
  │
Level 1: Chaotic Notebook
  ↓     • One giant notebook
        • No version control
        • "Works on my machine... sometimes"
```

**Most teams start at Level 1 or 2. Production systems need Level 4-5.**

### 2. What Does "Reproducible" Mean?

**Weak Reproducibility**: Same person, same machine, same week → same result
- Good enough for personal projects
- Not good enough for production

**Strong Reproducibility**: Different person, different machine, months later → same result
- Required for production ML
- Requires versioning EVERYTHING

**What Must Be Versioned**:
1. **Code**: Git commit SHA
2. **Data**: Dataset version (DVC, timestamps, hashes)
3. **Config**: Hyperparameters, feature list
4. **Environment**: Python version, library versions (requirements.txt)
5. **Random Seeds**: For reproducible randomness
6. **Hardware**: GPU type can affect results (document it)

**Example - Reproducible Experiment Documentation**:
```yaml
experiment_id: churn_model_v3
date: 2024-01-15
author: sarah@company.com

code:
  repo: github.com/company/ml-models
  commit: abc123def
  
data:
  training: s3://data/churn/2024-01-01/train.parquet
  validation: s3://data/churn/2024-01-01/val.parquet
  hash: md5:7f8a9b...

config:
  model: RandomForestClassifier
  n_estimators: 100
  max_depth: 10
  random_state: 42

environment:
  python: 3.9.7
  requirements: requirements.txt (hash: sha256:3f2a...)

results:
  accuracy: 0.89
  precision: 0.85
  recall: 0.87
  training_time: 45.2s
```

### 3. Moving Up the Ladder: Practical Steps

**Level 1 → Level 2**: Organize your notebook
- Add markdown headers for sections
- Add comments explaining logic
- Save to Git (even if messy)
- Estimated time: 1 hour

**Level 2 → Level 3**: Convert to scripts
- Extract functions from notebook cells
- Put hyperparameters in config file
- Create `train.py`, `evaluate.py` scripts
- Estimated time: 1 day

**Level 3 → Level 4**: Add experiment tracking
- Install MLflow or Weights & Biases
- Log parameters, metrics, artifacts
- Compare experiments in UI
- Estimated time: 2 days

**Level 4 → Level 5**: Full pipeline automation
- Airflow/Prefect orchestrates training
- CI/CD runs experiments on every commit
- Automatic model registration
- Estimated time: 1-2 weeks

**You don't jump from 1 to 5 overnight. Incremental improvement.**

---

## Diagrams

```
┌─────────────────────────────────────────────────────────────────┐
│                  The Reproducibility Ladder                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Level 5: █████████████████████████ Full Automation            │
│           • One-command reproduce                                │
│           • CI/CD integrated                                     │
│           • Production ready                                     │
│                                                                  │
│  Level 4: ████████████████████ Tracked Experiments             │
│           • All runs logged                                      │
│           • Comparable results                                   │
│           • Mostly automated                                     │
│                                                                  │
│  Level 3: ███████████████ Scripted                             │
│           • Code in .py files                                    │
│           • Config-driven                                        │
│           • Version controlled                                   │
│                                                                  │
│  Level 2: ██████████ Organized Notebooks                       │
│           • Some structure                                       │
│           • Basic versioning                                     │
│           • Hard to reproduce                                    │
│                                                                  │
│  Level 1: █████ Chaotic                                        │
│           • One big notebook                                     │
│           • No versioning                                        │
│           • Impossible to reproduce                              │
│                                                                  │
│  Time Investment: Hours → Days → Weeks                          │
│  Production Readiness: 0% → 20% → 50% → 80% → 100%            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-6-1-diagram.png)

> Diagram shows the 5 levels of reproducibility from chaos to full automation

---

## Lab / Demo

### Prerequisites

- Completed Section 5
- Understanding of Git basics
- Python environment

### Step-by-Step Instructions

```bash
# Step 1: Review a Level 1 (chaotic) notebook
cd project/experiments/level1_chaotic
jupyter notebook churn_experiment_messy.ipynb

# Step 2: See a Level 3 (scripted) version
cd ../level3_scripted
cat train.py
cat config.yaml

# Step 3: Look at Level 4 (tracked) experiments
cd ../level4_tracked
python train_with_mlflow.py
# Open MLflow UI: mlflow ui

# Step 4: Reproduce an experiment
python train_with_mlflow.py --config config.yaml --seed 42
```

### Expected Output

```
Level 1 Output (chaotic):
- Results vary each run
- Can't remember what worked
- "It worked yesterday!"

Level 3 Output (scripted):
Experiment: churn_v1
Config loaded from: config.yaml
Training...
Results: {'accuracy': 0.89, 'precision': 0.85}
Model saved to: models/churn_v1.pkl

Level 4 Output (tracked):
MLflow Run ID: abc123
Logged parameters: {n_estimators: 100, max_depth: 10}
Logged metrics: {accuracy: 0.89}
Logged artifacts: model.pkl, feature_importance.png
View at: http://localhost:5000/#/experiments/1/runs/abc123
```

### Explanation

1. **Step 1**: See what Level 1 chaos looks like (learn what NOT to do)
2. **Step 2**: Understand how scripts + config improve reproducibility
3. **Step 3**: Experience experiment tracking benefits
4. **Step 4**: Reproduce exact results with same config and seed

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Trying to jump from Level 1 to Level 5 immediately. You'll get overwhelmed and give up. Go one level at a time.

- ⚠️ **Pitfall 2**: Forgetting to version the environment. Code + data aren't enough—library versions matter. Today's scikit-learn might give different results than last year's.

- ⚠️ **Pitfall 3**: Not testing reproducibility. Just because you logged everything doesn't mean it's actually reproducible. Try reproducing your own experiment a week later.

---

## Homework / Practice

1. **Exercise 1**: Take one of your old notebooks. What level is it on the reproducibility ladder? List 3 concrete steps to move it up one level.

2. **Exercise 2**: Create a reproducibility checklist for experiments. What must be documented to reproduce a result?

3. **Stretch Goal**: Take a simple notebook, convert it to Level 3 (scripted with config). Then convert to Level 4 (add MLflow tracking). Time yourself at each step.

---

## Quick Quiz

1. **What does "reproducible" mean in ML experiments?**
   - A) Getting the same accuracy every time
   - B) Different person, different machine, months later → same results
   - C) Running the experiment twice
   - D) Using version control

2. **Which level on the reproducibility ladder is minimum for production?**
   - A) Level 1 - Chaotic
   - B) Level 2 - Organized
   - C) Level 3 - Scripted
   - D) Level 4-5 - Tracked/Automated

3. **True or False: Setting a random seed is enough to make ML experiments reproducible.**

<details>
<summary>Answers</summary>

1. **B** - Strong reproducibility means anyone can reproduce your results anytime, anywhere
2. **D** - Production needs Level 4+ with full tracking and automation
3. **False** - Random seed helps, but you also need versioned code, data, config, and environment

</details>

---

## Summary

- Reproducibility ladder has 5 levels: Chaotic → Organized → Scripted → Tracked → Automated
- Strong reproducibility requires versioning: code, data, config, environment, seeds
- Move up incrementally—don't jump from Level 1 to 5
- Production ML systems require Level 4-5
- Test reproducibility by trying to reproduce your own work later
- Investment: hours to weeks, but essential for reliable ML systems

---

## Next Steps

→ Continue to **Lecture 6.2**: Problems with "One Big Notebook"

---

## Additional Resources

- [Google: Best Practices for ML Engineering](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [Papers with Code: ML Reproducibility](https://paperswithcode.com/rc2020)
- [MLflow: Experiment Tracking](https://mlflow.org/docs/latest/tracking.html)
