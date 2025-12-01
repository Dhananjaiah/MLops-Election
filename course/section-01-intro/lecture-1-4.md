# Lecture 1.4 – End-to-End ML System Architecture (From Data to Dashboard)

## In This Lecture You Will Learn

- [x] Visualize the complete architecture of a production ML system
- [x] Understand how data flows from source to prediction to monitoring
- [x] Identify the key components and their responsibilities in an ML system

---

## Real-World Context

> **Story**: When Spotify built their recommendation system, they didn't just train a model—they built an entire ecosystem. Data flows from billions of user interactions, through feature engineering pipelines, into model training systems, out to serving infrastructure that handles millions of requests per second, and back through monitoring systems that track recommendation quality. One engineer described it as "building a city, not a house."
>
> The difference between a toy project and a production system is this architecture. Understanding it is the first step to building real ML systems.

In the real world, you're not building a model—you're building a system with many interconnected parts.

---

## Main Content

### 1. The Big Picture: ML System as a Pipeline

Most people think ML looks like this:

```
Data → Model → Predictions  (Simple, but wrong)
```

In reality, a production ML system looks like this:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION ML SYSTEM ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   DATA LAYER              TRAINING LAYER           SERVING LAYER            │
│   ──────────              ──────────────           ─────────────            │
│                                                                              │
│   ┌─────────┐            ┌─────────────┐          ┌─────────────┐           │
│   │ Sources │            │ Experiment  │          │  Model API  │           │
│   │ (DBs,   │───────────▶│  Tracking   │─────────▶│  (FastAPI,  │           │
│   │  APIs,  │            │  (MLflow)   │          │  Flask)     │           │
│   │  Files) │            └─────────────┘          └─────────────┘           │
│   └─────────┘                  │                        │                   │
│        │                       │                        │                   │
│        ▼                       ▼                        ▼                   │
│   ┌─────────┐            ┌─────────────┐          ┌─────────────┐           │
│   │ Feature │            │   Model     │          │  Inference  │           │
│   │  Store  │            │  Registry   │          │   Engine    │           │
│   │         │            │             │          │             │           │
│   └─────────┘            └─────────────┘          └─────────────┘           │
│        │                       │                        │                   │
│        │                       │                        │                   │
│   ─────┴───────────────────────┴────────────────────────┴─────────────────  │
│                                                                              │
│                         OPERATIONS LAYER                                     │
│                         ────────────────                                     │
│                                                                              │
│       ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐      │
│       │ CI/CD     │    │ Monitoring│    │  Logging  │    │ Alerting  │      │
│       │ Pipelines │    │ Dashboards│    │  System   │    │  System   │      │
│       └───────────┘    └───────────┘    └───────────┘    └───────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Component Deep Dive

Let's understand each component:

#### **Data Layer**

| Component | Purpose | Tools (Examples) |
|-----------|---------|------------------|
| **Data Sources** | Raw data storage | PostgreSQL, S3, APIs, Kafka |
| **Data Pipeline** | Transform & validate | Airflow, dbt, Spark |
| **Feature Store** | Store reusable features | Feast, Tecton, Redis |
| **Data Validation** | Quality checks | Great Expectations, dbt tests |

```
Data Flow Example:
──────────────────

Raw Events → Kafka → Spark Processing → Feature Store → Training
     │                                        │
     │                                        └──────▶ Serving
     └──────▶ Data Lake (historical storage)
```

#### **Training Layer**

| Component | Purpose | Tools (Examples) |
|-----------|---------|------------------|
| **Experiment Tracking** | Log runs, params, metrics | MLflow, Weights & Biases, Neptune |
| **Training Pipeline** | Automated model training | Kubeflow, Airflow, SageMaker |
| **Model Registry** | Version & stage models | MLflow Registry, SageMaker |
| **Hyperparameter Tuning** | Optimize model params | Optuna, Ray Tune |

```
Training Pipeline Flow:
───────────────────────

┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Pull   │───▶│ Feature │───▶│  Train  │───▶│ Evaluate│───▶│ Register│
│  Data   │    │  Eng.   │    │  Model  │    │  Model  │    │ if Good │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
                                                                 │
                                                                 ▼
                                                          Model Registry
                                                          (v1.0, v1.1, v2.0)
```

