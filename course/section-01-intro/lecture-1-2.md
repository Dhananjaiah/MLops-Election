# Lecture 1.2 – What Is MLOps? In One Story, Not a Definition

## In This Lecture You Will Learn

- [x] Understand MLOps through a relatable real-world story, not abstract definitions
- [x] Identify the key problems that MLOps solves in production ML systems
- [x] Recognize the difference between ML in research/experimentation vs. ML in production

---

## Real-World Context

> **Story**: Let me tell you about DataCorp's $3 million disaster.
>
> DataCorp hired a brilliant data science team. Within 6 months, they built an amazing fraud detection model—99.2% accuracy on test data! The CEO was thrilled. "Ship it!" she said.
>
> Fast forward 3 months: The model was "deployed" (copied to a server by a data scientist at 2 AM). It worked... sometimes. No one knew when it last ran. Customer complaints about false fraud alerts tripled. The model was still using data from 6 months ago. When the original data scientist quit, no one could figure out how to retrain it.
>
> **Total cost**: $3 million in fraud losses + customer churn + engineering time trying to fix it.
>
> **The root cause?** They had Machine Learning, but no MLOps.

This story isn't unique—it happens at companies every day. MLOps exists to prevent exactly this scenario.

---

## Main Content

### 1. The One-Sentence Definition

**MLOps is the discipline of deploying, monitoring, and maintaining ML models in production reliably and efficiently.**

But that definition doesn't help you *understand* it. Let's use an analogy instead.

### 2. MLOps Through Analogy: The Restaurant Kitchen

Think of an ML model like a recipe:

| Cooking at Home | Running a Restaurant | ML Equivalent |
|-----------------|---------------------|---------------|
| Make dinner for family | Serve 500 customers/night | Research → Production |
| Recipe in your head | Standardized recipe cards | Notebook → Versioned code |
| Shop when you need ingredients | Supply chain management | Ad-hoc data → Data pipelines |
| Taste and adjust | Quality control process | Manual evaluation → Automated testing |
| Cook when hungry | Scheduled meal service | Manual runs → Automated pipelines |
| "It was good!" | Customer ratings, sales data | No monitoring → Production metrics |

**A home cook can make great food. But running a restaurant requires systems, processes, and discipline. That's MLOps for ML.**

### 3. What MLOps Actually Covers

```
┌────────────────────────────────────────────────────────────────────┐
│                        MLOps Responsibilities                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🔄 REPRODUCIBILITY                                                │
│     "Can we recreate this exact model 6 months from now?"         │
│     → Version control for code, data, and models                  │
│                                                                     │
│  📦 PACKAGING                                                      │
│     "How do we turn a script into something deployable?"          │
│     → Docker containers, Python packages, APIs                    │
│                                                                     │
│  🚀 DEPLOYMENT                                                     │
│     "How do we get the model to serve real users?"                │
│     → CI/CD pipelines, Kubernetes, cloud services                 │
│                                                                     │
│  📊 MONITORING                                                     │
│     "How do we know if the model is still working well?"          │
│     → Metrics, alerts, drift detection, dashboards                │
│                                                                     │
│  🔁 RETRAINING                                                     │
│     "How do we update the model when it gets stale?"              │
│     → Automated pipelines, triggered retraining                   │
│                                                                     │
│  🏛️ GOVERNANCE                                                     │
│     "Who approved this model? Can we explain its decisions?"      │
│     → Model registry, approvals, audit logs, explainability       │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### 4. MLOps is NOT About...

Let's clear up common misconceptions:

❌ **Building better models** - That's data science
❌ **Collecting more data** - That's data engineering  
❌ **Managing servers** - That's DevOps/SRE
❌ **Writing cleaner Python code** - That's software engineering

✅ **MLOps is the glue** that connects all of these disciplines to deliver reliable ML systems.

### 5. The "Two Cultures" Problem

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   DATA SCIENTIST WORLD          │    PRODUCTION WORLD           │
│   ─────────────────────         │    ────────────────           │
│                                 │                               │
│   • Jupyter notebooks           │    • Version-controlled code  │
│   • "It works on my machine"    │    • "It works everywhere"    │
│   • Manual experiments          │    • Automated pipelines      │
│   • Accuracy on test set        │    • Business metrics         │
│   • One-time analysis           │    • 24/7 availability        │
│   • "Let me try this..."        │    • "It's been tested"       │
│                                 │                               │
│           ╔═══════════════════════════════════╗                 │
│           ║                                   ║                 │
│           ║         MLOps Bridge              ║                 │
│           ║   Connects both worlds safely     ║                 │
│           ║                                   ║                 │
│           ╚═══════════════════════════════════╝                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Diagrams

```
The MLOps Lifecycle (Simplified)
═══════════════════════════════

    ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
    │  DATA   │────▶│  TRAIN  │────▶│ DEPLOY  │────▶│ MONITOR │
    └─────────┘     └─────────┘     └─────────┘     └─────────┘
         │                                               │
         │                                               │
         └───────────────── RETRAIN ◀────────────────────┘
                    (when monitoring detects issues)


