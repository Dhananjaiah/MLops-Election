# Lecture 1.5 – Where Does MLOps Fit in the Overall Data/AI World?

## In This Lecture You Will Learn

- [x] Understand how MLOps relates to Data Engineering, DataOps, and AIOps
- [x] Map MLOps within the broader Data & AI technology landscape
- [x] Identify which skills and technologies overlap with adjacent disciplines

---

## Real-World Context

> **Story**: A Fortune 500 company hired a "Data Team" and gave them one goal: "Use AI to improve our business." Two years later, they had:
> - 3 Data Engineers building pipelines
> - 4 Data Scientists building models
> - 2 ML Engineers trying to deploy things
> - 1 DevOps person confused about what ML even is
> - 0 clear responsibility boundaries
> - $5M spent, 2 models in production
>
> The problem? Everyone was doing overlapping work, and critical gaps (like model monitoring) were no one's job. Once they mapped out the landscape and defined ownership, productivity tripled in 6 months.

Understanding where MLOps fits helps you know what to learn, who to collaborate with, and what falls outside your scope.

---

## Main Content

### 1. The Data & AI Technology Landscape

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     THE DATA & AI TECHNOLOGY LANDSCAPE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                           BUSINESS INTELLIGENCE                              │
│                           ─────────────────────                              │
│                           Dashboards, Reports, KPIs                          │
│                                     ▲                                        │
│                                     │                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        ANALYTICS & ML LAYER                          │    │
│  │                                                                      │    │
│  │    Data Science    │    ML Engineering    │    MLOps                │    │
│  │    ────────────    │    ──────────────    │    ─────                │    │
│  │    • Exploration   │    • Model building  │    • Deployment         │    │
│  │    • Experiments   │    • Feature eng.    │    • Monitoring         │    │
│  │    • Prototypes    │    • Optimization    │    • Automation         │    │
│  │                                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                     ▲                                        │
│                                     │                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                          DATA LAYER                                  │    │
│  │                                                                      │    │
│  │    Data Engineering    │    DataOps    │    Data Governance         │    │
│  │    ───────────────     │    ───────    │    ───────────────         │    │
│  │    • Pipelines         │    • Quality  │    • Privacy/Security      │    │
│  │    • ETL/ELT           │    • Testing  │    • Cataloging            │    │
│  │    • Storage           │    • CI/CD    │    • Compliance            │    │
│  │                                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                     ▲                                        │
│                                     │                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      INFRASTRUCTURE LAYER                            │    │
│  │                                                                      │    │
│  │    DevOps    │    SRE    │    Cloud Engineering    │    AIOps       │    │
│  │    ──────    │    ───    │    ─────────────────    │    ─────       │    │
│  │    • CI/CD   │    • SLAs │    • Cloud resources    │    • AI for    │    │
│  │    • IaC     │    • On-  │    • Kubernetes         │      IT Ops    │    │
│  │    • Deploy  │      call │    • Networking         │    • AIOps ≠   │    │
│  │              │           │                         │      MLOps!    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. MLOps vs. Similar Disciplines

Let's compare MLOps to commonly confused terms:

#### **MLOps vs. DevOps**

| Aspect | DevOps | MLOps |
|--------|--------|-------|
| **What changes** | Code | Code + Data + Models |
| **Versioning** | Git for code | Git + DVC + Model Registry |
| **Testing** | Unit, Integration, E2E | + Data validation, Model validation |
| **Deployment** | Deploy once, done | Deploy + Monitor + Retrain |
| **Feedback loop** | User feedback | + Model performance metrics |

**Key insight**: DevOps is a *subset* of MLOps. MLOps adds ML-specific concerns on top.

#### **MLOps vs. DataOps**

| Aspect | DataOps | MLOps |
|--------|---------|-------|
| **Focus** | Data pipeline quality | ML system operations |
| **Primary artifact** | Clean, reliable data | Deployed, monitored models |
| **Key metric** | Data freshness, accuracy | Model performance, latency |
| **Overlap** | Data validation, pipeline orchestration |

**Key insight**: DataOps ensures MLOps has good data to work with. They're complementary.

#### **MLOps vs. AIOps**

This one confuses everyone:

| Term | Meaning |
|------|---------|
| **MLOps** | Operations *for* ML systems (deploying ML models) |
| **AIOps** | Using ML *for* IT Operations (AI to monitor servers, predict outages) |

**Key insight**: They're almost opposites! MLOps deploys ML; AIOps uses ML.

### 3. The Venn Diagram of Data Roles

