# Lecture 5.6 – Where Data Engineer Ends and MLOps Starts (Responsibility Boundaries)

## In This Lecture You Will Learn

- [x] Understand where data engineering responsibilities end and MLOps begins
- [x] Identify collaboration points and shared ownership between teams
- [x] Navigate organizational boundaries effectively to avoid conflicts

---

## Real-World Context

> **Story**: A heated Slack thread: "Who's responsible for fixing the broken `customer_age` feature?" Data Engineer: "I just move data from A to B—feature logic is ML's job." ML Engineer: "We use the features, we don't build the pipelines!" Two weeks of finger-pointing, meanwhile production predictions are wrong. The resolution: a RACI matrix (Responsible, Accountable, Consulted, Informed). Data Engineering owns raw data pipelines and quality. ML/MLOps owns feature engineering and model transformations. Shared ownership of the feature store infrastructure. Clear boundaries saved future conflicts.

In the real world, most ML/data problems are actually organizational problems. Clarify ownership early, or suffer collaboration hell later.

---

## Main Content

### 1. Typical Responsibility Boundaries

**Data Engineering Owns:**
- 📊 **Raw data ingestion** from source systems (CRM, databases, APIs)
- 🏗️ **Data warehouse/data lake infrastructure** (S3, Snowflake, BigQuery setup)
- ✅ **Data quality for RAW data** (schema validation, completeness checks)
- 🔄 **Core ETL pipelines** (extract, load, basic transformations)
- 📚 **Data cataloging and governance** (what data exists, where, who owns it)
- 🔐 **Data access control** (who can read which datasets)

**MLOps Owns:**
- 🧪 **Feature engineering** (transforming raw data into ML features)
- 🤖 **Model training pipelines** (orchestrating training jobs)
- 🚀 **Model serving infrastructure** (APIs, containers, Kubernetes)
- 📈 **Model monitoring and retraining** (drift detection, performance tracking)
- 🔍 **ML-specific data quality** (distribution drift, feature drift, training/serving skew)
- 📦 **Model artifact management** (model registry, versioning)

**Shared Ownership** (Both Collaborate):
- 🏪 **Feature store** (Data Eng builds infrastructure, MLOps defines features)
- 📝 **Data contracts** (Data Eng provides data, ML specifies requirements)
- ⚠️ **Data quality SLAs** (both monitor, both get alerted)
- 🐛 **Incident response** (joint debugging when pipelines break)

### 2. Collaboration Points

**At Project Kickoff**:
- MLOps: "We need customer demographics, usage logs, and billing data"
- Data Eng: "Demographics are in PostgreSQL, usage in S3, billing in Stripe API"
- Together: Agree on data contracts, update frequency, SLAs

**During Development**:
- MLOps builds feature engineering code
- Data Eng reviews for performance implications on warehouse
- MLOps needs new data source → Data Eng assesses feasibility

**During Operations**:
- Data quality alert fires → Both investigate
- Data Eng: "The source system changed schema"
- MLOps: "Our feature code needs updating"
- Together: Fix and deploy

**At Feature Store**:
- Data Eng: Provisions infrastructure (databases, S3 buckets, access control)
- MLOps: Writes feature definitions and transformation code
- Data Eng: Ensures feature pipelines don't overload warehouse
- MLOps: Monitors feature drift and model performance

### 3. Common Anti-Patterns to Avoid

❌ **Anti-Pattern 1: MLOps Builds Own Data Pipelines**
- Result: Duplicate work, inconsistent data, tech debt
- Better: MLOps requests data from Data Eng via data contracts

❌ **Anti-Pattern 2: Data Eng Builds ML Features**
- Result: Features don't match model needs, slow iteration
- Better: Data Eng provides clean raw data, MLOps engineers features

❌ **Anti-Pattern 3: No Clear Ownership**
- Result: Features break, nobody fixes them, finger-pointing
- Better: RACI matrix defines who's Responsible, Accountable, Consulted, Informed

❌ **Anti-Pattern 4: Siloed Teams with No Communication**
- Result: MLOps doesn't know about schema changes, pipelines break
- Better: Joint Slack channels, shared on-call rotation, regular syncs

✅ **Best Practice: Define Interfaces, Not Implementation**
- Data Eng promises: "customer data table updated daily by 2 AM with schema X"
- MLOps doesn't care HOW Data Eng does it
- Clear contract enables independent work

### 4. RACI Matrix Example

| Task | Data Engineering | MLOps | Product |
|------|------------------|-------|---------|
| Raw data ingestion | **R/A** | I | I |
| Data warehouse setup | **R/A** | C | I |
| Feature engineering | C | **R/A** | C |
| Model training | I | **R/A** | C |
| Model serving API | I | **R/A** | C |
| Feature store infra | **R**/A | **R**/A | I |
| Production incident | **R** | **R** | I |
| Data contracts | **A** | **R** | C |

