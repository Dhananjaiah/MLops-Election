# Lecture 1.6 – Who Does What? (Data Engineer, ML Engineer, MLOps, DevOps, SRE, Product)

## In This Lecture You Will Learn

- [x] Clearly distinguish the responsibilities of each role in an ML team
- [x] Understand how roles collaborate and where handoffs occur
- [x] Identify which role owns which part of the ML system lifecycle

---

## Real-World Context

> **Story**: At a rapidly growing fintech company, a critical fraud detection model was delayed by 4 months. Why? Everyone assumed someone else was handling deployment.
>
> - Data Scientists said: "We trained the model, deployment is Engineering's job"
> - ML Engineers said: "We built the model pipeline, but infrastructure is DevOps' job"
> - DevOps said: "We don't know how to validate ML models, that's the ML team's job"
> - Product said: "Why isn't this live yet?!"
>
> The solution? A clear RACI matrix (Responsible, Accountable, Consulted, Informed) that defined exactly who does what. Once roles were clear, deployment took 3 weeks.

Understanding roles isn't about bureaucracy—it's about moving fast without dropping the ball.

---

## Main Content

### 1. The Cast of Characters

Let's meet the typical roles in an ML-enabled organization:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ML TEAM ROLES                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🔬 DATA SCIENTIST                                                          │
│     "I explore data and build models that solve business problems"          │
│     Focus: Experimentation, model selection, feature engineering            │
│                                                                              │
│  🛠️ ML ENGINEER                                                             │
│     "I turn prototypes into production-ready ML systems"                    │
│     Focus: Model optimization, training pipelines, model packaging          │
│                                                                              │
│  🚀 MLOPS ENGINEER                                                          │
│     "I ensure ML systems run reliably in production"                        │
│     Focus: Deployment, monitoring, automation, CI/CD for ML                 │
│                                                                              │
│  📊 DATA ENGINEER                                                            │
│     "I build the data infrastructure that feeds ML systems"                 │
│     Focus: Data pipelines, data quality, storage, ETL                       │
│                                                                              │
│  ⚙️ DEVOPS ENGINEER                                                          │
│     "I manage infrastructure and deployment automation"                     │
│     Focus: CI/CD, infrastructure as code, container orchestration           │
│                                                                              │
│  🛡️ SRE (Site Reliability Engineer)                                         │
│     "I ensure systems are reliable, scalable, and performant"               │
│     Focus: SLOs, incident response, capacity planning, on-call              │
│                                                                              │
│  📱 PRODUCT MANAGER                                                          │
│     "I define what we build and why it matters to the business"             │
│     Focus: Requirements, prioritization, success metrics, stakeholders      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Responsibility Matrix (RACI)

Who does what for each ML lifecycle phase?

| Phase | Data Scientist | ML Engineer | MLOps | Data Engineer | DevOps | Product |
|-------|----------------|-------------|-------|---------------|--------|---------|
| **Define Problem** | C | C | I | I | I | **R/A** |
| **Data Collection** | C | I | I | **R/A** | I | C |
| **Data Validation** | C | C | C | **R/A** | I | I |
| **Feature Engineering** | **R** | A | I | C | I | I |
| **Model Training** | **R/A** | C | I | I | I | I |
| **Model Evaluation** | **R/A** | C | I | I | I | C |
| **Model Packaging** | C | **R/A** | C | I | C | I |
| **Deployment** | I | C | **R/A** | I | C | I |
| **Monitoring Setup** | C | C | **R/A** | C | C | I |
| **Incident Response** | C | C | **R** | C | C | A |
| **Retraining** | C | **R** | A | C | I | I |

**Legend**: R = Responsible, A = Accountable, C = Consulted, I = Informed

### 3. Detailed Role Breakdown

#### **Data Scientist**

```
Primary Focus: "From business problem to validated model"

Day-to-Day Activities:
├── Exploratory Data Analysis (EDA)
├── Hypothesis testing
├── Feature engineering experiments
├── Model selection and training
├── Hyperparameter tuning
├── Model evaluation and interpretation
└── Communicating results to stakeholders

Handoffs:
├── TO Data Engineer: "I need this data in this format"
├── TO ML Engineer: "Here's a trained model ready for production"
└── TO Product: "Model achieves X accuracy, good for Y use case"

Tools:
├── Jupyter Notebooks
├── Python (scikit-learn, TensorFlow, PyTorch)
├── SQL for data exploration
└── Visualization tools (Matplotlib, Seaborn)
```

