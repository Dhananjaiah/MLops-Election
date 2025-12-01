# Lecture 1.7 – Agenda of the Entire Course (What We'll Build Step by Step)

## In This Lecture You Will Learn

- [x] Get a comprehensive overview of all 15 sections of this course
- [x] Understand what you'll build in each section and how sections connect
- [x] Plan your learning journey based on your goals and timeline

---

## Real-World Context

> **Story**: When learning to fly a plane, you don't just jump in the cockpit. First, you see the full curriculum: ground school, simulator training, supervised flights, solo flights, and finally your license. Knowing the full journey helps you stay motivated when individual lessons get tough.
>
> This course is your flight training for MLOps. This lecture is your curriculum overview—see the whole journey before we take off.

Having a clear roadmap prevents the "when will this ever end?" feeling and helps you connect each topic to the bigger picture.

---

## Main Content

### 1. Course Journey Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        YOUR MLOPS LEARNING JOURNEY                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   WEEK 1: FOUNDATION                                                         │
│   ══════════════════                                                         │
│   Section 1: Welcome & Big Picture ────▶ "What is MLOps?"                   │
│   Section 2: Prerequisites & Setup ────▶ "Let's get ready"                  │
│   Section 3: ML Lifecycle ─────────────▶ "How ML projects work"             │
│                                                                              │
│   WEEK 2: PROJECT & DATA                                                     │
│   ══════════════════════                                                     │
│   Section 4: Project Overview ─────────▶ "Our churn prediction case"        │
│   Section 5: Data Engineering ─────────▶ "Getting data ready for ML"        │
│   Section 6: Experimentation ──────────▶ "Reproducible experiments"         │
│                                                                              │
│   WEEK 3: PACKAGING                                                          │
│   ═════════════════                                                          │
│   Section 7: Model Packaging ──────────▶ "Script → Package → API"           │
│   Section 8: Versioning & Registry ────▶ "Track everything"                 │
│   Section 9: Training Pipelines ───────▶ "Automated training"               │
│                                                                              │
│   WEEK 4: DEPLOYMENT                                                         │
│   ══════════════════                                                         │
│   Section 10: CI/CD for ML ────────────▶ "Automated deployment"             │
│   Section 11: Deployment Patterns ─────▶ "Kubernetes & serving"             │
│   Section 12: Monitoring ──────────────▶ "Know when things break"           │
│                                                                              │
│   WEEK 5: MASTERY                                                            │
│   ═══════════════                                                            │
│   Section 13: Governance ──────────────▶ "Security & compliance"            │
│   Section 14: Capstone ────────────────▶ "Everything together"              │
│   Section 15: Career ──────────────────▶ "Land your MLOps job"              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Section-by-Section Breakdown

#### **Section 1: Welcome, Agenda & Big Picture** (This Section!)
*Where you are now*

| Lecture | Topic | What You'll Learn |
|---------|-------|-------------------|
| 1.1 | Course Welcome | How to use this course effectively |
| 1.2 | What Is MLOps? | MLOps through stories, not definitions |
| 1.3 | Why We Need MLOps | The business case for operationalizing ML |
| 1.4 | ML System Architecture | End-to-end system overview |
| 1.5 | MLOps in Context | Where MLOps fits in the data world |
| 1.6 | Roles & Responsibilities | Who does what in ML teams |
| 1.7 | Course Agenda | This lecture! |
| 1.8 | Project Sneak Peek | Preview what we're building |

**By the end**: You understand MLOps and are excited to build!

---

#### **Section 2: Prerequisites, Tools & Environment Setup**
*Get your development environment ready*

| Lecture | Topic | What You'll Build |
|---------|-------|-------------------|
| 2.1 | Skills Needed | Self-assessment of prerequisites |
| 2.2 | Tech Stack Overview | Understand our tooling choices |
| 2.3 | Local Dev Setup | Python, VS Code, Docker installed |
| 2.4 | Project Structure | Create the project skeleton |
| 2.5 | Python Packages | Set up requirements.txt, venv |
| 2.6 | Git Basics | Branching, PRs, tags |
| 2.7 | Running Labs | How to follow along |
| 2.8 | Troubleshooting | Fix common setup issues |

**By the end**: Your machine is ready to code!

---

#### **Section 3: Understanding the ML Lifecycle**
*How ML projects work in real organizations*

| Lecture | Topic | Key Concept |
|---------|-------|-------------|
| 3.1 | Problem Framing | Business problem → ML problem |
| 3.2 | CRISP-DM | Classic ML lifecycle methodology |
| 3.3 | Where Things Break | Why notebooks fail in production |
| 3.4 | MLOps vs DevOps | Similarities and differences |
| 3.5 | Online vs Batch | Different serving patterns |
| 3.6 | MLOps Responsibilities | Your job at each stage |

