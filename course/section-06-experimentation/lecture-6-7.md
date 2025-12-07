# Lecture 6.7 – How MLOps Enforces Reproducibility in a Team

## In This Lecture You Will Learn

- [x] Implement team-wide reproducibility practices
- [x] Use MLOps tooling to enforce reproducibility automatically
- [x] Build a culture of reproducibility in ML teams

---

## Real-World Context

> **Story**: At StartupCo, each data scientist had their own way of tracking experiments. Alice used spreadsheets. Bob used MLflow locally. Carol just... remembered (badly). Code reviews were impossible because no one knew what parameters were used. When they landed a big client requiring audit trails, they had 3 months of "we think we can reproduce this... maybe?" The fix: company-wide standards enforced through tooling. Every experiment MUST be logged to central MLflow. Every model MUST have a config file. Git commit SHAs MUST be tagged. Compliance went from "hope and prayer" to "click a button."

In the real world, reproducibility isn't a personal virtue—it's a team requirement enforced through process and tooling. MLOps is how you scale reproducibility from one person to dozens.

---

## Main Content

### 1. Team Reproducibility Challenges

**Individual Level** (Lecture 6.6): You can reproduce YOUR experiments
- Your machine, your setup, your memory

**Team Level** (This lecture): ANYONE can reproduce ANY experiment
- Different people, different machines, months later
- No tribal knowledge, no "ask Alice how she did it"

**Challenges**:
1. Different development environments
2. Inconsistent tool usage
3. Undocumented decisions
4. Lost institutional knowledge (turnover)
5. No enforcement of standards

### 2. MLOps Solutions for Team Reproducibility

**Solution 1: Centralized Experiment Tracking**

**Problem**: Everyone tracks experiments differently
**Solution**: Mandatory central MLflow server

```python
# Configuration enforced in .env or config
MLFLOW_TRACKING_URI=https://mlflow.company.internal

# Every experiment automatically logs here
import mlflow
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# Can't run experiments without logging
with mlflow.start_run():
    # ... experiment code
```

**Benefits**:
- All experiments in one place
- Searchable by anyone on team
- Audit trail for compliance
- Cross-team comparison

**Solution 2: Standardized Project Templates**

**Problem**: Every project structured differently
**Solution**: Cookiecutter template enforced at project creation

```bash
# Company template
cookiecutter https://github.com/company/ml-project-template

# Generates:
project/
├── data/
├── src/
├── config/
├── tests/
├── requirements.txt
├── Makefile
└── README.md (with required sections)
```

**Solution 3: Automated Environment Management**

**Problem**: "Works on my machine" syndrome
**Solution**: Docker containers for all training

```dockerfile
# Dockerfile (versioned in Git)
FROM python:3.9.7
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ /app/src/
WORKDIR /app
ENTRYPOINT ["python", "src/train.py"]
```

```bash
# Anyone can run:
docker build -t churn-model:v1 .
docker run churn-model:v1 --config config/baseline.yaml
```

**Solution 4: Automated Code Reviews**

**Problem**: Parameters hard-coded, experiments not logged
**Solution**: CI/CD checks before merge

```yaml
# .github/workflows/pr-checks.yml
name: Experiment Validation
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Check config files exist
        run: test -f config/*.yaml
      
      - name: Check no hard-coded parameters
        run: |
          ! grep -r "n_estimators = 100" src/
      
      - name: Check MLflow logging
        run: |
          grep -r "mlflow.start_run" src/ || exit 1
      
      - name: Run reproducibility test
        run: |
          python train.py --config config/test.yaml
          python train.py --config config/test.yaml
          diff results1.txt results2.txt
```

**Solution 5: Data Version Control (DVC)**

**Problem**: Data changes without versioning
**Solution**: Treat data like code

```bash
# Initialize DVC
dvc init

# Track data
dvc add data/train.csv
git add data/train.csv.dvc data/.gitignore
git commit -m "Add training data v1"

# Anyone can pull exact data
git checkout abc123
dvc pull  # Downloads data/train.csv from S3/GCS
```

### 3. Team Processes for Reproducibility

