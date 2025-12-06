# Lecture 10.1 – CI/CD Basics Refresher (Build, Test, Deploy)

## In This Lecture You Will Learn

- [x] Understand the core concepts of Continuous Integration and Continuous Deployment
- [x] See how CI/CD applies to software development and sets the foundation for ML
- [x] Know the typical stages of a CI/CD pipeline and what happens in each

---

## Real-World Context

> **Story**: A fintech company was releasing their fraud detection model once a quarter. Each release was a "big bang" event: 2 weeks of manual testing, all-hands meetings, nervous deployment on Sunday nights. One bad release caused a 3-hour outage that cost $500,000.
>
> After implementing CI/CD, they deployed 50 times per month. Each deployment was small, tested automatically, and could be rolled back in minutes. The same engineer who used to spend nights deploying now sleeps peacefully while automation handles the work.

CI/CD transforms deployment from scary events into routine, safe operations.

---

## Main Content

### 1. What is CI/CD?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD FUNDAMENTALS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CI = CONTINUOUS INTEGRATION                                                │
│  ═══════════════════════════                                                │
│  "Every code change is automatically tested"                                │
│                                                                              │
│  What happens:                                                               │
│  1. Developer pushes code to Git                                            │
│  2. Automated system pulls the code                                         │
│  3. Runs tests (unit, integration)                                          │
│  4. Reports pass/fail                                                       │
│                                                                              │
│  Goal: Catch bugs early, prevent broken code from merging                   │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  CD = CONTINUOUS DEPLOYMENT/DELIVERY                                        │
│  ═══════════════════════════════════                                        │
│  "Every passing change is automatically deployed"                           │
│                                                                              │
│  Continuous Delivery:                                                        │
│  → Code is automatically prepared for release                               │
│  → Human approval required to deploy to production                          │
│                                                                              │
│  Continuous Deployment:                                                      │
│  → Code automatically deploys to production after passing tests             │
│  → No manual gates (for mature teams)                                       │
│                                                                              │
│  Goal: Get working code to users quickly and safely                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. The CI/CD Pipeline Stages

A typical pipeline has these stages:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD PIPELINE STAGES                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                          ┌─────────────────────────┐                        │
│                          │   1. SOURCE             │                        │
│                          │   (Git push/PR)         │                        │
│                          └───────────┬─────────────┘                        │
│                                      │                                       │
│                                      ▼                                       │
│                          ┌─────────────────────────┐                        │
│                          │   2. BUILD              │                        │
│                          │   - Install dependencies│                        │
│                          │   - Compile (if needed) │                        │
│                          │   - Create artifacts    │                        │
│                          └───────────┬─────────────┘                        │
│                                      │                                       │
│                                      ▼                                       │
│                          ┌─────────────────────────┐                        │
│                          │   3. TEST               │                        │
│                          │   - Unit tests          │                        │
│                          │   - Integration tests   │                        │
│                          │   - Linting/formatting  │                        │
│                          └───────────┬─────────────┘                        │
│                                      │                                       │
│                                      ▼                                       │
│                          ┌─────────────────────────┐                        │
│                          │   4. PACKAGE            │                        │
│                          │   - Build Docker image  │                        │
│                          │   - Push to registry    │                        │
│                          └───────────┬─────────────┘                        │
│                                      │                                       │
│                                      ▼                                       │
│                          ┌─────────────────────────┐                        │
│                          │   5. DEPLOY (Staging)   │                        │
│                          │   - Deploy to test env  │                        │
│                          │   - Run smoke tests     │                        │
│                          └───────────┬─────────────┘                        │
│                                      │                                       │
│                                      ▼                                       │
│                          ┌─────────────────────────┐                        │
│                          │   6. DEPLOY (Production)│                        │
│                          │   - Deploy to prod      │                        │
│                          │   - Monitor rollout     │                        │
│                          └─────────────────────────┘                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. CI/CD Tools Landscape

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD TOOLS COMPARISON                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TOOL              │ HOSTING        │ BEST FOR                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│  GitHub Actions    │ Cloud (GitHub) │ GitHub repos, free for public        │
│  GitLab CI         │ Cloud/Self     │ GitLab repos, all-in-one platform   │
│  Jenkins           │ Self-hosted    │ Complex pipelines, enterprise        │
│  CircleCI          │ Cloud          │ Fast builds, good caching            │
│  Travis CI         │ Cloud          │ Open source projects                 │
│  Azure DevOps      │ Cloud          │ Microsoft ecosystem                  │
│  AWS CodePipeline  │ Cloud (AWS)    │ AWS deployments                      │
│                                                                              │
│  OUR CHOICE: GitHub Actions                                                 │
│  ─────────────────────────                                                   │
│  Why:                                                                        │
│  • Free for public repos                                                    │
│  • Integrated with GitHub (our code host)                                   │
│  • YAML configuration (easy to read)                                        │
│  • Large marketplace of actions                                             │
│  • Industry standard                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. GitHub Actions Anatomy