#### **Serving Layer**

| Component | Purpose | Tools (Examples) |
|-----------|---------|------------------|
| **Model Server** | Serve predictions | FastAPI, TensorFlow Serving |
| **API Gateway** | Route & secure traffic | Kong, AWS API Gateway |
| **Load Balancer** | Distribute requests | NGINX, ALB |
| **Batch Inference** | Scheduled predictions | Spark, Airflow |

```
Serving Patterns:
─────────────────

REAL-TIME (Online)                    BATCH (Offline)
──────────────────                    ──────────────
                                      
User Request                          Scheduled Job
     │                                     │
     ▼                                     ▼
┌──────────┐                          ┌──────────┐
│   API    │                          │  Batch   │
│  Server  │                          │  Job     │
└──────────┘                          └──────────┘
     │                                     │
     ▼                                     ▼
┌──────────┐                          ┌──────────┐
│  Model   │                          │  Process │
│ Inference│                          │  All Data│
└──────────┘                          └──────────┘
     │                                     │
     ▼                                     ▼
Response                              Output File
(milliseconds)                        (Database/S3)
```

#### **Operations Layer**

| Component | Purpose | Tools (Examples) |
|-----------|---------|------------------|
| **CI/CD** | Automate deployment | GitHub Actions, GitLab CI |
| **Monitoring** | Track system health | Prometheus, Grafana |
| **Logging** | Capture events | ELK Stack, CloudWatch |
| **Alerting** | Notify on issues | PagerDuty, Slack webhooks |

### 3. Our Course Project Architecture

Here's what we'll build:

```
┌─────────────────────────────────────────────────────────────────┐
│               CUSTOMER CHURN PREDICTION SYSTEM                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     DATA PIPELINE                        │    │
│  │  Customer DB ──▶ ETL Script ──▶ Feature Engineering     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   TRAINING PIPELINE                      │    │
│  │  Processed Data ──▶ Train Model ──▶ Evaluate ──▶ Log    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    MODEL REGISTRY                        │    │
│  │  models/churn_model.pkl (version controlled)            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   SERVING LAYER                          │    │
│  │  FastAPI Server ──▶ Docker Container ──▶ Kubernetes     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  MONITORING & CI/CD                      │    │
│  │  GitHub Actions ──▶ Health Checks ──▶ Metrics           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4. How Components Communicate

```
Request Flow for a Single Prediction:
─────────────────────────────────────

1. User/App sends HTTP request
   POST /predict {"tenure": 24, "monthly_charges": 65.5, ...}
                    │
                    ▼
2. API Gateway receives request
   - Authentication ✓
   - Rate limiting ✓
   - Route to model service
                    │
                    ▼
3. Model Service processes
   - Validate input
   - Transform features
   - Load model (cached)
   - Run inference
                    │
                    ▼
4. Return prediction
   {"churn_probability": 0.73, "prediction": 1}
                    │
                    ▼
5. Log everything
   - Request/response logged
   - Latency recorded
   - Prediction stored for monitoring
```

---

## Diagrams

```
Component Responsibility Matrix:
════════════════════════════════

┌──────────────────┬─────────────────────────────────────────────┐
│    Component     │              Responsibility                 │
├──────────────────┼─────────────────────────────────────────────┤
│ Data Sources     │ Store raw business data                     │
│ Data Pipeline    │ Transform, validate, move data              │
│ Feature Store    │ Store computed features for reuse           │
│ Training System  │ Train models reproducibly                   │
│ Experiment Track │ Log experiments for comparison              │
│ Model Registry   │ Version and stage models                    │
│ Model Server     │ Serve predictions via API                   │
│ Monitoring       │ Track system and model health               │
│ CI/CD            │ Automate testing and deployment             │
│ Alerting         │ Notify humans when things go wrong          │
└──────────────────┴─────────────────────────────────────────────┘
```

---

## Lab / Demo

### Prerequisites

- Completed Lectures 1.1-1.3
- Course repository cloned

### Step-by-Step Instructions

Let's trace through our actual project code to see the architecture in action:

```bash
# Step 1: See the data layer
cd project/src/churn_mlops
ls data/
# __init__.py - Contains data loading and validation functions