**Process 1: Experiment Review Meetings**
- Weekly meeting: review experiments
- Present: config, results, MLflow link
- Discuss: what worked, what didn't
- Document: decisions in wiki/Confluence

**Process 2: Reproducibility Testing**
- Before merging to main: reproduce on CI
- Before production deployment: team member reproduces
- Quarterly audits: random sample of old experiments

**Process 3: Documentation Standards**
```markdown
## Required in Every PR Description:
1. MLflow run link
2. Config file used
3. Data version (DVC/timestamp)
4. Results (accuracy, etc.)
5. Reproduction instructions
```

**Process 4: Onboarding Checklist**
```
New Team Member Onboarding:
☐ Clone repo, set up environment (should take <30 min)
☐ Reproduce the "baseline" experiment (proves setup works)
☐ Run own experiment, log to MLflow
☐ Present experiment in team meeting
```

### 4. Cultural Shift: Making Reproducibility the Default

**Shift 1: From "Nice to Have" to "Non-Negotiable"**
- Don't merge PRs without experiment tracking
- Don't deploy models without reproduction test
- Don't present results without MLflow link

**Shift 2: From "Extra Work" to "Time Saver"**
- Initial setup: Yes, takes time
- Long-term payoff: Massive time savings
- Frame it: "We're investing 1 hour now to save 10 hours later"

**Shift 3: From "Individual" to "Team Sport"**
- Your experiment should be reproducible by ANY teammate
- Pair on experiment setup
- Review each other's MLflow runs

**Shift 4: Celebrate Reproducibility Wins**
- "Alice reproduced Bob's 3-month-old experiment in 10 minutes!"
- "We passed the compliance audit thanks to our tracking!"
- Make heroes of people who document well

### 5. Measuring Reproducibility Maturity

| Level | Criteria | Typical Company |
|-------|----------|-----------------|
| **0 - Chaos** | No tracking, no versioning | Early startups |
| **1 - Aware** | Some experiments logged manually | Growing startups |
| **2 - Standard** | Most experiments tracked, templates used | Mid-size companies |
| **3 - Enforced** | CI/CD checks, required logging | Mature ML teams |
| **4 - Auditable** | Full compliance, tested reproduction | Regulated industries |

**Goal**: Reach Level 3 for most teams, Level 4 if required by industry

---

## Diagrams

```
┌─────────────────────────────────────────────────────────────────┐
│         MLOps Team Reproducibility Stack                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LAYER 1: Standards & Templates                                 │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • Cookiecutter project template                       │      │
│  │ • Required README sections                            │      │
│  │ • Config file naming conventions                      │      │
│  └──────────────────────────────────────────────────────┘      │
│                         ↓                                         │
│  LAYER 2: Automation & Tooling                                  │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • Central MLflow server (mandatory logging)           │      │
│  │ • DVC for data versioning                             │      │
│  │ • Docker for environment consistency                  │      │
│  │ • Git for code versioning                             │      │
│  └──────────────────────────────────────────────────────┘      │
│                         ↓                                         │
│  LAYER 3: Enforcement (CI/CD)                                   │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • PR checks: config exists, params not hard-coded     │      │
│  │ • Reproduction tests run automatically                │      │
│  │ • Block merge if experiment not logged                │      │
│  └──────────────────────────────────────────────────────┘      │
│                         ↓                                         │
│  LAYER 4: Culture & Process                                     │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • Weekly experiment reviews                           │      │
│  │ • Onboarding: reproduce baseline experiment           │      │
│  │ • Celebrate reproducibility wins                      │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                  │
│  Result: Anyone can reproduce any experiment, anytime          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-6-7-diagram.png)

> Diagram shows the four layers of team reproducibility infrastructure

---

## Lab / Demo

### Prerequisites

- Completed all previous lectures in Section 6
- Team environment (or simulate with multiple local directories)

### Step-by-Step Instructions

```bash
# Step 1: Set up team-wide MLflow server (simulate)
mlflow server --host 0.0.0.0 --port 5000 &
export MLFLOW_TRACKING_URI=http://localhost:5000

