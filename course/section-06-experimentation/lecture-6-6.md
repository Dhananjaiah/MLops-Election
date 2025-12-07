# Lecture 6.6 – Reproducing Results End-to-End (Same Code, Same Data, Same Model)

## In This Lecture You Will Learn

- [x] Test end-to-end reproducibility of ML experiments
- [x] Identify and fix common reproducibility blockers
- [x] Build a checklist for reproducible experiments

---

## Real-World Context

> **Story**: "Can you reproduce the model from Q3?" asked the audit team. Dev said yes, downloaded the code from Git (commit SHA documented!), pulled the data (versioned with DVC!), checked the MLflow run (params logged!). But the accuracy was 0.87 instead of 0.89. After 2 days of debugging: Python 3.8 vs 3.9 gave slightly different results. The lesson: Reproducibility requires versioning EVERYTHING—not just code and data, but environment too. Document assumptions, test reproduction, then test again.

In the real world, claiming reproducibility and achieving it are different. The only way to know if your experiment is reproducible is to reproduce it yourself.

---

## Main Content

### 1. The Reproducibility Checklist

To reproduce an experiment, you need:

**✅ 1. Code (Exact Version)**
- Git commit SHA: `abc123def456`
- Not just "main branch"—specific commit
- Includes: training scripts, feature engineering, evaluation

**✅ 2. Data (Versioned)**
- Training data: `s3://data/train_2024-01-15.parquet` (hash: md5:7f8a...)
- Validation data: `s3://data/val_2024-01-15.parquet`
- Test data: `s3://data/test_2024-01-15.parquet`
- Use: DVC, timestamps, or content hashes

**✅ 3. Configuration (Parameters)**
- All hyperparameters in config.yaml
- Feature list documented
- Random seeds set
- No hard-coded magic numbers

**✅ 4. Environment (Dependencies)**
- Python version: 3.9.7
- Library versions: `requirements.txt` with pinned versions
  ```
  scikit-learn==1.0.2
  pandas==1.3.5
  numpy==1.21.5
  ```
- System dependencies: CUDA version if using GPU

**✅ 5. Hardware Context** (if it affects results)
- CPU/GPU type (some operations are non-deterministic)
- Document: "Trained on AWS p3.2xlarge (V100 GPU)"

**✅ 6. Execution Order**
- Step-by-step instructions
- What to run, in what order
- Expected outputs at each step

### 2. Testing Reproducibility

**Test 1: Same Person, Same Machine**
```bash
# Original run
python train.py --config config.yaml
# Result: accuracy=0.89

# One week later, same person, same machine
git checkout abc123  # Same code
python train.py --config config.yaml
# Result: accuracy=0.89 ✓
```

**Test 2: Different Person, Different Machine**
```bash
# New team member, fresh laptop
git clone repo
git checkout abc123
pip install -r requirements.txt
python train.py --config config.yaml
# Result: accuracy=0.89 ✓ (Strong reproducibility!)
```

**Test 3: Months Later**
```bash
# 6 months later, different Python version?
python --version  # 3.10 (was 3.9)
pip install -r requirements.txt  # May fail if libraries deprecated
python train.py --config config.yaml
# Result: accuracy=0.85 ❌ (Environment matters!)
```

### 3. Common Reproducibility Blockers

**Blocker 1: Random Seeds Not Set**
```python
# Bad: No seed
model = RandomForestClassifier()
# Each run gives different results

# Good: Seed everything
import random, numpy as np
random.seed(42)
np.random.seed(42)
model = RandomForestClassifier(random_state=42)
```

**Blocker 2: Unpinned Dependencies**
```
# Bad requirements.txt
pandas
scikit-learn

# Good requirements.txt
pandas==1.3.5
scikit-learn==1.0.2
```

**Blocker 3: Non-Deterministic Operations**
- GPU operations can be non-deterministic
- Parallel processing with randomness
- File order (if reading directory of files)

**Blocker 4: Hidden State**
- Global variables
- Cached data
- Model checkpoints from previous runs

**Blocker 5: Data Has Changed**
- "Latest" data vs. snapshot
- Database query without timestamp
- API responses change over time

### 4. Documentation Template

```markdown
# Experiment: churn_model_baseline
## Reproducibility Information

### Code
- Repository: https://github.com/company/ml-models
- Commit: abc123def456
- Branch: main (at time of experiment)

### Data
- Training: s3://data/churn/2024-01-15/train.parquet (md5: 7f8a9b...)
- Validation: s3://data/churn/2024-01-15/val.parquet (md5: 3c2d1f...)
- Features: See config/features.yaml

### Configuration
- Config file: config/baseline.yaml
- Model: RandomForestClassifier
- Hyperparameters: n_estimators=100, max_depth=10, random_state=42

### Environment
- Python: 3.9.7
- Requirements: requirements.txt (sha256: a1b2c3...)
- Hardware: AWS m5.2xlarge (CPU only)
- OS: Ubuntu 20.04

### Results
- Accuracy: 0.89
- Precision: 0.85
- Recall: 0.87
- Training time: 45.2 seconds
- MLflow run: http://mlflow.company.internal/runs/abc123

### Reproduction Steps
1. `git clone repo && git checkout abc123`
2. `pip install -r requirements.txt`
3. `python src/data/download_data.py --date 2024-01-15`
4. `python src/models/train_model.py --config config/baseline.yaml`
5. Expected: accuracy ≈ 0.89 (±0.01)

### Notes
- Model was trained on 2024-01-15
- Validated same results on 2024-01-22 (7 days later)
- Team member Alice reproduced on 2024-01-30 successfully
```