# Step 2: See the feature engineering layer
ls features/
# __init__.py - Contains FeatureEngineer class and helper functions

# Step 3: See the training layer
ls models/
# __init__.py - ChurnModel class with fit, predict, save, load
# train.py - Training script
# inference.py - ChurnPredictor for serving

# Step 4: See the serving layer
ls serving/
# app.py - FastAPI application with /predict endpoint

# Step 5: See the operations layer (CI/CD)
cat ../../infra/ci/github-actions-mlops-pipeline.yml | head -50

# Step 6: Trace a prediction path
echo "
Data Flow in Our Project:
========================
1. data/__init__.py     → Load and validate data
2. features/__init__.py → Engineer features
3. models/train.py      → Train the model
4. models/__init__.py   → Save to models/churn_model.pkl
5. serving/app.py       → Serve via FastAPI at /predict
6. infra/ci/*.yml       → Automated deployment via GitHub Actions
"
```

### Expected Output

```
$ ls data/
__init__.py

$ ls models/
__init__.py  inference.py  train.py

$ ls serving/
__init__.py  app.py

Data Flow in Our Project:
========================
1. data/__init__.py     → Load and validate data
2. features/__init__.py → Engineer features
3. models/train.py      → Train the model
4. models/__init__.py   → Save to models/churn_model.pkl
5. serving/app.py       → Serve via FastAPI at /predict
6. infra/ci/*.yml       → Automated deployment via GitHub Actions
```

### Explanation

1. **Data layer**: The `data` module handles loading CSV files and generating sample data
2. **Feature layer**: The `features` module transforms raw data into model-ready features
3. **Training layer**: The `models` module contains the model class and training script
4. **Serving layer**: The `serving` module exposes the model as a REST API
5. **Operations**: GitHub Actions automates testing and deployment

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Building components in isolation. The data pipeline team builds their thing, the model team builds theirs, and they don't connect smoothly. Always design with integration in mind.

- ⚠️ **Pitfall 2**: Ignoring the "boring" parts. Logging, monitoring, and alerting aren't exciting, but they're what save you at 3 AM. Build them early.

- ⚠️ **Pitfall 3**: Over-engineering from day one. You don't need Kubernetes, feature stores, and real-time serving on day one. Start simple, evolve as needed.

---

## Homework / Practice

1. **Exercise 1**: Draw the architecture of an ML system you've worked with (or a hypothetical one). Identify which components exist and which are missing.

2. **Exercise 2**: For our Customer Churn project, identify what data would flow between each component. What format would it be in?

3. **Stretch Goal**: Research how Netflix, Spotify, or Uber structures their ML systems. What components do they have that we don't cover in this course?

---

## Quick Quiz

1. **What is the purpose of a Feature Store?**
   - A) Store raw data from various sources
   - B) Store computed features for reuse across training and serving
   - C) Store trained models
   - D) Store API endpoints

2. **What's the difference between online and batch serving?**
   - A) Online is faster hardware, batch is slower
   - B) Online serves individual predictions in real-time, batch processes many predictions on a schedule
   - C) Online uses the internet, batch doesn't
   - D) There's no difference

3. **True or False: Monitoring is optional for small ML systems.**

<details>
<summary>Answers</summary>

1. **B** - Feature stores enable feature reuse and consistency between training and serving
2. **B** - Online serving is real-time (milliseconds), batch serving is scheduled (hours/days)
3. **False** - Even small systems can fail silently; monitoring is always important

</details>

---

## Summary

- A production ML system has four main layers: Data, Training, Serving, and Operations
- Data flows from sources through pipelines to features to models to predictions
- Key components include: data pipelines, feature stores, experiment tracking, model registry, API servers, and monitoring
- Our course project implements a simplified but complete version of this architecture
- Start simple and evolve—you don't need every component on day one

---

## Next Steps

→ Continue to **Lecture 1.5**: Where Does MLOps Fit in the Overall Data/AI World?

---

## Additional Resources

- [Uber's Michelangelo Architecture](https://www.uber.com/blog/michelangelo-machine-learning-platform/) - Real-world ML platform
- [Google's TFX Paper](https://research.google/pubs/pub46484/) - Production ML pipelines
- [ML System Design Patterns](https://mercari.github.io/ml-system-design-pattern/) - Common architectural patterns