#### **ML Engineer**

```
Primary Focus: "From prototype to production-ready model"

Day-to-Day Activities:
├── Refactor notebook code to production code
├── Build reproducible training pipelines
├── Optimize model for inference (speed, memory)
├── Implement feature engineering in production
├── Create model packaging (Docker, APIs)
└── Write model tests and validation

Handoffs:
├── FROM Data Scientist: "Validated model ready for production"
├── TO MLOps: "Packaged model ready for deployment"
├── TO Data Engineer: "Feature pipeline requirements"
└── TO DevOps: "Infrastructure requirements"

Tools:
├── Python, Software engineering practices
├── Docker, Kubernetes basics
├── MLflow, experiment tracking
└── FastAPI, Flask for APIs
```

#### **MLOps Engineer**

```
Primary Focus: "Reliable ML systems in production"

Day-to-Day Activities:
├── Build CI/CD pipelines for ML
├── Deploy models to production
├── Set up monitoring and alerting
├── Implement automated retraining triggers
├── Manage model registry and versioning
└── Troubleshoot production ML issues

Handoffs:
├── FROM ML Engineer: "Packaged model ready for deployment"
├── TO SRE: "Model meets SLO requirements"
├── WITH Data Engineer: "Data pipeline health"
└── TO Product: "Model performance metrics"

Tools:
├── MLflow, Kubeflow, Metaflow
├── Kubernetes, Docker
├── Prometheus, Grafana
├── GitHub Actions, Jenkins
├── Evidently, Seldon, BentoML
```

#### **Data Engineer**

```
Primary Focus: "Reliable data infrastructure"

Day-to-Day Activities:
├── Build and maintain data pipelines
├── Ensure data quality and validation
├── Manage data storage (lakes, warehouses)
├── Implement data transformations
├── Optimize query performance
└── Handle data governance requirements

Handoffs:
├── TO Data Scientist: "Clean, validated data available"
├── TO ML Engineer: "Feature data in required format"
├── TO MLOps: "Data pipeline status and health"
└── FROM Product: "Data requirements for new features"

Tools:
├── Apache Spark, dbt
├── Airflow, Prefect, Dagster
├── SQL, Python
├── AWS/GCP/Azure data services
├── Great Expectations, Soda
```

#### **DevOps Engineer**

```
Primary Focus: "Infrastructure and deployment automation"

Day-to-Day Activities:
├── Manage CI/CD pipelines
├── Infrastructure as Code (Terraform, Pulumi)
├── Container orchestration (Kubernetes)
├── Security and access management
├── Cost optimization
└── General infrastructure support

Handoffs:
├── TO MLOps: "Infrastructure ready for ML workloads"
├── TO All Teams: "Deployment pipelines available"
├── FROM MLOps: "ML-specific infrastructure needs"
└── WITH SRE: "Reliability requirements"

Tools:
├── Kubernetes, Docker
├── Terraform, Ansible
├── GitHub Actions, GitLab CI
├── AWS/GCP/Azure cloud services
├── Monitoring tools (Prometheus, Datadog)
```

#### **SRE (Site Reliability Engineer)**

```
Primary Focus: "System reliability and performance"

Day-to-Day Activities:
├── Define and monitor SLOs/SLIs
├── Incident response and on-call
├── Capacity planning
├── Performance optimization
├── Post-mortem analysis
└── Chaos engineering

Handoffs:
├── TO All Teams: "SLO requirements and status"
├── FROM MLOps: "Model performance metrics"
├── WITH DevOps: "Infrastructure reliability"
└── TO Product: "Service availability reports"

Tools:
├── Prometheus, Grafana, Datadog
├── PagerDuty, OpsGenie
├── Kubernetes, cloud platforms
├── Custom monitoring solutions
```

#### **Product Manager**

