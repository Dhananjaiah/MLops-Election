# Lecture 2.2 – Tech Stack Overview (Python, Git, Docker, CI/CD, Cloud/Kubernetes)

## In This Lecture You Will Learn

- [x] Understand every tool we'll use in this course and why we chose it
- [x] See how tools connect to form the complete MLOps stack
- [x] Know when to use which tool (decision framework)

---

## Real-World Context

> **Story**: A startup founder asked their new ML hire: "What tools do we need for MLOps?" The answer was a 47-item spreadsheet covering every possible tool in the ecosystem. Overwhelmed, they ended up with Kubernetes for a model that served 10 requests per day.
>
> The right answer? "Let me understand your scale and requirements first." This lecture teaches you a pragmatic, right-sized tech stack—tools that are industry-standard but not over-engineered for learning.

We'll use tools that 80% of companies use, so your skills will transfer to real jobs.

---

## Main Content

### 1. Our Tech Stack at a Glance

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COURSE TECH STACK                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LAYER           │ OUR CHOICE        │ ALTERNATIVES (INDUSTRY)              │
│  ──────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  Language        │ Python 3.10       │ (No real alternative for ML)         │
│                                                                              │
│  ML Framework    │ scikit-learn      │ TensorFlow, PyTorch, XGBoost         │
│                                                                              │
│  API Framework   │ FastAPI           │ Flask, Django, Starlette             │
│                                                                              │
│  Containerization│ Docker            │ Podman, containerd                   │
│                                                                              │
│  Version Control │ Git + GitHub      │ GitLab, Bitbucket, Azure DevOps      │
│                                                                              │
│  CI/CD           │ GitHub Actions    │ GitLab CI, Jenkins, CircleCI         │
│                                                                              │
│  Experiment Track│ MLflow            │ Weights & Biases, Neptune, Comet     │
│                                                                              │
│  Orchestration   │ Overview only     │ Airflow, Prefect, Kubeflow           │
│                                                                              │
│  Deployment      │ Docker Compose +  │ AWS ECS, Google Cloud Run            │
│                  │ K8s concepts      │ Azure Container Instances            │
│                                                                              │
│  Monitoring      │ Prometheus/Grafana│ Datadog, New Relic, CloudWatch       │
│                  │ concepts          │                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Tool-by-Tool Deep Dive

#### **Python 3.10+**

```
Why Python?
═══════════

• 90%+ of ML code is Python
• Rich ecosystem (pandas, NumPy, scikit-learn)
• Easy to learn, hard to master
• Industry standard—you'll use it everywhere

What We Use It For:
───────────────────
• Data processing
• Model training
• API development
• Testing
• Scripting/automation

Key Libraries We'll Use:
────────────────────────
├── pandas          → Data manipulation
├── numpy           → Numerical operations
├── scikit-learn    → Machine learning
├── fastapi         → Web APIs
├── pydantic        → Data validation
├── pytest          → Testing
└── pyyaml          → Configuration
```

#### **Git & GitHub**

```
Why Git/GitHub?
═══════════════

• Universal version control
• Collaboration standard
• GitHub Actions for CI/CD
• Free for public repos, cheap for private

What We Use It For:
───────────────────
• Code versioning
• Collaboration (PRs, reviews)
• CI/CD pipelines
• Documentation (READMEs, wikis)

Key Concepts We'll Cover:
─────────────────────────
├── Commits         → Save points
├── Branches        → Parallel work
├── Pull Requests   → Code review
├── Tags            → Release versioning
└── Actions         → Automated workflows
```

#### **Docker**

```
Why Docker?
═══════════

• "Works on my machine" → "Works everywhere"
• Package everything (code, dependencies, runtime)
• Industry standard for deployment
• Simple to learn core concepts

What We Use It For:
───────────────────
• Packaging our model API
• Consistent environments
• Deployment preparation
• Local testing

Key Concepts We'll Cover:
─────────────────────────
├── Images          → Blueprint (Dockerfile)
├── Containers      → Running instance
├── Registries      → Image storage
├── docker-compose  → Multi-container apps
└── Best practices  → Small images, security
```

#### **FastAPI**

```
Why FastAPI?
════════════

• Modern, fast, easy to learn
• Auto-generates API documentation
• Built-in data validation (Pydantic)
• Async support out of the box

What We Use It For:
───────────────────
• Serving model predictions
• Health check endpoints
• API documentation
• Request/response validation

Key Features We'll Use:
───────────────────────
├── @app.get/post   → HTTP endpoints
├── Pydantic models → Request validation
├── /docs           → Auto-generated Swagger
├── Background tasks→ Async processing
└── Middleware      → Logging, auth
```