# Step 2: Create project from template
cookiecutter https://github.com/drivendata/cookiecutter-data-science
cd my_ml_project

# Step 3: Set up DVC for data versioning
dvc init
dvc add data/raw/train.csv
git add data/raw/train.csv.dvc .dvc/.gitignore

# Step 4: Create CI/CD validation script
cat > .github/workflows/validate.yml << 'EOF'
name: Experiment Validation
on: [pull_request]
jobs:
  reproduce:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Reproduce experiment
        run: |
          python train.py --config config/baseline.yaml > run1.txt
          python train.py --config config/baseline.yaml > run2.txt
          diff run1.txt run2.txt || echo "WARNING: Non-deterministic results"
EOF

# Step 5: Test team reproduction
# Person A runs experiment
python train.py --config config/baseline.yaml

# Person B (different machine) reproduces
git pull
dvc pull
docker build -t model:v1 .
docker run model:v1 --config config/baseline.yaml
```

### Expected Output

```
Step 1: MLflow Server Started
[2024-01-15 10:30:00] Listening on http://localhost:5000

Step 3: DVC Initialized
Initialized DVC repository.
To track data: dvc add <file>

Step 5: Reproduction Success
Person A result: Accuracy = 0.890
Person B result: Accuracy = 0.890
✓ Successfully reproduced across team members!
```

### Explanation

1. **Step 1**: Central tracking server (all team uses same)
2. **Step 2**: Standard project structure (consistency)
3. **Step 3**: Data versioning (exact data snapshots)
4. **Step 4**: Automated checks (enforce standards)
5. **Step 5**: Cross-person reproduction test

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Tooling without culture. Having MLflow doesn't mean people use it. Need process enforcement + buy-in.

- ⚠️ **Pitfall 2**: Over-automating too fast. Start with manual standards, automate once patterns are clear.

- ⚠️ **Pitfall 3**: One-size-fits-all. Reproducibility for research experiments vs. production models may have different requirements.

---

## Homework / Practice

1. **Exercise 1**: Design a "reproducibility score" for your team. What criteria would you measure? (0-100 scale)

2. **Exercise 2**: Draft a team policy: "All experiments must..." (list 5 requirements). Make it realistic, not aspirational.

3. **Stretch Goal**: Set up a local MLflow server, configure your project to log there, and run 3 experiments from different directories (simulate team members).

---

## Quick Quiz

1. **What's the main challenge of team-level reproducibility vs. individual?**
   - A) Team experiments are more complex
   - B) Different people, machines, and environments must all work
   - C) Teams have bigger datasets
   - D) It's actually easier with teams

2. **How does CI/CD help enforce reproducibility?**
   - A) It makes code run faster
   - B) It automatically checks standards (config exists, experiments logged, etc.)
   - C) It trains models automatically
   - D) It doesn't help with reproducibility

3. **True or False: Perfect tooling (MLflow, DVC, Docker) is enough to guarantee team reproducibility.**

<details>
<summary>Answers</summary>

1. **B** - Team reproducibility requires coordination across people, environments, and time
2. **B** - CI/CD can enforce standards through automated checks
3. **False** - Tooling is necessary but not sufficient. Need process, culture, and enforcement.

</details>

---

## Summary

- Team reproducibility requires: standards, tooling, automation, and culture
- Key tools: Central MLflow, DVC, Docker, project templates, CI/CD checks
- Processes: Experiment reviews, reproduction testing, documentation standards
- Culture shift: Reproducibility from "nice to have" to "non-negotiable"
- Maturity levels: Aim for Level 3 (enforced) or Level 4 (auditable)
- Success = anyone can reproduce any experiment, anytime, anywhere

---

## Next Steps

🎉 **Congratulations!** You've completed Section 6 - Reproducible Experimentation!

→ Continue to **Section 7** or revisit earlier sections for deeper understanding

---

## Additional Resources

- [ML Test Score: Reproducibility Checklist](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/45742.pdf)
- [ClearML: Team ML Experiment Management](https://clear.ml/)
- [Papers with Code: Reproducibility](https://paperswithcode.com/)