A GitHub Actions workflow:

```yaml
# .github/workflows/ci.yml

name: CI Pipeline                        # Workflow name

on:                                      # TRIGGERS
  push:                                  # Run on push to these branches
    branches: [main, develop]
  pull_request:                          # Run on PRs to main
    branches: [main]
  workflow_dispatch:                     # Manual trigger button

env:                                     # ENVIRONMENT VARIABLES
  PYTHON_VERSION: '3.10'                 # Shared across all jobs

jobs:                                    # JOBS (run in parallel by default)
  test:                                  # Job name
    name: Run Tests                      # Display name
    runs-on: ubuntu-latest               # Runner (machine type)
    
    steps:                               # STEPS (run sequentially)
      - name: Checkout code              # Step 1
        uses: actions/checkout@v4        # Use a pre-built action
        
      - name: Set up Python              # Step 2
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          
      - name: Install dependencies       # Step 3
        run: |                           # Run shell commands
          pip install -r requirements.txt
          pip install pytest
          
      - name: Run tests                  # Step 4
        run: pytest tests/ -v
        
  lint:                                  # Second job (parallel)
    name: Lint Code
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install flake8
      - run: flake8 src/
        
  build:                                 # Third job (depends on test + lint)
    name: Build Docker
    runs-on: ubuntu-latest
    needs: [test, lint]                  # Wait for these jobs to pass
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .
```

### 5. CI/CD Best Practices

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD BEST PRACTICES                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1️⃣  FAST FEEDBACK                                                          │
│      • Aim for <10 minutes for CI                                           │
│      • Run fast tests first, slow tests later                               │
│      • Use caching for dependencies                                         │
│                                                                              │
│  2️⃣  FAIL FAST                                                              │
│      • Stop pipeline on first failure                                       │
│      • Clear error messages                                                 │
│      • Easy to see what broke                                               │
│                                                                              │
│  3️⃣  REPRODUCIBLE BUILDS                                                    │
│      • Pin dependency versions                                              │
│      • Use Docker for consistent environments                               │
│      • Same result every time                                               │
│                                                                              │
│  4️⃣  SECURE SECRETS                                                         │
│      • Never hardcode credentials                                           │
│      • Use GitHub Secrets                                                   │
│      • Rotate keys regularly                                                │
│                                                                              │
│  5️⃣  BRANCH PROTECTION                                                      │
│      • Require CI to pass before merge                                      │
│      • Require code review                                                  │
│      • No direct pushes to main                                             │
│                                                                              │
│  6️⃣  SMALL, FREQUENT CHANGES                                                │
│      • Smaller PRs = easier reviews                                         │
│      • Deploy often = less risk per deploy                                  │
│      • If it hurts, do it more often                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6. Our Project's CI Pipeline

Let's look at our actual CI configuration:

```yaml
# infra/ci/github-actions-mlops-pipeline.yml

name: MLOps CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    paths:
      - 'project/**'
  pull_request:
    branches: [main]
    paths:
      - 'project/**'

env:
  PYTHON_VERSION: '3.10'
  DOCKER_IMAGE: churn-prediction-api

jobs:
  # Stage 1: Test
  test:
    name: Test & Lint
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: project
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      - run: pip install -r requirements.txt
      - run: flake8 src --count --select=E9,F63,F7,F82 --show-source
      - run: PYTHONPATH=src pytest tests/ -v --cov=churn_mlops

  # Stage 2: Build (only if tests pass)
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          context: ./project
          push: false
          tags: ${{ env.DOCKER_IMAGE }}:${{ github.sha }}
```

---

## Diagrams

```
CI/CD Flow Visualization:
═════════════════════════

Developer                     CI/CD System                    Production
─────────                     ───────────                     ──────────

    │                              │                               │
    │  git push                    │                               │
    ├─────────────────────────────▶│                               │
    │                              │                               │
    │                    ┌─────────┴──────────┐                   │
    │                    │  Trigger Pipeline  │                   │
    │                    └─────────┬──────────┘                   │
    │                              │                               │
    │                    ┌─────────▼──────────┐                   │
    │                    │   Install deps     │                   │
    │                    │   Run tests        │                   │
    │                    │   Check linting    │                   │
    │                    └─────────┬──────────┘                   │
    │                              │                               │
    │                              │ Tests pass?                   │
    │                              │                               │
    │                    ┌─────────▼──────────┐                   │
    │◀───── Fail ────────│   NO → Notify      │                   │
    │                    │   developer        │                   │
    │                    └────────────────────┘                   │
    │                              │                               │
    │                              │ YES                           │
    │                              ▼                               │
    │                    ┌─────────────────────┐                   │
    │                    │   Build Docker      │                   │
    │                    │   Push to registry  │                   │
    │                    └─────────┬───────────┘                   │
    │                              │                               │
    │                              │                               │
    │                    ┌─────────▼──────────┐                   │
    │                    │  Deploy to staging │                   │
    │                    │  Run smoke tests   │                   │
    │                    └─────────┬──────────┘                   │
    │                              │                               │
    │                    ┌─────────▼──────────┐    Deploy         │
    │                    │  Deploy to prod    │──────────────────▶│
    │                    └────────────────────┘                   │
    │                                                              │
```