**By the end**: You understand the full ML lifecycle and where MLOps fits!

---

#### **Section 4: Course Project Overview**
*Introducing our Customer Churn Prediction project*

| Lecture | Topic | What You'll Define |
|---------|-------|-------------------|
| 4.1 | Use Case Definition | Why churn prediction matters |
| 4.2 | Business Requirements | Success metrics and KPIs |
| 4.3 | Data Sources | What data we'll use |
| 4.4 | High-Level Architecture | System design diagram |
| 4.5 | Real Company Context | How this fits in enterprises |
| 4.6 | Automation Scope | What to automate vs. keep manual |

**By the end**: Clear project scope and architecture defined!

---

#### **Section 5: Data Engineering Basics for MLOps**
*Getting data ready for ML systems*

| Lecture | Topic | What You'll Build |
|---------|-------|-------------------|
| 5.1 | Data Types & Storage | Understand CSV, Parquet, databases |
| 5.2 | Data Ingestion | Loading data from various sources |
| 5.3 | Data Quality | Validation with Great Expectations |
| 5.4 | Feature Engineering | Create model-ready features |
| 5.5 | Feature Stores | Store and serve features |
| 5.6 | Responsibility Boundaries | Where DE ends and MLOps starts |

**By the end**: Data loading and validation code working!

---

#### **Section 6: Reproducible Experimentation**
*From chaos to systematic experiments*

| Lecture | Topic | What You'll Build |
|---------|-------|-------------------|
| 6.1 | Reproducibility Ladder | Levels of reproducibility |
| 6.2 | Notebook Problems | Why notebooks break |
| 6.3 | Experiment Structure | Organized experiment folders |
| 6.4 | Tracking Concepts | Runs, params, metrics, artifacts |
| 6.5 | MLflow Tracking | Log experiments with MLflow |
| 6.6 | End-to-End Reproduction | Same code → same model |
| 6.7 | Team Enforcement | MLOps role in reproducibility |

**By the end**: MLflow experiment tracking set up!

---

#### **Section 7: Model Packaging**
*From script to deployable service*

| Lecture | Topic | What You'll Build |
|---------|-------|-------------------|
| 7.1 | Python Packages | Reusable churn_mlops package |
| 7.2 | Clean Inference | The predict() function |
| 7.3 | REST API | FastAPI model service |
| 7.4 | Docker Introduction | Container fundamentals |
| 7.5 | Dockerizing the Model | Production-ready Docker image |
| 7.6 | Local API Testing | curl, Postman tests |

**By the end**: Model running as a Docker container with API!

---

#### **Section 8: Data & Model Versioning**
*Track everything, reproduce anything*

| Lecture | Topic | What You'll Build |
|---------|-------|-------------------|
| 8.1 | Why Versioning Matters | The reproducibility problem |
| 8.2 | Git + DVC | Code and data versioning |
| 8.3 | Model Registry | MLflow Model Registry |
| 8.4 | Model States | Staging → Production → Archived |
| 8.5 | Artifact Storage | Store models and artifacts |
| 8.6 | Governance Basics | Approval workflows |

**By the end**: Model registry with staged model versions!

---

#### **Section 9: Automated Training Pipelines**
*Orchestrate model training*

| Lecture | Topic | What You'll Build |
|---------|-------|-------------------|
| 9.1 | Why Pipelines | Problems with manual execution |
| 9.2 | Pipeline Building Blocks | Tasks, steps, DAGs |
| 9.3 | Orchestrators Overview | Airflow, Prefect, Kubeflow |
| 9.4 | Pipeline Design | Design our training pipeline |
| 9.5 | Pipeline Implementation | Build with chosen tool |
| 9.6 | Scheduling & Retries | Handle failures gracefully |
| 9.7 | Team Boundaries | MLOps vs. Data Engineering |

**By the end**: Automated training pipeline running!

---

#### **Section 10: CI/CD for ML Systems**
*Automated testing and deployment*

| Lecture | Topic | What You'll Build |
|---------|-------|-------------------|
| 10.1 | CI/CD Basics | Build, test, deploy refresher |
| 10.2 | ML CI/CD Complexity | What's different for ML |
| 10.3 | ML Testing | Unit, integration, model tests |
| 10.4 | Docker in CI | Build images automatically |
| 10.5 | Continuous Delivery | Staging → Production |
| 10.6 | Blue/Green & Canary | Safe deployment strategies |
| 10.7 | Rollbacks | When deployments go wrong |

**By the end**: GitHub Actions CI/CD pipeline working!

---

#### **Section 11: Deployment Architectures**
*Get models to production*