---

## Diagrams

```
┌──────────────────────────────────────────────────────────────────┐
│           Reproducibility Testing Flow                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Original Experiment                                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Code: commit abc123                                     │    │
│  │ Data: train_2024-01-15.parquet (hash: 7f8a...)         │    │
│  │ Config: baseline.yaml (n_estimators=100)               │    │
│  │ Environment: Python 3.9.7, requirements.txt            │    │
│  │ Result: Accuracy = 0.89                                │    │
│  └────────────────────────────────────────────────────────┘    │
│                          ↓                                        │
│  Test 1: Same Person, 1 Week Later                              │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Same code, data, config, environment                    │    │
│  │ Result: Accuracy = 0.89 ✓                              │    │
│  └────────────────────────────────────────────────────────┘    │
│                          ↓                                        │
│  Test 2: Different Person, Different Machine                    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Fresh clone, fresh environment                          │    │
│  │ Result: Accuracy = 0.89 ✓                              │    │
│  └────────────────────────────────────────────────────────┘    │
│                          ↓                                        │
│  Test 3: 6 Months Later (Environment Changed)                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Python 3.10, sklearn 1.2.0 (newer versions)            │    │
│  │ Result: Accuracy = 0.85 ❌ (Environment drift!)        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  Lesson: Pin ALL dependencies for true reproducibility         │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-6-6-diagram.png)

> Diagram shows three levels of reproducibility testing

---

## Lab / Demo

### Prerequisites

- Completed Lectures 6.1-6.5
- Git, Python environment

### Step-by-Step Instructions

```bash
# Step 1: Create a reproducible experiment
cd project
git checkout -b experiment_reproducibility_test

# Step 2: Document everything
cat > EXPERIMENT.md << 'EOF'
# Experiment Documentation
Code: $(git rev-parse HEAD)
Date: $(date)
Python: $(python --version)
Data: data/train_2024-01-15.csv
Config: config/baseline.yaml
EOF

# Step 3: Pin dependencies
pip freeze > requirements.txt

# Step 4: Run experiment and record result
python train.py --config config/baseline.yaml | tee results.txt

# Step 5: Test reproduction (simulate different person)
cd /tmp
git clone /path/to/project reprotest
cd reprotest
pip install -r requirements.txt
python train.py --config config/baseline.yaml

# Compare results
diff /path/to/project/results.txt results.txt
```

### Expected Output

```
Step 4 Output:
Accuracy: 0.890
Precision: 0.875
Model saved to: models/baseline_rf.pkl

Step 5 Output (reproduction):
Accuracy: 0.890  ← Same!
Precision: 0.875 ← Same!

diff output:
(no differences) ✓ Successfully reproduced!
```

### Explanation

1. **Step 1**: Start with clean branch
2. **Step 2**: Document all context
3. **Step 3**: Pin exact versions
4. **Step 4**: Run and save results
5. **Step 5**: Fresh environment reproduction test

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Assuming "it works on my machine" = reproducible. Test on a fresh machine/container.

- ⚠️ **Pitfall 2**: Not testing reproduction until months later. Test within days while memory is fresh.

- ⚠️ **Pitfall 3**: Ignoring small differences. 0.890 vs 0.891 might be acceptable, but investigate why they differ.

---

## Homework / Practice

1. **Exercise 1**: Take one of your experiments. Try to reproduce it in a fresh Python environment. What breaks?

2. **Exercise 2**: Create a complete reproduction guide for an experiment. Give it to a teammate—can they reproduce your results?

3. **Stretch Goal**: Set up a Docker container that encapsulates your entire environment. Test reproduction inside the container.

---

## Quick Quiz

1. **What's required for strong reproducibility?**
   - A) Just the code
   - B) Code + data
   - C) Code + data + config + environment + documentation
   - D) Nothing, randomness is fine

2. **Why pin dependency versions in requirements.txt?**
   - A) To make pip install faster
   - B) To ensure same library versions = same results
   - C) It's not necessary
   - D) To reduce file size

3. **True or False: If you can reproduce results on your own machine, it's guaranteed to work everywhere.**

<details>
<summary>Answers</summary>

1. **C** - Strong reproducibility requires versioning everything: code, data, config, environment
2. **B** - Pinned versions (pandas==1.3.5) ensure everyone uses the same libraries
3. **False** - Test on different machines/environments to ensure true reproducibility

</details>

---

## Summary

- Reproducibility checklist: code, data, config, environment, hardware context, execution order
- Test reproduction: same person (weak test), different person/machine (strong test)
- Common blockers: unseeded randomness, unpinned dependencies, non-deterministic operations
- Document everything in EXPERIMENT.md or similar
- Test reproduction early and often—don't wait months
- Strong reproducibility = different person, different machine, same results

---

## Next Steps

→ Continue to **Lecture 6.7**: How MLOps Enforces Reproducibility in a Team

---

## Additional Resources

- [DVC: Data Version Control](https://dvc.org/)
- [Docker for ML Reproducibility](https://docs.docker.com/get-started/)
- [Papers with Code: Reproducibility Checklist](https://paperswithcode.com/rc2020)
