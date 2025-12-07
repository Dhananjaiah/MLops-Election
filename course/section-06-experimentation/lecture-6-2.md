# Lecture 6.2 – Problems with "One Big Notebook"

## In This Lecture You Will Learn

- [x] Identify why "one big notebook" fails in production ML
- [x] Recognize the specific problems notebooks cause for teams
- [x] Understand when to move from notebooks to scripts

---

## Real-World Context

> **Story**: Jake's notebook was 3,000 lines long. To run a new experiment, he'd scroll to cell 47, change a parameter, re-run cells 47-152 (but skip cell 89 which had a bug), then jump to cell 200 for evaluation. His teammate tried to reproduce his results—gave up after 2 hours. When Jake went on vacation, nobody could run his experiments. When he came back, even HE couldn't remember the run order. The lesson: Notebooks are great for exploration, terrible for production. There's a time to move on.

In the real world, notebooks are how most ML work starts. But staying in notebooks too long creates technical debt, blocks collaboration, and prevents deployment. Knowing when and how to graduate from notebooks is a critical MLOps skill.

---

## Main Content

### 1. Why Notebooks Are Great (For Exploration)

**Notebooks Excel At**:
- ✅ Quick iteration and visualization
- ✅ Interactive data exploration
- ✅ Teaching and presentations
- ✅ Prototyping new ideas
- ✅ Sharing analysis with non-technical stakeholders

**Perfect Use Case**: "Let's explore this dataset and try 3 algorithms"

### 2. The Problems with "One Big Notebook"

**Problem 1: Hidden State**
```python
# Cell 1
x = 5

# Cell 5 (run before Cell 3)
x = x + 10  # x = 15

# Cell 3 (run last)
print(x)  # Prints 15, but should print 5 if run top-to-bottom
```
**Issue**: Cell execution order matters. Run out of order = wrong results.

**Problem 2: Hard to Refactor**
- Copy-paste same code in multiple cells
- Change one place, forget to change others
- No functions, no modules, no reuse

**Problem 3: Impossible to Test**
- Can't write unit tests for notebook cells
- No way to validate functions work correctly
- Changes break things silently

**Problem 4: Version Control Nightmares**
- Notebooks are JSON (includes outputs, cell IDs)
- Git diffs are unreadable
- Merge conflicts are painful
- Can't do meaningful code reviews

**Problem 5: Can't Integrate with CI/CD**
- No way to run notebook in automated pipeline
- Can't schedule notebook execution reliably
- Can't deploy notebook as API

**Problem 6: Team Collaboration Fails**
- "Works on my machine" syndrome
- Hidden dependencies (cell execution order)
- Unclear how to use someone else's notebook
- No clear interface or documentation

**Problem 7: No Separation of Concerns**
- Data loading mixed with feature engineering
- Training mixed with evaluation
- Visualization mixed with business logic
- Everything in one file = unmaintainable

### 3. When to Move from Notebook to Scripts

**Stay in Notebooks When**:
- ✅ Exploring new dataset (first 1-2 weeks)
- ✅ Trying different algorithms quickly
- ✅ Creating visualizations for stakeholders
- ✅ One-off analysis

**Move to Scripts When**:
- ⚠️ Notebook exceeds 500 lines
- ⚠️ Running same experiment multiple times
- ⚠️ Need to share code with team
- ⚠️ Ready to automate training
- ⚠️ Preparing for production deployment

**The Transition**:
```
Week 1-2: Notebook exploration (good!)
Week 3: Extract functions, organize cells
Week 4: Convert to train.py, evaluate.py scripts
Week 5+: Add config, logging, tests
```

### 4. How to Transition (Practical Steps)

**Step 1: Extract Functions**
```python
# Before: All code in cells
data = pd.read_csv('data.csv')
data = data.dropna()
data['new_feature'] = data['a'] / data['b']
# ... 50 more lines

# After: Functions
def load_and_clean_data(path):
    data = pd.read_csv(path)
    data = data.dropna()
    return data

def engineer_features(data):
    data['new_feature'] = data['a'] / data['b']
    return data
```

**Step 2: Create Modules**
```
project/
  src/
    data.py         # load_and_clean_data()
    features.py     # engineer_features()
    models.py       # train_model(), evaluate_model()
  scripts/
    train.py        # Main training script
  notebooks/
    exploration.ipynb  # Keep for exploration only
```

**Step 3: Use Config Files**
```yaml
# config.yaml
data:
  train_path: data/train.csv
  test_path: data/test.csv

model:
  type: RandomForest
  n_estimators: 100
  max_depth: 10
  random_state: 42
```

**Step 4: Add CLI**
```python
# train.py
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    # Load config, train model, save output
    
if __name__ == '__main__':
    main()
```

---

## Diagrams