---

## Lab / Demo

### Prerequisites

- Completed Sections 1-9
- GitHub account
- Project pushed to a GitHub repository

### Step-by-Step Instructions

```bash
# Step 1: Look at our CI configuration
cd project
cat ../infra/ci/github-actions-mlops-pipeline.yml

# Step 2: Understand the structure
echo "
Our CI pipeline has these stages:
1. TEST: Run pytest and flake8
2. BUILD: Create Docker image
3. VALIDATE: Train model (on main branch)
4. DEPLOY: To staging then production (placeholders)
"

# Step 3: Simulate CI locally
echo "=== Running CI steps locally ==="

# Install dependencies (like CI does)
pip install -r requirements.txt

# Run linting (like CI does)
flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics || echo "Linting complete"

# Run tests (like CI does)
PYTHONPATH=src pytest tests/ -v

# Build Docker (like CI does)
docker build -t churn-api:local .

echo ""
echo "✅ All CI steps passed locally!"
echo "When you push to GitHub, CI runs these same steps automatically."

# Step 4: Check GitHub Actions (if repo exists)
echo "
To see your CI runs:
1. Go to your GitHub repo
2. Click 'Actions' tab
3. See workflow runs
"
```

### Expected Output

```
=== Running CI steps locally ===
Collecting numpy>=1.21.0...
Successfully installed numpy-1.24.0 pandas-2.0.3 ...

src/churn_mlops/data/__init__.py:1:1: E302 expected 2 blank lines
Linting complete

============================= test session starts =============================
tests/test_data.py::TestDataLoading::test_generate_sample_data PASSED
tests/test_models.py::TestChurnModel::test_fit PASSED
...
============================= 15 passed in 2.34s ==============================

Successfully built abc123def456
Successfully tagged churn-api:local

✅ All CI steps passed locally!
```

### Explanation

1. **Config review**: Understanding what CI does before it runs
2. **Local simulation**: Run CI steps locally to debug faster
3. **Linting**: Catches syntax errors and style issues
4. **Testing**: Validates code correctness
5. **Docker build**: Confirms the image can be created

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Slow CI pipelines. If CI takes 30 minutes, developers will skip it. Keep it under 10 minutes. Use caching and parallelization.

- ⚠️ **Pitfall 2**: Flaky tests. Tests that sometimes pass and sometimes fail destroy trust in CI. Fix or remove flaky tests immediately.

- ⚠️ **Pitfall 3**: "It works on my machine." Use Docker in CI to ensure consistent environments. Never rely on runner-specific configurations.

---

## Homework / Practice

1. **Exercise 1**: Create a simple GitHub Actions workflow that prints "Hello, MLOps!" on every push. File: `.github/workflows/hello.yml`

2. **Exercise 2**: Add a job to your workflow that checks if Python files are formatted with Black: `black --check src/`

3. **Stretch Goal**: Set up branch protection rules on GitHub requiring CI to pass before merge.

---

## Quick Quiz

1. **What does "Continuous Integration" mean?**
   - A) Deploying code continuously
   - B) Automatically testing every code change
   - C) Continuous code reviews
   - D) Running servers continuously

2. **In GitHub Actions, what is a "job"?**
   - A) A single shell command
   - B) A group of steps that run on the same runner
   - C) A trigger event
   - D) A workflow file

3. **True or False: CI should take as long as needed to run all possible tests.**

<details>
<summary>Answers</summary>

1. **B** - CI is about automatically testing every code change
2. **B** - A job is a set of steps running on one runner; jobs can run in parallel
3. **False** - CI should be fast (<10 min ideally) to maintain developer productivity

</details>

---

## Summary

- CI/CD automates testing and deployment, making releases safe and frequent
- CI = Automatic testing; CD = Automatic deployment
- Pipeline stages: Source → Build → Test → Package → Deploy
- GitHub Actions uses YAML to define workflows, jobs, and steps
- Best practices: fast feedback, fail fast, reproducible builds, secure secrets
- Run CI locally first to debug faster; push to GitHub for official CI

---

## Next Steps

→ Continue to **Lecture 10.2**: Extra Complexity in ML CI/CD (Data, Drift, Longer Runs)

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions) - Official reference
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions) - Pre-built actions
- [CI/CD Best Practices](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment) - Atlassian guide