**Legend:**
- **R** = Responsible (does the work)
- **A** = Accountable (final decision, can't delegate)
- **C** = Consulted (input requested)
- **I** = Informed (kept in the loop)

### 5. In This Course vs. Real Companies

**In This Course:**
- YOU are both Data Engineer AND MLOps engineer
- Learn both perspectives, understand both sides
- Build appreciation for each role's challenges

**In Real Companies:**
- Separate teams with different expertise
- Data Engineering: SQL, data modeling, ETL tools
- MLOps: Python, ML frameworks, Kubernetes, monitoring
- Collaboration is essential for success

---

## Diagrams

```
┌─────────────────────────────────────────────────────────────────┐
│           Data Engineering vs MLOps Responsibilities             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🏢 Data Engineering Territory                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ • Raw Data Ingestion                                    │    │
│  │ • Data Warehouse/Lake Setup                             │    │
│  │ • Core ETL Pipelines                                    │    │
│  │ • Data Governance & Catalog                             │    │
│  └──────────────────────┬──────────────────────────────────┘   │
│                         │                                        │
│                         ↓                                        │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           🤝 SHARED ZONE                                │    │
│  │  • Feature Store (infra + definitions)                  │    │
│  │  • Data Contracts                                       │    │
│  │  • Data Quality SLAs                                    │    │
│  │  • Incident Response                                    │    │
│  └──────────────────────┬──────────────────────────────────┘   │
│                         │                                        │
│                         ↓                                        │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 🤖 MLOps Territory                                      │    │
│  │ • Feature Engineering                                   │    │
│  │ • Model Training                                        │    │
│  │ • Model Serving                                         │    │
│  │ • Model Monitoring & Drift                              │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Clear boundaries + collaboration = Successful ML systems       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-5-6-diagram.png)

> Diagram shows Data Engineering and MLOps territories with shared collaboration zone

---

## Lab / Demo

### Prerequisites

- Completed all previous lectures in Section 5
- Understanding of organizational dynamics

### Step-by-Step Instructions

```bash
# Step 1: Review responsibility matrix
cd project/docs
cat responsibility_matrix.md

# Step 2: Check data contract template
cat data_contracts/customer_data_contract.yaml

# Step 3: Review escalation procedures
cat runbooks/data_pipeline_failure.md

# Step 4: See communication guidelines
cat team_guidelines/data_eng_mlops_collaboration.md
```

### Expected Output

```yaml
# Example Data Contract
data_source: customer_master_db
owner_team: data_engineering
consumer_teams: [mlops_churn, mlops_recommender]

sla:
  update_frequency: daily
  update_time: "02:00 UTC"
  max_delay: "30 minutes"
  
schema:
  customer_id: {type: string, required: true}
  signup_date: {type: date, required: true}
  monthly_charges: {type: float, required: true}

change_policy:
  breaking_changes: "30 days notice via #data-changes"
  non_breaking_changes: "announced but no approval needed"

contacts:
  primary: data-eng-lead@company.com
  oncall: #data-eng-oncall
```

### Explanation

1. **Step 1**: See who owns what (RACI matrix)
2. **Step 2**: Understand how teams formalize data agreements
3. **Step 3**: Know what to do when things break
4. **Step 4**: Learn best practices for cross-team collaboration

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Assuming the other team knows what you need. Data Eng can't read minds. MLOps must clearly specify requirements via data contracts.

- ⚠️ **Pitfall 2**: "Not my problem" attitude. When production breaks, both teams debug together. Finger-pointing wastes time.

- ⚠️ **Pitfall 3**: No shared on-call rotation. If only Data Eng is on-call for data issues, they can't fix ML-specific feature problems. Shared responsibility = shared on-call.

---

## Homework / Practice

1. **Exercise 1**: Create a RACI matrix for 5 tasks in an ML project: data ingestion, feature engineering, model training, API deployment, monitoring. Assign R/A/C/I for Data Eng, MLOps, and Product teams.

2. **Exercise 2**: Write a data contract for the "customer usage" data our churn model needs. Include: owner, schema, SLA, change policy, and contact information.

3. **Stretch Goal**: Role-play a scenario: The customer data feed is 6 hours late. As MLOps engineer, what do you do? Who do you contact? How do you prevent it in the future?

---

## Quick Quiz

1. **Who typically owns feature engineering?**
   - A) Data Engineering
   - B) MLOps
   - C) Product Team
   - D) DevOps

2. **What is a data contract?**
   - A) Legal document with vendors
   - B) Formal agreement defining data schema, SLA, and change policy
   - C) Employment contract for data engineers
   - D) API documentation

3. **True or False: In a well-functioning organization, Data Engineering and MLOps never need to talk to each other.**

<details>
<summary>Answers</summary>

1. **B** - MLOps owns feature engineering (transforming raw data for ML)
2. **B** - Data contracts formalize what data looks like, when it's updated, and how changes are communicated
3. **False** - Constant collaboration is essential. They work on different parts of the same pipeline.

</details>

---

## Summary

- Data Engineering: raw data ingestion, data warehouse, core ETL, governance
- MLOps: feature engineering, model training, serving, ML-specific monitoring
- Shared: feature store, data contracts, data quality SLAs, incident response
- Collaboration points: project kickoff, contracts, operational incidents
- Use RACI matrices to clarify who's Responsible, Accountable, Consulted, Informed
- Avoid anti-patterns: duplicate pipelines, unclear ownership, siloed teams
- In this course you learn both roles; in companies, they're separate teams

---

## Next Steps

→ Continue to **Section 6**: Reproducible Experimentation: From Notebook to Pipeline

---

## Additional Resources

- [RACI Matrix Guide](https://www.projectmanager.com/blog/raci-chart-definition-tips-and-example)
- [Data Contracts: The Key to Scaling Autonomy](https://locallyoptimistic.com/post/data-contracts/)
- [DataOps vs MLOps: Understanding the Difference](https://www.montecarlodata.com/blog-dataops-vs-mlops/)