#### **MLflow**

```
Why MLflow?
═══════════

• Open source (no vendor lock-in)
• Covers experiment tracking + model registry
• Easy to set up locally
• Integrates with most ML frameworks

What We Use It For:
───────────────────
• Logging experiments (params, metrics)
• Comparing model runs
• Model versioning
• Model registry (staging → production)

Key Components:
───────────────
├── Tracking        → Log experiments
├── Projects        → Package code
├── Models          → Model versioning
└── Registry        → Model lifecycle
```

#### **GitHub Actions**

```
Why GitHub Actions?
═══════════════════

• Free for public repos
• Integrated with GitHub (no separate setup)
• YAML-based configuration
• Huge marketplace of actions

What We Use It For:
───────────────────
• Running tests on every PR
• Building Docker images
• Deploying to staging/production
• Automating model training

Key Concepts We'll Cover:
─────────────────────────
├── Workflows       → Automation definition
├── Jobs            → Parallel work units
├── Steps           → Sequential commands
├── Triggers        → When to run (push, PR)
└── Secrets         → Secure credentials
```

#### **Kubernetes (Concepts Only)**

```
Why Learn Kubernetes Concepts?
══════════════════════════════

• Industry standard for container orchestration
• Scalability, reliability, self-healing
• Most MLOps job postings mention K8s
• Understanding concepts helps even if you use managed services

What We'll Cover:
─────────────────
• Core concepts (pods, services, deployments)
• YAML manifests
• Basic deployment patterns
• When K8s makes sense (and when it doesn't)

What We WON'T Cover (Out of Scope):
───────────────────────────────────
• Running your own K8s cluster
• Advanced networking
• Service mesh
• Custom controllers/operators
```

### 3. How Tools Connect

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HOW OUR TOOLS WORK TOGETHER                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                          ┌─────────────────┐                                │
│                          │  GitHub Repo    │                                │
│                          │  (Source Code)  │                                │
│                          └────────┬────────┘                                │
│                                   │                                          │
│                          ┌────────▼────────┐                                │
│                          │ GitHub Actions  │                                │
│                          │  (CI/CD)        │                                │
│                          └────────┬────────┘                                │
│                                   │                                          │
│              ┌────────────────────┼────────────────────┐                    │
│              │                    │                    │                    │
│              ▼                    ▼                    ▼                    │
│     ┌────────────────┐   ┌────────────────┐   ┌────────────────┐           │
│     │  Run Tests     │   │  Build Docker  │   │  Log to MLflow │           │
│     │  (pytest)      │   │  Image         │   │  (experiments) │           │
│     └────────────────┘   └────────┬───────┘   └────────────────┘           │
│                                   │                                          │
│                          ┌────────▼────────┐                                │
│                          │  Push to        │                                │
│                          │  Registry       │                                │
│                          └────────┬────────┘                                │
│                                   │                                          │
│                          ┌────────▼────────┐                                │
│                          │  Deploy to      │                                │
│                          │  K8s / Docker   │                                │
│                          └────────┬────────┘                                │
│                                   │                                          │
│                          ┌────────▼────────┐                                │
│                          │  FastAPI serves │                                │
│                          │  /predict       │                                │
│                          └─────────────────┘                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. Tool Selection Framework

How to choose tools in real projects:

| Factor | Questions to Ask |
|--------|-----------------|
| **Scale** | How many requests/day? How much data? |
| **Team** | How many people? What skills exist? |
| **Budget** | Free tier enough? Enterprise support needed? |
| **Integration** | Does it work with existing tools? |
| **Lock-in** | Can we migrate away if needed? |
| **Maturity** | Is it battle-tested or cutting-edge? |

**Our Course Choices:**

| Factor | Our Situation | Our Choice |
|--------|--------------|------------|
| Scale | Learning project, small | Docker Compose, local MLflow |
| Team | Solo learner | Simple tools, no complex setup |
| Budget | Free | All open-source tools |
| Integration | Learning stack | Tools that work together |
| Lock-in | Want transferable skills | Industry-standard tools |
| Maturity | Production-grade learning | Stable, well-documented |

---

## Diagrams