| Lecture | Topic | What You'll Learn |
|---------|-------|-------------------|
| 11.1 | Serving Patterns | Online vs. batch vs. near-real-time |
| 11.2 | API Architectures | Monolith vs. microservice |
| 11.3 | Deployment Options | VM vs. managed vs. Kubernetes |
| 11.4 | Kubernetes Basics | Pods, services, ingress |
| 11.5 | Model Serving Frameworks | Seldon, KServe, BentoML |
| 11.6 | Our Deployment Pattern | Final architecture choice |

**By the end**: Model deployed to Kubernetes!

---

#### **Section 12: Monitoring, Observability & Model Health**
*Know when things go wrong*

| Lecture | Topic | What You'll Build |
|---------|-------|-------------------|
| 12.1 | What to Monitor | Infra, app, model metrics |
| 12.2 | System Metrics | Latency, errors, throughput |
| 12.3 | Model Metrics | Drift, skew, degradation |
| 12.4 | Logging & Tracing | Debug production issues |
| 12.5 | Dashboards | Grafana monitoring setup |
| 12.6 | Alerting | PagerDuty/Slack notifications |
| 12.7 | Feedback Loops | Trigger retraining |
| 12.8 | Cost Optimization | Efficient resource usage |

**By the end**: Full monitoring dashboard with alerts!

---

#### **Section 13: Governance, Security & Responsible MLOps**
*Production-grade practices*

| Lecture | Topic | Key Practice |
|---------|-------|--------------|
| 13.1 | Access Control | Secrets management |
| 13.2 | Compliance | PII, GDPR, audit logs |
| 13.3 | Explainability | Model cards, interpretability |
| 13.4 | Approval Workflows | Model promotion gates |
| 13.5 | Data Requests | Handle "delete my data" |
| 13.6 | Team Best Practices | Organizational patterns |

**By the end**: Governance policies documented and implemented!

---

#### **Section 14: End-to-End Capstone**
*Putting it all together*

| Lecture | Topic | What You'll Do |
|---------|-------|----------------|
| 14.1 | Final Architecture | Review complete system |
| 14.2 | Code Walkthrough | Understand every component |
| 14.3 | Full Pipeline Run | Data → Training → Deploy → Monitor |
| 14.4 | Failure Scenarios | Debug common issues |
| 14.5 | Interview Prep | Present your project |
| 14.6 | Enterprise Context | How this scales |

**By the end**: Complete, working MLOps system!

---

#### **Section 15: Career, Interviews & Next Steps**
*Land your MLOps role*

| Lecture | Topic | What You'll Prepare |
|---------|-------|---------------------|
| 15.1 | Job Roles | Titles and expectations |
| 15.2 | Interview Stories | How to tell your MLOps story |
| 15.3 | Portfolio Building | What recruiters want |
| 15.4 | Project Extensions | Feature stores, A/B testing |
| 15.5 | Learning Path | LLMOps, Advanced MLOps |

**By the end**: Ready for MLOps job applications!

---

### 3. What You'll Build (Cumulative View)

```
Your Project Evolution:
═══════════════════════

Section 2:  📁 Empty project folder
            └── pyproject.toml, requirements.txt

Section 4:  📁 + Project documentation
            └── Architecture diagrams, requirements

Section 5:  📁 + Data layer
            └── src/churn_mlops/data/

Section 6:  📁 + Experiments
            └── notebooks/, mlflow experiments

Section 7:  📁 + Model & API
            └── src/churn_mlops/models/, serving/
            └── Dockerfile

Section 8:  📁 + Model registry
            └── MLflow model versions

Section 9:  📁 + Pipeline
            └── Training pipeline code

Section 10: 📁 + CI/CD
            └── .github/workflows/

Section 11: 📁 + K8s deployment
            └── infra/k8s/

Section 12: 📁 + Monitoring
            └── Prometheus, Grafana configs

Section 14: 📁 COMPLETE SYSTEM! 🎉
            └── Everything working together
```

---

## Diagrams

```
Course Dependency Graph:
═══════════════════════

              ┌─────────────────┐
              │ Section 1       │
              │ (Big Picture)   │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Section 2       │
              │ (Setup)         │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Section 3       │
              │ (ML Lifecycle)  │
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
┌────────▼────┐ ┌──────▼──────┐ ┌────▼────────┐
│ Section 4   │ │ Section 5   │ │ Section 6   │
│ (Project)   │ │ (Data)      │ │ (Experiments│
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
              ┌────────▼────────┐
              │ Section 7       │
              │ (Packaging)     │
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
┌────────▼────┐ ┌──────▼──────┐ ┌────▼────────┐
│ Section 8   │ │ Section 9   │ │ Section 10  │
│ (Versioning)│ │ (Pipelines) │ │ (CI/CD)     │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
┌────────▼────┐ ┌──────▼──────┐ ┌────▼────────┐
│ Section 11  │ │ Section 12  │ │ Section 13  │
│ (Deployment)│ │ (Monitoring)│ │ (Governance)│
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
              ┌────────▼────────┐
              │ Section 14      │
              │ (Capstone)      │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Section 15      │
              │ (Career)        │
              └─────────────────┘
```

