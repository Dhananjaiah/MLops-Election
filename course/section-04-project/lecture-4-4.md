# Lecture 4.4 – High-Level Architecture for Our Project (Big Diagram)

## In This Lecture You Will Learn

- [x] Visualize the complete end-to-end architecture of our churn prediction system
- [x] Understand how different components interact in an MLOps pipeline
- [x] Identify where data flows from ingestion to prediction to monitoring

---

## Real-World Context

> **Story**: The VP of Engineering asked Priya to "just draw out the system" before her team started building. Priya resisted—"We don't have time for diagrams, let's just code!" Three months later, her team had built: a training script, a Flask API, a Docker image, and a Kubernetes deployment. But they didn't fit together. The API couldn't find the model. The training pipeline wrote to S3, but the API read from local disk. There was no monitoring. They spent 6 weeks "integrating" components that should have worked together from day one. A 2-hour architecture session would have saved 6 weeks of rework.

In the real world, skipping architecture design leads to fragmented systems that don't integrate cleanly. A clear architecture diagram is your blueprint—it aligns the team and prevents costly mistakes.

---

## Main Content

### 1. The Big Picture: End-to-End Architecture

Our churn prediction system has **5 major components**:

```
📊 Data Sources → 🔄 Data Pipeline → 🤖 Training Pipeline → 🚀 Serving → 📈 Monitoring
```

**Component 1: Data Sources** (Lecture 4.3)
- CRM, Usage Logs, Billing, Support
- Each with its own schema, update frequency, and access method

**Component 2: Data Pipeline**
- Extracts data from multiple sources
- Transforms and cleans raw data
- Loads into a feature store or data warehouse
- Runs daily or hourly (scheduled)

**Component 3: Training Pipeline**
- Reads features from feature store
- Trains/evaluates multiple models
- Logs experiments (MLflow/Weights & Biases)
- Registers best model to model registry
- Runs weekly or on-demand

**Component 4: Serving/Inference**
- REST API that loads model from registry
- Accepts customer features, returns churn probability
- Deployed as containerized service (Docker + Kubernetes)
- Handles 100-1000 requests/sec with <500ms latency

**Component 5: Monitoring & Feedback**
- Tracks model performance in production
- Detects data drift and model degradation
- Alerts when metrics drop below thresholds
- Feeds actual outcomes back for retraining

### 2. Detailed Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                   CHURN PREDICTION SYSTEM ARCHITECTURE                │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  1. DATA SOURCES                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  📊 CRM DB     📈 Usage Logs    💳 Billing    🎫 Support Tickets    │
└────────┬────────────┬────────────┬──────────────┬───────────────────┘
         │            │            │              │
         └────────────┴────────────┴──────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────────┐
│  2. DATA PIPELINE (Airflow / Prefect)                               │
├─────────────────────────────────────────────────────────────────────┤
│  Extract → Transform → Validate → Load                              │
│  - Join data from sources                                           │
│  - Engineer features (e.g., days_since_last_login)                  │
│  - Quality checks (missing values, outliers)                        │
│  - Store in Feature Store or Data Warehouse                         │
│                                                                      │
│  Schedule: Daily @ 2 AM                                             │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ↓
                    ┌────────────────┐
                    │ Feature Store  │
                    │   (S3/GCS)     │
                    └────────┬───────┘
                             │
         ┌───────────────────┼───────────────────┐
         ↓                   ↓                   ↓
┌────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ 3a. TRAINING   │  │ 3b. EXPERIMENT  │  │ 3c. MODEL       │
│    PIPELINE    │  │     TRACKING    │  │    REGISTRY     │
├────────────────┤  ├─────────────────┤  ├─────────────────┤
│ Train models   │→→│ Log to MLflow:  │→→│ Store models:   │
│ - Random Forest│  │ - Parameters    │  │ - Staging       │
│ - XGBoost      │  │ - Metrics       │  │ - Production    │
│ - LightGBM     │  │ - Artifacts     │  │ - Archived      │
│                │  │                 │  │                 │
│ Evaluate       │  │ Compare runs    │  │ Version control │
│ Select best    │  │ Select winner   │  │ A/B testing     │
└────────────────┘  └─────────────────┘  └────────┬────────┘
                                                   │
         Schedule: Weekly or on model drift       │
                                                   ↓