```
Tech Stack Decision Tree:
═════════════════════════

START: "I have ML code in a notebook"
        │
        ▼
Q1: "Do I need it to run outside my laptop?"
        │
    ├── NO → Keep the notebook (for now)
    │
    └── YES → Package as Python module
                │
                ▼
Q2: "Do others need to use it?"
        │
    ├── NO → CLI script is fine
    │
    └── YES → Build API (FastAPI)
                │
                ▼
Q3: "Does it need to run on different machines?"
        │
    ├── NO → Virtual environment is enough
    │
    └── YES → Docker container
                │
                ▼
Q4: "Does it need to handle many requests?"
        │
    ├── NO → Single container (Docker Compose)
    │
    └── YES → Container orchestration (Kubernetes)
                │
                ▼
Q5: "Does it need to update automatically?"
        │
    └── YES → CI/CD pipeline (GitHub Actions)

This course takes you through all these decisions!
```

---

## Lab / Demo

### Prerequisites

- Completed Lecture 2.1
- Computer ready

### Step-by-Step Instructions

Let's check what tools you already have installed:

```bash
# Step 1: Check Python
python --version
python3 --version

# Step 2: Check pip
pip --version
pip3 --version

# Step 3: Check Git
git --version

# Step 4: Check Docker (may not be installed yet)
docker --version
docker compose version

# Step 5: Summary script
echo "
╔══════════════════════════════════════════════════════════╗
║              TOOL INSTALLATION STATUS                     ║
╠══════════════════════════════════════════════════════════╣
"

# Python
if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
else
    echo "❌ Python: Not found"
fi

# pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip: $(pip3 --version | cut -d' ' -f2)"
else
    echo "❌ pip: Not found"
fi

# Git
if command -v git &> /dev/null; then
    echo "✅ Git: $(git --version | cut -d' ' -f3)"
else
    echo "❌ Git: Not found"
fi

# Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker: $(docker --version | cut -d' ' -f3 | tr -d ',')"
else
    echo "⚠️  Docker: Not found (will install in Lecture 2.3)"
fi

echo "
╚══════════════════════════════════════════════════════════╝
"
```

### Expected Output

```
╔══════════════════════════════════════════════════════════╗
║              TOOL INSTALLATION STATUS                     ║
╠══════════════════════════════════════════════════════════╣
✅ Python: Python 3.10.8
✅ pip: 23.0.1
✅ Git: 2.39.0
⚠️  Docker: Not found (will install in Lecture 2.3)
╚══════════════════════════════════════════════════════════╝
```

### Explanation

1. **Python/pip**: Already needed for Lecture 2.1 assessment
2. **Git**: Most systems have it; we'll configure it properly
3. **Docker**: We'll install in Lecture 2.3—don't worry if missing

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Tool overwhelm. You don't need to master every tool before starting. We learn them as we need them.

- ⚠️ **Pitfall 2**: Chasing the newest tool. Stick with stable, well-documented tools. New ≠ better for production.

- ⚠️ **Pitfall 3**: Over-engineering. A FastAPI server with Docker Compose handles more traffic than most ML projects will ever see. Start simple.

---

## Homework / Practice

1. **Exercise 1**: Research one alternative for each tool in our stack. Why might a company choose it over our choice?

2. **Exercise 2**: Find 3 MLOps job postings. List the tools they mention. How many overlap with our stack?

3. **Stretch Goal**: Try to explain our tech stack to a non-technical friend. Can you describe what Docker does in one sentence?

---

## Quick Quiz

1. **Why do we use FastAPI instead of Flask?**
   - A) FastAPI is older and more stable
   - B) FastAPI has auto-documentation and built-in validation
   - C) Flask doesn't support Python
   - D) FastAPI is the only option for ML

2. **When would you NOT need Kubernetes?**
   - A) When serving millions of requests per day
   - B) When you need auto-scaling
   - C) When a single Docker container handles your load
   - D) When deploying to production

3. **True or False: You must install all tools before starting the course.**

<details>
<summary>Answers</summary>

1. **B** - FastAPI provides automatic API docs and Pydantic validation
2. **C** - K8s adds complexity; use it when you actually need scaling
3. **False** - We install tools progressively as we need them

</details>

---

## Summary

- Our stack: Python, Git, Docker, FastAPI, MLflow, GitHub Actions, K8s concepts
- Each tool was chosen for being: industry-standard, open-source, well-documented
- Tools connect: Code → Git → CI/CD → Docker → Deploy → Monitor
- Use the decision framework: don't over-engineer for your scale
- You don't need to master everything before starting—learn as you go

---

## Next Steps

→ Continue to **Lecture 2.3**: Setting Up Local Dev Environment

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Excellent official docs
- [Docker Get Started](https://docs.docker.com/get-started/) - Official Docker tutorial
- [MLflow Quickstart](https://mlflow.org/docs/latest/quickstart.html) - Official MLflow guide
- [GitHub Actions Docs](https://docs.github.com/en/actions) - CI/CD documentation