---

## Lab / Demo

### Prerequisites

- Course repository cloned
- Completed lectures 1.1-1.6

### Step-by-Step Instructions

Let's preview what we'll build by exploring the existing project structure:

```bash
# Step 1: See the complete project structure
cd project
find . -type f -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "Dockerfile" | head -30

# Step 2: Preview the code we'll write
echo "=== FILES WE'LL BUILD ==="
echo ""
echo "Section 5 (Data):"
head -20 src/churn_mlops/data/__init__.py
echo ""
echo "Section 7 (API):"
head -20 src/churn_mlops/serving/app.py
echo ""
echo "Section 10 (CI/CD):"
head -20 ../infra/ci/github-actions-mlops-pipeline.yml

# Step 3: Preview the final system
echo ""
echo "=== FINAL SYSTEM COMPONENTS ==="
echo "1. Data Layer:     src/churn_mlops/data/"
echo "2. Features:       src/churn_mlops/features/"
echo "3. Models:         src/churn_mlops/models/"
echo "4. Serving API:    src/churn_mlops/serving/app.py"
echo "5. Docker:         Dockerfile, docker-compose.yml"
echo "6. CI/CD:          infra/ci/github-actions-mlops-pipeline.yml"
echo "7. Kubernetes:     infra/k8s/k8s-manifests.yaml"
echo "8. Configuration:  config/config.yaml"
echo ""
echo "This is what you'll understand deeply by the end!"
```

### Expected Output

```
=== FILES WE'LL BUILD ===

Section 5 (Data):
"""
Data Loading Module
===================
...

Section 7 (API):
"""
FastAPI Application for Churn Prediction
========================================
...

Section 10 (CI/CD):
# MLOps CI/CD Pipeline Template
# ==============================
...

=== FINAL SYSTEM COMPONENTS ===
1. Data Layer:     src/churn_mlops/data/
2. Features:       src/churn_mlops/features/
...
```

### Explanation

1. We previewed the actual code we'll build throughout the course
2. Each component corresponds to specific sections
3. By the end, you'll understand every line of this code

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Skipping sections. Each section builds on the previous. If you skip Section 7 (Packaging), Section 10 (CI/CD) won't make sense because there's nothing to deploy.

- ⚠️ **Pitfall 2**: Rushing through labs. The labs are where real learning happens. Budget 2x the video time for hands-on practice.

- ⚠️ **Pitfall 3**: Not taking quizzes. Quizzes reveal gaps in understanding. A 70% quiz score means you should review before moving on.

---

## Homework / Practice

1. **Exercise 1**: Print the COURSE_OVERVIEW.md file. Highlight the 5 lectures you're most excited about and the 5 you're most nervous about.

2. **Exercise 2**: Create a study schedule. If you have 10 hours/week, how long will the course take? (Hint: ~50-60 hours total)

3. **Stretch Goal**: Find a study buddy or accountability partner. Share your schedule and check in weekly on progress.

---

## Quick Quiz

1. **Which section covers deploying models to Kubernetes?**
   - A) Section 7 (Model Packaging)
   - B) Section 10 (CI/CD)
   - C) Section 11 (Deployment)
   - D) Section 14 (Capstone)

2. **When do we start working on the hands-on project?**
   - A) Section 1
   - B) Section 4
   - C) Section 7
   - D) Section 14

3. **True or False: You can skip Section 3 (ML Lifecycle) if you already know the basics.**

<details>
<summary>Answers</summary>

1. **C** - Section 11 covers Kubernetes and deployment architectures
2. **B** - Section 4 introduces our project; Section 5+ builds it
3. **False** - Section 3 provides context that's referenced throughout the course. Even if you know the basics, it's worth reviewing.

</details>

---

## Summary

- This course has 15 sections organized into 5 weeks: Foundation, Project & Data, Packaging, Deployment, Mastery
- Each section builds on the previous—follow them in order
- By the end, you'll have a complete, production-ready ML system
- The project evolves from empty folder to deployed, monitored system
- Budget 50-60 hours total; more if you dive deep into extensions

---

## Next Steps

→ Continue to **Lecture 1.8**: Sneak Peek: Our End-to-End MLOps Project (What We're Building)

---

## Additional Resources

- [COURSE_OVERVIEW.md](../../COURSE_OVERVIEW.md) - Full syllabus with all lecture titles
- [project/README.md](../../project/README.md) - Project setup instructions
- [Study Tips for Technical Courses](https://www.coursera.org/articles/how-to-study) - Learning strategies