```
                    ┌───────────────────────────────────────────────┐
                    │                                               │
                    │              DATA SCIENTIST                   │
                    │           ─────────────────                   │
                    │           • Experiments                       │
                    │           • Model Selection                   │
                    │           • Statistical Analysis              │
                    │                                               │
           ┌────────┼────────────────────┬──────────────────────────┤
           │        │                    │                          │
           │        │     ┌──────────────┼──────────────────┐       │
           │        │     │              │                  │       │
           │   ML ENGINEER│         MLOps ENGINEER          │       │
           │   ───────────│         ──────────────          │       │
           │   • Model    │         • Deployment            │       │
           │     building │         • Monitoring            │       │
           │   • Feature  │         • Automation            │       │
           │     eng.     │         • CI/CD for ML          │       │
           │              │                                 │       │
     ┌─────┼──────────────┼─────────────────────────────────┼───────┤
     │     │              │                                 │       │
     │     │              │                                 │       │
     │     │   DATA       │                          DevOps │       │
     │     │   ENGINEER   │                          ────── │       │
     │     │   ─────────  │                          • CI/CD│       │
     │     │   • Pipelines│                          • IaC  │       │
     │     │   • ETL      │                          • K8s  │       │
     │     │   • Storage  │                                 │       │
     │     │              │                                 │       │
     └─────┴──────────────┴─────────────────────────────────┴───────┘
     
     Legend: Overlapping areas show shared responsibilities
```

### 4. Where MLOps Skills Come From

MLOps practitioners typically have backgrounds in one of these areas and learn the others:

| Background | Strengths | Gaps to Fill |
|------------|-----------|--------------|
| **Data Science** | ML concepts, Python, experiments | Infrastructure, deployment, monitoring |
| **Software Engineering** | Code quality, testing, APIs | ML concepts, data pipelines, model evaluation |
| **DevOps/SRE** | Infrastructure, CI/CD, monitoring | ML concepts, model-specific concerns |
| **Data Engineering** | Pipelines, data quality, storage | Model deployment, API development |

**The ideal MLOps person**: Knows enough of all four areas to build the bridge between them.

### 5. Technology Mapping

Where do common tools fit?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TECHNOLOGY MAPPING                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MLOPS SPECIFIC                                                              │
│  ─────────────                                                               │
│  • MLflow, Weights & Biases     (Experiment Tracking)                       │
│  • Kubeflow, Metaflow           (ML Pipelines)                              │
│  • Seldon, KServe               (Model Serving)                             │
│  • Evidently, WhyLabs           (Model Monitoring)                          │
│                                                                              │
│  SHARED WITH DEVOPS                                                          │
│  ─────────────────                                                           │
│  • Docker, Kubernetes           (Containerization)                          │
│  • GitHub Actions, GitLab CI    (CI/CD)                                     │
│  • Prometheus, Grafana          (Monitoring)                                │
│  • Terraform, Pulumi            (Infrastructure as Code)                    │
│                                                                              │
│  SHARED WITH DATA ENGINEERING                                                │
│  ───────────────────────────                                                 │
│  • Airflow, Prefect, Dagster    (Orchestration)                             │
│  • Spark, dbt                   (Data Processing)                           │
│  • Great Expectations, Soda     (Data Validation)                           │
│  • Feast, Tecton                (Feature Stores)                            │
│                                                                              │
│  SHARED WITH DATA SCIENCE                                                    │
│  ────────────────────────                                                    │
│  • scikit-learn, PyTorch        (Model Training)                            │
│  • Jupyter, VS Code             (Development)                               │
│  • Pandas, NumPy                (Data Manipulation)                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrams

```
Career Pathway to MLOps:
═══════════════════════

Data Scientist Path:
────────────────────
DS → Learn infrastructure basics → Learn CI/CD → MLOps

Software Engineer Path:
───────────────────────
SWE → Learn ML basics → Learn data pipelines → MLOps

DevOps Path:
────────────
DevOps → Learn ML concepts → Learn model-specific concerns → MLOps

Data Engineer Path:
───────────────────
DE → Learn ML basics → Learn deployment → MLOps

All paths converge at MLOps, bringing different strengths!
```

---

## Lab / Demo

### Prerequisites

- Completed Lectures 1.1-1.4
- Course repository cloned

### Step-by-Step Instructions

Let's identify which parts of our project align with which discipline:

```bash
# Step 1: Identify Data Engineering components
echo "=== DATA ENGINEERING COMPONENTS ==="
echo "These would typically be built by Data Engineers:"
ls project/src/churn_mlops/data/
echo "→ data/__init__.py contains: load_csv, validate_data, generate_sample_data"
echo ""

# Step 2: Identify Data Science components
echo "=== DATA SCIENCE COMPONENTS ==="
echo "These would typically be built by Data Scientists:"
ls project/src/churn_mlops/features/
ls project/src/churn_mlops/models/__init__.py
echo "→ features/ contains: FeatureEngineer, create_derived_features"
echo "→ models/ contains: ChurnModel class with fit, predict, evaluate"
echo ""

# Step 3: Identify DevOps components
echo "=== DEVOPS COMPONENTS ==="
echo "These would typically be built by DevOps Engineers:"
ls project/Dockerfile
ls project/docker-compose.yml
ls infra/ci/
ls infra/k8s/
echo "→ Dockerfile, docker-compose.yml: Containerization"
echo "→ CI pipeline, K8s manifests: Deployment infrastructure"
echo ""

# Step 4: Identify MLOps-specific components
echo "=== MLOPS-SPECIFIC COMPONENTS ==="
echo "These bridge all the above:"
ls project/src/churn_mlops/serving/
ls project/src/churn_mlops/models/train.py
ls project/src/churn_mlops/models/inference.py
echo "→ serving/app.py: Model API"
echo "→ train.py: Reproducible training pipeline"
echo "→ inference.py: Production inference wrapper"
```