┌─────────────────────────────────────────────────────────────────────┐
│  4. MODEL SERVING (Kubernetes)                                      │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ API Pod 1    │  │ API Pod 2    │  │ API Pod 3    │            │
│  │ (FastAPI)    │  │ (FastAPI)    │  │ (FastAPI)    │            │
│  │ + Model v1.3 │  │ + Model v1.3 │  │ + Model v1.3 │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│          ↕                 ↕                  ↕                     │
│       [Load Balancer / Ingress]                                    │
│                    ↕                                                │
│        POST /predict {customer_id, features}                       │
│        → {churn_probability: 0.73}                                 │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│  5. MONITORING & FEEDBACK                                           │
├─────────────────────────────────────────────────────────────────────┤
│  📊 Prometheus + Grafana                                            │
│  - Latency, throughput, error rate                                 │
│  - Model prediction distribution                                    │
│  - Data drift detection                                             │
│                                                                      │
│  🔔 Alerting (PagerDuty / Slack)                                   │
│  - Model accuracy drops below 75%                                  │
│  - API latency > 1 second                                          │
│  - Data schema mismatch                                            │
│                                                                      │
│  🔄 Feedback Loop                                                   │
│  - Collect actual churn outcomes                                    │
│  - Label predictions (TP, FP, TN, FN)                              │
│  - Retrain trigger when drift detected                             │
└─────────────────────────────────────────────────────────────────────┘
```

### 3. Technology Stack Choices

| Component | Technology | Why? |
|-----------|------------|------|
| **Data Pipeline** | Apache Airflow | Industry standard for orchestration, great UI |
| **Feature Store** | AWS S3 + Parquet | Cost-effective, versioned, time-travel queries |
| **Experiment Tracking** | MLflow | Open source, model registry included |
| **Model Format** | Pickle / ONNX | Python-native, portable across frameworks |
| **API Framework** | FastAPI | High performance, auto-docs, async support |
| **Containerization** | Docker | Standard, works everywhere |
| **Orchestration** | Kubernetes | Auto-scaling, self-healing, battle-tested |
| **Monitoring** | Prometheus + Grafana | Open source, rich ecosystem |
| **CI/CD** | GitHub Actions | Integrated with code repo |

**Note**: These are our choices for this course. Real companies might use Azure ML, SageMaker, Vertex AI, or other managed services.

---

## Diagrams

![Diagram Placeholder](../../assets/diagrams/lecture-4-4-diagram.png)

> The complete architecture diagram is shown in ASCII above. The full color version should illustrate data flow from sources through pipelines to serving, with feedback loops back to training.

---

## Lab / Demo

### Prerequisites

- Completed Lectures 4.1-4.3
- Understanding of basic system design

### Step-by-Step Instructions

```bash
# Step 1: View the architecture diagram
cd project/docs
cat architecture.md

# Step 2: Review the technology stack decisions
cat tech_stack.md

# Step 3: Check the docker-compose file that runs the whole system locally
cd ..
cat docker-compose.yml

# Step 4: (Optional) Start the entire stack locally
docker-compose up -d
```

### Expected Output

```yaml
# docker-compose.yml shows all services:
services:
  postgres:          # Feature store database
  mlflow:            # Experiment tracking
  airflow:           # Data pipeline orchestration
  api:               # Model serving API
  prometheus:        # Metrics collection
  grafana:           # Monitoring dashboards
```

### Explanation

1. **Step 1**: Read the architecture documentation with detailed explanations
2. **Step 2**: Understand why each technology was chosen (trade-offs)
3. **Step 3**: See how all components are defined in infrastructure-as-code
4. **Step 4**: Run the entire system on your laptop to see it in action

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Over-engineering from day one. Start simple (even a cron job + Python script), then add complexity as needed. You don't need Kubernetes on day 1.

- ⚠️ **Pitfall 2**: Ignoring the monitoring component. Many teams build training + serving but forget monitoring. Then they don't know when models degrade.

- ⚠️ **Pitfall 3**: Tight coupling between components. If your API hardcodes the model path, you can't update models without redeploying the API. Use registries and loose coupling.

---

## Homework / Practice

1. **Exercise 1**: Redraw the architecture diagram by hand. This forces you to understand every component and connection.

2. **Exercise 2**: For each component in the architecture, list one failure mode and how we'd detect it. Example: "Data pipeline fails → feature store isn't updated → monitoring alerts on stale data."

3. **Stretch Goal**: Research an alternative architecture using cloud-managed services (AWS SageMaker, Azure ML, or GCP Vertex AI). What components are replaced? What stays the same?

---

## Quick Quiz

1. **What is the purpose of the model registry in our architecture?**
   - A) To store raw data
   - B) To version and manage trained models across environments
   - C) To serve predictions
   - D) To monitor model performance

2. **Which component is responsible for transforming raw data into features?**
   - A) Model serving API
   - B) MLflow
   - C) Data pipeline (Airflow)
   - D) Monitoring system

3. **True or False: The training pipeline and serving API should be tightly coupled for performance.**

<details>
<summary>Answers</summary>

1. **B** - The model registry stores, versions, and manages models as they move from staging to production
2. **C** - The data pipeline extracts, transforms, and loads data into the feature store
3. **False** - They should be loosely coupled. Training produces models in a registry; serving reads from the registry. This allows independent updates.

</details>

---

## Summary

- Our architecture has 5 major components: data sources, data pipeline, training pipeline, serving, and monitoring
- Data flows from sources → features → training → models → predictions → feedback
- We use open-source tools (Airflow, MLflow, FastAPI, Kubernetes, Prometheus) for learning
- Every component should be loosely coupled with clear interfaces
- Monitoring is not optional—it's how you know your system works

---

## Next Steps

→ Continue to **Lecture 4.5**: Where This Project Fits in a Real Company's Stack

---

## Additional Resources

- [Google: Machine Learning Systems Design](https://developers.google.com/machine-learning/crash-course/production-ml-systems)
- [MLOps Architecture Patterns (Databricks)](https://www.databricks.com/glossary/mlops)
- [AWS MLOps Reference Architecture](https://aws.amazon.com/architecture/ml-ops/)