```
Primary Focus: "Business value and priorities"

Day-to-Day Activities:
├── Define problem statements and success metrics
├── Prioritize ML initiatives
├── Stakeholder communication
├── Gather requirements
├── Track business impact
└── Make trade-off decisions

Handoffs:
├── TO Data Scientist: "Problem definition and success criteria"
├── FROM All Technical Roles: "Feasibility and timeline"
├── TO Stakeholders: "Progress and impact"
└── DECISIONS: "Priority, scope, trade-offs"

Tools:
├── Jira, Asana, Linear
├── Confluence, Notion
├── Data dashboards
├── Presentation tools
```

### 4. How Roles Collaborate

```
ML Project Workflow with Role Collaboration:
════════════════════════════════════════════

Phase 1: IDEATION
─────────────────
Product ────▶ "We need to predict customer churn"
    │
    ▼
Data Scientist ────▶ "Let me explore if this is feasible"
    │
    ▼
Data Engineer ────▶ "I'll prepare the customer data"


Phase 2: DEVELOPMENT
────────────────────
Data Scientist ────▶ "I've built a model with 85% accuracy"
    │
    ▼
ML Engineer ────▶ "I'll package this for production"
    │
    ▼
DevOps ────▶ "Here's the infrastructure you'll need"


Phase 3: DEPLOYMENT
───────────────────
ML Engineer ────▶ "Model is packaged and tested"
    │
    ▼
MLOps ────▶ "Deploying to production with monitoring"
    │
    ▼
SRE ────▶ "I'll ensure it meets our SLOs"


Phase 4: OPERATIONS
───────────────────
MLOps ────▶ "Model performance is dropping"
    │
    ├───▶ Data Engineer ────▶ "Data drift detected upstream"
    │
    └───▶ Data Scientist ────▶ "Need to retrain with new data"
              │
              ▼
          ML Engineer ────▶ "Triggering retraining pipeline"
```

---

## Diagrams

```
Responsibility Overlap Visualization:
═════════════════════════════════════

              DATA PIPELINE     MODEL BUILDING     DEPLOYMENT     OPERATIONS
              ─────────────     ──────────────     ──────────     ──────────

Data Engineer  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

Data Scientist ░░░░░░████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░

ML Engineer    ░░░░░░░░░░░░░░░░████████████████████████░░░░░░░░░░░░░░░░░

MLOps          ░░░░░░░░░░░░░░░░░░░░░░░░████████████████████████████████

DevOps         ░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████░░░░████████░░░░░░░░

SRE            ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████████████████████

Product        ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████

               ▲                                                        ▲
               │                                                        │
            Problem                                                  Business
            Definition                                               Impact
```

---

## Lab / Demo

### Prerequisites

- Completed Lectures 1.1-1.5
- Course repository cloned

### Step-by-Step Instructions

Let's map our project code to the roles that would typically own each part:

```bash
# Step 1: Create a role mapping document
cd project

echo "
=== ROLE MAPPING FOR CHURN PREDICTION PROJECT ===

📊 DATA ENGINEER would own:
- src/churn_mlops/data/__init__.py
  → Data loading, validation, schema definitions
  → Connects to: Data sources, data lake, databases

🔬 DATA SCIENTIST would own:
- src/churn_mlops/features/__init__.py
  → Feature engineering logic
  → Feature selection decisions
- Jupyter notebooks for exploration
  → notebooks/exploration_notebook_template.ipynb

🛠️ ML ENGINEER would own:
- src/churn_mlops/models/__init__.py
  → ChurnModel class implementation
- src/churn_mlops/models/train.py
  → Training pipeline code
- src/churn_mlops/models/inference.py
  → Inference wrapper for production

🚀 MLOPS ENGINEER would own:
- src/churn_mlops/serving/app.py
  → FastAPI model serving
- infra/ci/github-actions-mlops-pipeline.yml
  → CI/CD pipeline definitions
- config/config.yaml
  → Model and system configuration

⚙️ DEVOPS ENGINEER would own:
- Dockerfile
  → Container definitions
- docker-compose.yml
  → Local orchestration
- infra/k8s/k8s-manifests.yaml
  → Kubernetes deployment specs

📱 PRODUCT MANAGER would own:
- README.md (high-level docs)
- Business metric definitions
- Success criteria documentation
"

# Step 2: Count files per role
echo ""
echo "=== FILE COUNT BY ROLE ==="
echo "Data Engineer:    $(find src/churn_mlops/data -name '*.py' | wc -l) files"
echo "Data Scientist:   $(find src/churn_mlops/features -name '*.py' | wc -l) + notebooks"
echo "ML Engineer:      $(find src/churn_mlops/models -name '*.py' | wc -l) files"
echo "MLOps:            $(find src/churn_mlops/serving -name '*.py' | wc -l) + config files"
echo "DevOps:           $(ls Dockerfile docker-compose.yml 2>/dev/null | wc -l) + k8s manifests"
```