### Expected Output

```
=== DATA ENGINEERING COMPONENTS ===
These would typically be built by Data Engineers:
__init__.py
→ data/__init__.py contains: load_csv, validate_data, generate_sample_data

=== DATA SCIENCE COMPONENTS ===
These would typically be built by Data Scientists:
__init__.py
__init__.py
→ features/ contains: FeatureEngineer, create_derived_features
→ models/ contains: ChurnModel class with fit, predict, evaluate

=== DEVOPS COMPONENTS ===
These would typically be built by DevOps Engineers:
project/Dockerfile
project/docker-compose.yml
github-actions-mlops-pipeline.yml
k8s-manifests.yaml
→ Dockerfile, docker-compose.yml: Containerization
→ CI pipeline, K8s manifests: Deployment infrastructure

=== MLOPS-SPECIFIC COMPONENTS ===
These bridge all the above:
__init__.py  app.py
train.py
inference.py
→ serving/app.py: Model API
→ train.py: Reproducible training pipeline
→ inference.py: Production inference wrapper
```

### Explanation

1. **Data Engineering**: Data loading and validation—getting clean data ready
2. **Data Science**: Feature engineering and model training—the ML core
3. **DevOps**: Infrastructure configuration—containers and deployment
4. **MLOps**: Ties everything together—serving, training pipelines, inference

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Assuming MLOps replaces other roles. It doesn't! MLOps works *alongside* Data Engineering, Data Science, and DevOps. It's a specialty, not a replacement.

- ⚠️ **Pitfall 2**: Confusing AIOps with MLOps. They're almost opposite things. If someone asks you about "AIOps," clarify whether they mean ML for IT or ops for ML.

- ⚠️ **Pitfall 3**: Trying to learn everything at once. Focus on MLOps core skills first, then deepen knowledge in adjacent areas based on your team's needs.

---

## Homework / Practice

1. **Exercise 1**: Look at job postings for "MLOps Engineer," "ML Engineer," and "Data Engineer." List the top 5 required skills for each. What overlaps?

2. **Exercise 2**: Draw a diagram of your current (or desired) company's data team structure. Where would MLOps fit?

3. **Stretch Goal**: Interview someone in a Data Engineering or DevOps role. Ask them: "What's the most frustrating thing about working with ML teams?" This reveals collaboration opportunities.

---

## Quick Quiz

1. **What's the main difference between MLOps and AIOps?**
   - A) MLOps is for machine learning, AIOps is for artificial intelligence
   - B) MLOps deploys ML systems, AIOps uses AI to manage IT systems
   - C) MLOps is newer than AIOps
   - D) They're the same thing

2. **Which discipline is most responsible for ensuring data quality before it reaches ML models?**
   - A) MLOps
   - B) DevOps
   - C) DataOps / Data Engineering
   - D) Data Science

3. **True or False: An MLOps engineer should have deep expertise in all areas (ML, DevOps, Data Engineering).**

<details>
<summary>Answers</summary>

1. **B** - MLOps is about operating ML systems; AIOps is about using AI for IT operations
2. **C** - DataOps and Data Engineering focus on data quality and pipelines
3. **False** - MLOps engineers need *working knowledge* of all areas but typically specialize in one while knowing enough of the others to collaborate effectively

</details>

---

## Summary

- MLOps sits at the intersection of Data Science, Data Engineering, DevOps, and Software Engineering
- MLOps is NOT the same as AIOps (opposite meanings!)
- MLOps extends DevOps with ML-specific concerns: data versioning, model monitoring, retraining
- DataOps is complementary—it ensures MLOps has quality data to work with
- Most MLOps practitioners come from one background (DS, SWE, DevOps, DE) and learn the others

---

## Next Steps

→ Continue to **Lecture 1.6**: Who Does What? (Data Engineer, ML Engineer, MLOps, DevOps, SRE, Product)

---

## Additional Resources

- [DataOps Manifesto](https://www.dataopsmanifesto.org/) - DataOps principles
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/) - Site Reliability Engineering practices
- [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar) - Industry technology trends
