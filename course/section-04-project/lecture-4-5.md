# Lecture 4.5 – Where This Project Fits in a Real Company's Stack

## In This Lecture You Will Learn

- [x] Understand how our churn project fits into a larger enterprise ML platform
- [x] Identify what infrastructure already exists vs. what we build
- [x] Recognize that this is one ML system among many in a real company

---

## Real-World Context

> **Story**: Kumar joined a Fortune 500 company excited to build ML systems. On day one, he learned they already had: a data lake, a feature platform, a model registry, Kubernetes clusters, CI/CD pipelines, monitoring stacks, and 40 other ML models in production. His job wasn't to build all that—it was to build *his* churn model using the existing platform. He spent the first month learning what already existed, who owned each piece, and how to plug his model into the ecosystem. The lesson: in real companies, you're rarely building from scratch. You're integrating with existing systems.

In the real world, especially at larger companies, there's already a "ML Platform" team that provides shared infrastructure. Your job is to build your ML use case on top of that platform, not reinvent every component.

---

## Main Content

### 1. The Enterprise ML Platform Landscape

In a mature company, the full stack looks like this:

```
┌─────────────────────────────────────────────────────────────────┐
│               ENTERPRISE ML PLATFORM (Shared)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Infrastructure Layer (Platform Team owns)                      │
│  ├─ Kubernetes Clusters (Dev, Staging, Prod)                   │
│  ├─ Container Registry (Docker images)                         │
│  ├─ Secret Management (Vault, AWS Secrets Manager)             │
│  ├─ Networking & Load Balancers                                │
│  └─ Logging & Monitoring (ELK, Prometheus, Grafana)            │
│                                                                  │
│  Data Platform (Data Engineering owns)                          │
│  ├─ Data Lake (S3, ADLS, GCS)                                  │
│  ├─ Data Warehouse (Snowflake, BigQuery, Redshift)             │
│  ├─ Data Catalog (Collibra, Alation)                           │
│  ├─ ETL Orchestration (Airflow, Prefect)                       │
│  └─ Feature Store (Feast, Tecton, in-house)                    │
│                                                                  │
│  ML Platform (ML Platform Team owns)                            │
│  ├─ Experiment Tracking (MLflow, Weights & Biases)             │
│  ├─ Model Registry (MLflow, SageMaker)                         │
│  ├─ Training Infrastructure (GPU clusters, Kubeflow)            │
│  ├─ Model Serving Framework (Seldon, KFServing)                │
│  └─ ML Monitoring (Evidently, Arize)                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                          ↑ Our Project Uses This ↑
                          
┌─────────────────────────────────────────────────────────────────┐
│          OUR CHURN PREDICTION PROJECT (We own)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ Data Pipeline for Churn Features                            │
│  ✅ Churn Model Training Code                                   │
│  ✅ Churn Prediction API                                        │
│  ✅ Churn-specific Business Logic                               │
│  ✅ Churn Model Monitoring Dashboards                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. What We Build vs. What Already Exists

**What the Platform Provides (We Don't Build)**:
- Kubernetes clusters for deployment
- MLflow for experiment tracking
- Centralized feature store
- CI/CD pipelines (templates)
- Monitoring infrastructure (Prometheus, Grafana)
- Authentication & authorization systems
- Log aggregation
- Model serving templates

**What We Build (Our Responsibility)**:
- Churn-specific feature engineering logic
- Model training scripts (using our algorithm choices)
- Model evaluation criteria (what makes a good churn model?)
- Prediction API endpoints (business logic for our use case)
- Custom dashboards for churn metrics
- Integration tests for our service

**What We Share with Platform Team**:
- Performance requirements (need GPU for training?)
- SLA requirements (99.9% uptime?)
- Compliance needs (PII handling, data residency)
- Capacity planning (expected request volume)

### 3. Multiple ML Systems Coexisting

Our churn model is just ONE of many ML systems:

| Team | ML Use Case | Same Platform? |
|------|-------------|----------------|
| Marketing | Product recommendation engine | ✅ Yes |
| Fraud | Transaction fraud detection | ✅ Yes |
| Customer Service | Ticket routing & prioritization | ✅ Yes |
| Sales | Lead scoring | ✅ Yes |
| **Us** | **Customer churn prediction** | **✅ Yes** |
| Finance | Revenue forecasting | ✅ Yes |
| Operations | Demand forecasting | ✅ Yes |

**Why This Matters**:
- We don't get to choose the infrastructure (already decided)
- We share compute resources (need to be efficient)
- We follow company-wide standards (coding, security, monitoring)
- We coordinate deployments (can't break the platform for others)
- We learn from other teams' best practices

**Example Scenario**:
- The fraud team already solved model versioning with MLflow
- We don't invent our own system; we use theirs
- The recommendation team has a pattern for A/B testing
- We adopt their pattern for consistency
- The lead scoring team wrote documentation on the feature store
- We read it before reinventing their wheels

---

## Diagrams

```
┌──────────────────────────────────────────────────────────────────┐
│                   Company-Wide View                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Infrastructure Platform (SRE/Platform Team)                     │
│  └─ Kubernetes, Networking, Storage, Security                    │
│                     ↑                                             │
│  ML Platform (ML Platform Team)                                  │
│  └─ Feature Store, Model Registry, Serving, Monitoring           │
│                     ↑                                             │
│  ┌─────────────────┴────────────────────────────┐               │
│  │                                                │               │
│  │  Churn    Fraud     Recommender    Lead      │               │
│  │  Model    Model     Model          Scoring   │               │
│  │  (Us!)    Team      Team           Team      │               │
│  │                                                │               │
│  └────────────────────────────────────────────────┘              │
│            Individual ML Projects                                 │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-4-5-diagram.png)