### Expected Output

```
=== ROLE MAPPING FOR CHURN PREDICTION PROJECT ===

📊 DATA ENGINEER would own:
- src/churn_mlops/data/__init__.py
  → Data loading, validation, schema definitions
  ...

=== FILE COUNT BY ROLE ===
Data Engineer:    1 files
Data Scientist:   1 + notebooks
ML Engineer:      3 files
MLOps:            2 + config files
DevOps:           2 + k8s manifests
```

### Explanation

1. We mapped each source file to the role that would typically own it
2. This shows how a real project has clear ownership boundaries
3. In a small team, one person might wear multiple hats, but ownership should still be defined

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Assuming one role can do everything. In startups, people wear multiple hats, but that's different from thinking "we don't need MLOps, the data scientist will handle deployment."

- ⚠️ **Pitfall 2**: Creating silos. Clear roles shouldn't mean people don't talk to each other. The best teams have clear ownership AND strong collaboration.

- ⚠️ **Pitfall 3**: Role titles vary by company. "ML Engineer" at Company A might be "Data Scientist" at Company B. Focus on responsibilities, not titles.

---

## Homework / Practice

1. **Exercise 1**: For your current project (or a hypothetical one), create a RACI matrix like the one above. Who is responsible for each phase?

2. **Exercise 2**: Interview someone in a different data role. What's their biggest frustration with cross-functional collaboration? What would make it better?

3. **Stretch Goal**: Research how Google, Netflix, or Uber structure their ML teams. Do they have separate MLOps roles, or is it distributed?

---

## Quick Quiz

1. **Who is typically responsible for building data pipelines that feed ML models?**
   - A) Data Scientist
   - B) ML Engineer
   - C) Data Engineer
   - D) Product Manager

2. **What's the main difference between ML Engineer and MLOps Engineer?**
   - A) ML Engineers use Python, MLOps Engineers don't
   - B) ML Engineers focus on model building/packaging, MLOps focuses on deployment/monitoring
   - C) They're the same role
   - D) MLOps Engineers only work on infrastructure

3. **True or False: In a startup, one person can reasonably cover all ML roles.**

<details>
<summary>Answers</summary>

1. **C** - Data Engineers own data infrastructure and pipelines
2. **B** - ML Engineers focus on model development; MLOps focuses on operationalizing models
3. **True** (with caveats) - In early stages, but as scale increases, specialization becomes necessary

</details>

---

## Summary

- ML teams typically include: Data Scientist, ML Engineer, MLOps Engineer, Data Engineer, DevOps, SRE, and Product Manager
- Clear role definitions prevent balls from being dropped ("I thought YOU were handling deployment!")
- Use RACI matrices to clarify who is Responsible, Accountable, Consulted, and Informed
- Roles overlap—especially ML Engineer and MLOps—and exact boundaries vary by company
- Even in small teams, clarifying ownership improves velocity and reduces confusion

---

## Next Steps

→ Continue to **Lecture 1.7**: Agenda of the Entire Course (What We'll Build Step by Step)

---

## Additional Resources

- [The Team Topologies Book](https://teamtopologies.com/) - Organizing teams for fast flow
- [Google's ML Roles](https://cloud.google.com/blog/products/ai-machine-learning/machine-learning-engineers-roles-and-skills) - Google's perspective
- [MLOps.community Role Discussions](https://mlops.community/) - Community debates on role definitions