Each stage has MLOps concerns:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DATA    → Is it versioned? Validated? Reproducible?
TRAIN   → Is training automated? Are experiments tracked?
DEPLOY  → Is deployment automated? Can we rollback?
MONITOR → Are we tracking the right metrics? Alerting?
```

---

## Lab / Demo

### Prerequisites

- Completed Lecture 1.1
- Access to the course repository

### Step-by-Step Instructions

In this lab, we'll examine a "before and after" comparison—what ML looks like without MLOps vs. with MLOps.

```bash
# Step 1: Look at a typical "notebook-only" approach
# (This is what we're trying to AVOID)

# Imagine a data scientist's folder:
# my_project/
# ├── model_v1.ipynb
# ├── model_v2_final.ipynb
# ├── model_v2_final_ACTUALLY_final.ipynb
# ├── model_v3_fixed.ipynb
# ├── data.csv
# └── data_new.csv

# Problems:
# - Which model is in production? 🤷
# - What data was used for which model? 🤷
# - How do we deploy any of these? 🤷

# Step 2: Now look at our MLOps project structure
cd project
tree -L 2 src/
# or: find src -maxdepth 2 -type f

# Step 3: Notice the organization
# src/
# └── churn_mlops/
#     ├── __init__.py      # Package definition
#     ├── data/            # Data loading & validation
#     ├── features/        # Feature engineering
#     ├── models/          # Training & inference
#     ├── serving/         # API endpoints
#     └── pipelines/       # Orchestration

# This structure is:
# ✅ Version controlled
# ✅ Testable
# ✅ Deployable
# ✅ Maintainable
```

### Expected Output

```
$ tree -L 2 src/
src/
└── churn_mlops
    ├── __init__.py
    ├── data
    ├── features
    ├── models
    ├── pipelines
    └── serving

6 directories, 1 file
```

### Explanation

1. **Step 1**: We recognize the chaos of unstructured ML projects (we've all been there!)
2. **Step 2**: We see how the course project is organized with MLOps principles
3. **Step 3**: Each module has a clear responsibility, making the system maintainable

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Thinking MLOps is only for big companies. Even a solo data scientist benefits from version control, automated testing, and deployment pipelines. Start small.

- ⚠️ **Pitfall 2**: Over-engineering too early. You don't need Kubernetes on day one. Start with good practices (versioning, testing) and add infrastructure as needed.

- ⚠️ **Pitfall 3**: Confusing MLOps with ML platform engineering. MLOps is about practices and processes. Platform engineering is about building the infrastructure. They overlap but aren't identical.

---

## Homework / Practice

1. **Exercise 1**: Think of a past ML project (school, work, or personal). List 3 things that would have been easier with MLOps practices.

2. **Exercise 2**: Find a public GitHub repository with ML code. Does it follow MLOps practices? Look for: tests, CI/CD config, Dockerfile, clear documentation.

3. **Stretch Goal**: Read Google's paper "Hidden Technical Debt in Machine Learning Systems" (2015). It's the foundational paper that sparked the MLOps movement.

---

## Quick Quiz

1. **Which of these is an MLOps responsibility?**
   - A) Building a more accurate model
   - B) Ensuring a deployed model can be monitored and retrained
   - C) Collecting more training data
   - D) Designing the model architecture

2. **What does the "restaurant kitchen" analogy illustrate?**
   - A) ML models are like food
   - B) The difference between one-time work and reliable operations at scale
   - C) Data scientists should become chefs
   - D) Restaurants use ML for recommendations

3. **True or False: MLOps is only relevant for companies with 100+ ML models in production.**

<details>
<summary>Answers</summary>

1. **B** - Deployment, monitoring, and retraining are core MLOps concerns
2. **B** - The analogy shows how operating at scale requires systems and processes
3. **False** - MLOps practices benefit projects of any size

</details>

---

## Summary

- MLOps is the discipline of reliably deploying, monitoring, and maintaining ML models in production
- The "restaurant kitchen" analogy: home cooking vs. running a restaurant = research ML vs. production ML
- MLOps covers: reproducibility, packaging, deployment, monitoring, retraining, and governance
- MLOps is the bridge between data science experiments and production systems
- You don't need to be a big company to benefit from MLOps practices

---

## Next Steps

→ Continue to **Lecture 1.3**: Why Do We Need MLOps? (From "Cool Model" → "Business Value")

---

## Additional Resources

- [Hidden Technical Debt in ML Systems](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) - The foundational paper
- [Google MLOps Guide](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) - Industry best practices
- [MLOps Community](https://mlops.community/) - Community resources and discussions