> Diagram shows our churn project sitting on top of shared ML and infrastructure platforms, alongside other ML projects

---

## Lab / Demo

### Prerequisites

- Completed Lectures 4.1-4.4
- Understanding of shared vs. dedicated infrastructure

### Step-by-Step Instructions

```bash
# Step 1: Review the platform documentation
cd project/docs
cat platform_overview.md

# Step 2: Check what platform services are available
cat platform_services.yaml

# Step 3: See how to integrate with the feature store
cat examples/feature_store_integration.py

# Step 4: Review platform SLA and support
cat platform_sla.md
```

### Expected Output

```yaml
# platform_services.yaml
available_services:
  compute:
    - kubernetes_dev_cluster
    - kubernetes_prod_cluster
    - gpu_nodes: 10
  
  ml_services:
    - mlflow_server: https://mlflow.company.internal
    - model_registry: centralized
    - feature_store: feast_v0.24.0
  
  monitoring:
    - prometheus: https://prometheus.company.internal
    - grafana: https://grafana.company.internal
    - alertmanager: configured
  
  data:
    - data_warehouse: snowflake
    - data_lake: s3://company-data-lake
```

### Explanation

1. **Step 1**: Learn what infrastructure and services already exist
2. **Step 2**: Identify which services we'll use for our churn project
3. **Step 3**: See code examples for integrating with platform services
4. **Step 4**: Understand support processes and SLAs from the platform team

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Reinventing the wheel. Before building something, ask: "Does the platform already provide this?" Often it does, and your custom solution will be inferior.

- ⚠️ **Pitfall 2**: Ignoring platform standards. You might think your way is better, but non-standard systems become unmaintainable when you leave or the platform evolves.

- ⚠️ **Pitfall 3**: Not engaging with platform teams early. Tell them your requirements in month 1, not month 6 when you're about to deploy and discover they don't support your needs.

---

## Homework / Practice

1. **Exercise 1**: List 5 components from our architecture (Lecture 4.4). For each, decide: would this be provided by a platform team in a real company, or would we build it?

2. **Exercise 2**: Imagine you join a company with an established ML platform. Write 5 questions you'd ask the platform team in your first week to understand what's available.

3. **Stretch Goal**: Research a real ML platform offering (AWS SageMaker, Azure ML, Databricks, Vertex AI). What components does it provide? How would our churn project architecture change if we used it?

---

## Quick Quiz

1. **In a large enterprise, who typically owns the Kubernetes cluster where ML models run?**
   - A) Each ML team owns their own cluster
   - B) The ML Platform or Infrastructure team provides shared clusters
   - C) The data engineering team
   - D) Nobody—everyone uses their own VMs

2. **What should you do before building a custom tool for your ML project?**
   - A) Build it immediately to save time
   - B) Check if the ML platform team already provides it
   - C) Ask for a bigger budget
   - D) Hire a consultant

3. **True or False: In real companies, ML projects typically build everything from scratch.**

<details>
<summary>Answers</summary>

1. **B** - Platform/Infrastructure teams provide shared Kubernetes clusters for all ML projects
2. **B** - Always check what already exists before building custom solutions
3. **False** - ML projects integrate with existing platforms; building from scratch is rare at established companies

</details>

---

## Summary

- In real companies, there's usually a shared ML platform providing infrastructure, data, and ML tools
- Our churn project builds on top of this platform, not from scratch
- Platform provides: Kubernetes, feature store, model registry, monitoring
- We build: churn-specific features, model code, business logic, API endpoints
- Multiple ML teams share the same platform—coordination and standards matter
- Always check what exists before building custom solutions

---

## Next Steps

→ Continue to **Lecture 4.6**: What We Will Automate vs What Will Stay Manual

---

## Additional Resources

- [Uber's Michelangelo ML Platform](https://eng.uber.com/michelangelo-machine-learning-platform/)
- [Netflix ML Infrastructure](https://netflixtechblog.com/machine-learning-at-netflix-a-journey-into-ml-infrastructure-5b27d22b12b4)
- [Airbnb's ML Platform](https://medium.com/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70)