```
┌────────────────────────────────────────────────────────────────┐
│         Notebook → Scripts Transition                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📓 ONE BIG NOTEBOOK (3000 lines)                              │
│  Problems:                                                      │
│  • Hidden state (cell order matters)                           │
│  • Can't test or version control                               │
│  • No CI/CD integration                                        │
│  • Team collaboration fails                                    │
│                                                                 │
│  ↓ REFACTOR ↓                                                  │
│                                                                 │
│  📁 ORGANIZED SCRIPTS                                          │
│  ├── src/                                                      │
│  │   ├── data.py (functions)                                  │
│  │   ├── features.py                                          │
│  │   └── models.py                                            │
│  ├── scripts/                                                  │
│  │   └── train.py (CLI)                                       │
│  ├── config.yaml                                               │
│  └── tests/                                                    │
│                                                                 │
│  Benefits:                                                      │
│  ✓ Testable, versionable, CI/CD ready                         │
│  ✓ Team can collaborate                                        │
│  ✓ Clear structure and interfaces                             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-6-2-diagram.png)

> Diagram shows the transition from monolithic notebook to organized script structure

---

## Lab / Demo

### Prerequisites

- Completed Lecture 6.1
- Familiarity with Jupyter notebooks
- Basic Python knowledge

### Step-by-Step Instructions

```bash
# Step 1: Review a "big notebook" example
cd project/experiments
jupyter notebook big_messy_notebook.ipynb

# Step 2: See the refactored version
cd ../src
cat data.py features.py models.py

# Step 3: Run the scriptified version
cd ../scripts
python train.py --config ../config.yaml --output ../models/

# Step 4: Compare: notebook vs scripts
diff ../experiments/big_messy_notebook.ipynb train.py
```

### Expected Output

```
Big Notebook Issues Found:
- 3,247 lines of code
- Cell execution order critical
- 15 global variables
- No functions, all inline code
- Can't run in CI/CD

Refactored Scripts:
- data.py: 150 lines (testable functions)
- features.py: 200 lines (reusable)
- models.py: 180 lines (clean interface)
- train.py: 50 lines (CLI wrapper)
- config.yaml: 20 lines (all parameters)

$ python train.py --config config.yaml
Loading data from: data/train.csv
Engineering features...
Training RandomForest...
Accuracy: 0.89
Model saved to: models/churn_v1.pkl
```

### Explanation

1. **Step 1**: Experience the pain of navigating a massive notebook
2. **Step 2**: See how code is organized into logical modules
3. **Step 3**: Run clean, testable, CI/CD-ready training
4. **Step 4**: Appreciate the improvement

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Thinking you need to abandon notebooks entirely. Keep them for exploration! Just don't deploy them to production.

- ⚠️ **Pitfall 2**: Refactoring too early. If you're still exploring, stay in notebooks. Wait until you have something that works.

- ⚠️ **Pitfall 3**: Refactoring too late. If your notebook is 5,000 lines and used by 3 people, you're already in pain. Refactor sooner.

---

## Homework / Practice

1. **Exercise 1**: Review one of your notebooks. Count: lines of code, number of cells, global variables, functions. Is it time to refactor?

2. **Exercise 2**: Take a 100-line notebook and extract 3 functions from it. Put them in a separate .py file and import them into the notebook.

3. **Stretch Goal**: Convert a simple notebook (200-300 lines) into a script with CLI arguments and a config file. Time yourself—it should take 1-2 hours max.

---

## Quick Quiz

1. **What is the main problem with hidden state in notebooks?**
   - A) It uses too much memory
   - B) Cell execution order affects results, making them hard to reproduce
   - C) It's a security risk
   - D) Notebooks run slower

2. **When should you move from notebooks to scripts?**
   - A) Day 1 of any ML project
   - B) Never, notebooks are fine for everything
   - C) When ready to automate, share with team, or deploy
   - D) Only for large companies

3. **True or False: You should delete all notebooks after moving to scripts.**

<details>
<summary>Answers</summary>

1. **B** - Hidden state means running cells out of order gives wrong results
2. **C** - Move to scripts when automation, collaboration, or deployment is needed
3. **False** - Keep notebooks for exploration and visualization. Just don't use them for production code.

</details>

---

## Summary

- Notebooks are great for exploration, terrible for production
- Problems: hidden state, hard to test, version control issues, no CI/CD
- Move to scripts when: >500 lines, automating, sharing with team, deploying
- Transition: Extract functions → Create modules → Add config → Build CLI
- Keep notebooks for exploration, use scripts for production
- This transition usually takes 1-2 weeks and is worth every hour

---

## Next Steps

→ Continue to **Lecture 6.3**: Structuring Experiments (Folders, Scripts, Configs)

---

## Additional Resources

- [Netflix: Notebook-Driven Development](https://netflixtechblog.com/notebook-innovation-591ee3221233)
- [Joel Grus: I Don't Like Notebooks](https://www.youtube.com/watch?v=7jiPeIFXb6U) - Controversial but valuable perspective
- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) - Project template
