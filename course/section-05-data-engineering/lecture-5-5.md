# Lecture 5.5 – Storing Data & Features for Re-use (Intro to Feature Stores)

## In This Lecture You Will Learn

- [x] Understand the purpose and benefits of feature stores
- [x] Identify when you need a feature store vs. simpler alternatives
- [x] Integrate feature stores into ML training and serving pipelines

---

## Real-World Context

> **Story**: Five teams at MegaCorp each calculated "customer lifetime value" differently. Each maintained their own ETL pipelines, their own S3 buckets, their own documentation (or lack thereof). When asked to compare models, they couldn't—apples to oranges. Enter the feature store: one source of truth, one calculation, versioned, monitored, and reusable. Initial investment: 2 weeks. Time saved per team per month: 1 week. ROI in 3 months. The lesson: feature stores aren't for tiny teams—they're for when feature proliferation becomes chaos.

In the real world, feature stores solve organizational problems (reuse, consistency, governance), not just technical ones.

---

## Main Content

### 1. What Is a Feature Store?

A **centralized repository** for storing, managing, and serving ML features.

Think of it as "GitHub for ML features"—versioned, documented, shareable.

**Three Main Components**:
1. **Feature Definitions**: How to calculate each feature (code/config)
2. **Feature Values**: Pre-computed feature values for training and serving
3. **Feature Metadata**: Owner, version, statistics, data lineage, documentation

### 2. Problems Feature Stores Solve

**Problem 1: Duplication**
- 5 teams independently calculate "customer engagement"
- 5 different implementations, 5x the work
- Solution: Calculate once, store centrally, reuse everywhere

**Problem 2: Training/Serving Skew**
- Training uses pandas in Python
- Serving uses different code in Java
- Subtle differences break models
- Solution: Feature store provides same features to both

**Problem 3: Feature Discovery**
- Data scientist asks: "Has anyone built a payment failure rate feature?"
- Without catalog: Email 50 people, wait 3 days, get vague answers
- With feature store: Search catalog, find feature in 30 seconds

**Problem 4: Governance**
- Which features contain PII?
- Who owns the "credit_score" feature?
- Can I use this feature for this model?
- Solution: Metadata and access control in feature store

**Problem 5: Performance**
- Expensive aggregation: "total_purchases_last_90_days"
- Re-calculating on every prediction is slow
- Solution: Pre-compute once, cache in feature store, fast lookups

### 3. Feature Store Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    FEATURE STORE                            │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────┐      ┌──────────────────────┐  │
│  │  OFFLINE STORE       │      │  ONLINE STORE        │  │
│  │  (Training)          │      │  (Serving)           │  │
│  ├──────────────────────┤      ├──────────────────────┤  │
│  │ • Batch features     │      │ • Real-time lookup   │  │
│  │ • Historical data    │      │ • Low latency <10ms  │  │
│  │ • Large volumes      │      │ • Key-value store    │  │
│  │ • Parquet/Data Lake  │      │ • Redis/DynamoDB     │  │
│  │                      │      │                      │  │
│  │ Use: Model Training  │      │ Use: Predictions     │  │
│  └──────────────────────┘      └──────────────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐│
│  │           FEATURE REGISTRY (Metadata)                  ││
│  │  - Feature definitions & schemas                       ││
│  │  - Owners & documentation                              ││
│  │  - Versions & lineage                                  ││
│  │  - Statistics & monitoring                             ││
│  └───────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────┘
```

**Offline Store**: For training
- Store: S3, BigQuery, Snowflake (columnar, analytical)
- Access: Batch queries, large scans
- Latency: Seconds to minutes (doesn't matter for training)

**Online Store**: For serving
- Store: Redis, DynamoDB, PostgreSQL (row-based, transactional)
- Access: Single row lookup by key
- Latency: Milliseconds (critical for predictions)

### 4. When Do You Need a Feature Store?

**YES, use a feature store if**:
- ✅ Multiple ML teams sharing features
- ✅ Need both training (batch) and serving (real-time) access
- ✅ Feature reuse is common
- ✅ Governance/compliance requirements
- ✅ >10 ML models in production

**NO, simpler alternatives if**:
- ❌ Single team, single model (early stage)
- ❌ All batch processing, no real-time serving
- ❌ MVP phase, requirements changing weekly
- ❌ <5 people working on ML

**Simple Alternatives**:
- S3 + Parquet files (offline only)
- PostgreSQL tables (small scale)
- Feature engineering library (code reuse without infrastructure)

### 5. Popular Feature Store Tools

| Tool | Type | Best For |
|------|------|----------|
| **Feast** | Open Source | On-prem, Kubernetes, flexible |
| **Tecton** | Commercial | Enterprise, fully managed |
| **AWS SageMaker Feature Store** | Cloud | AWS-native workloads |
| **Databricks Feature Store** | Cloud | Databricks users |
| **Vertex AI Feature Store** | Cloud | GCP-native workloads |

**Our Churn Project**: 
We'll use a simple "feature store" pattern (S3 + Parquet) for learning. In real companies, you'd likely use a proper feature store if you have multiple ML systems.

---

## Diagrams

```
┌────────────────────────────────────────────────────────────┐
│         Feature Store in ML Workflow                       │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 Raw Data Sources                                       │
│         ↓                                                   │
│  🔄 Feature Engineering Pipeline                           │
│         ↓                                                   │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              FEATURE STORE                            │ │
│  │  ┌──────────────┐          ┌──────────────┐         │ │
│  │  │ Offline      │          │ Online       │         │ │
│  │  │ (Parquet/S3) │          │ (Redis/DB)   │         │ │
│  │  └──────┬───────┘          └──────┬───────┘         │ │
│  └─────────┼──────────────────────────┼─────────────────┘ │
│            │                          │                    │
│            ↓                          ↓                    │
│   🤖 Model Training          🚀 Real-time Serving         │
│      (Batch)                     (Low Latency)            │
│                                                             │
│  Benefits:                                                 │
│  • Single source of truth                                 │
│  • Consistent features across training & serving          │
│  • Reusable across models                                 │
│  • Governed & documented                                  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-5-5-diagram.png)

> Diagram shows feature store as central hub serving both training and serving workloads

---

## Lab / Demo

### Prerequisites

- Completed Lectures 5.1-5.4
- Understanding of offline vs online systems

### Step-by-Step Instructions

```bash
# Step 1: Review feature store configuration
cd project/feature_store
cat feast_config.yaml

# Step 2: Explore feature definitions
cat features/churn_features.py

# Step 3: (Simulated) Write features to offline store
python scripts/materialize_features.py --start-date 2024-01-01 --end-date 2024-01-31

# Step 4: (Simulated) Read features for training
python scripts/get_training_features.py --entity-ids customer_ids.csv

# Step 5: (Simulated) Sync to online store for serving
python scripts/materialize_online.py
```

### Expected Output

```
Feature Materialization Complete
================================
Features written to offline store (S3):
- s3://feature-store/churn/offline/2024-01/features.parquet
- Rows: 2,000,000
- Features: 25
- Date range: 2024-01-01 to 2024-01-31

Training Features Retrieved:
- Customer IDs: 10,000
- Feature columns: 25
- Missing values: 0.02% (acceptable)

Online Store Synchronized:
- Redis keys created: 2,000,000
- Average lookup latency: 2.3ms
- Cache hit rate: 99.8%
```

### Explanation

1. **Step 1**: Review Feast configuration (feature store framework)
2. **Step 2**: See how features are defined declaratively
3. **Step 3**: Materialize (pre-compute) features for historical data
4. **Step 4**: Retrieve features for model training (point-in-time correct)
5. **Step 5**: Sync latest features to online store for fast serving

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Implementing a feature store too early. If you're still prototyping with 1 model and 1 person, S3 + Parquet is fine. Don't over-engineer.

- ⚠️ **Pitfall 2**: Not considering point-in-time correctness. When training a model for "predict churn on 2024-01-15", you can only use features available ON 2024-01-15, not future data.

- ⚠️ **Pitfall 3**: Ignoring the cost of online store. Redis/DynamoDB for 10M features updated hourly gets expensive. Consider: Do you really need real-time? Can you cache?

---

## Homework / Practice

1. **Exercise 1**: List 3 scenarios where a feature store is essential and 3 where it's overkill. Justify each.

2. **Exercise 2**: Design a simple feature store using only S3 and Python. How would you organize folders? How would you version features? How would you handle training vs serving?

3. **Stretch Goal**: Research Feast (open-source feature store). Install it locally and define a simple feature (e.g., "days_since_signup"). Materialize it to local storage.

---

## Quick Quiz

1. **What is the main purpose of a feature store?**
   - A) Store raw data
   - B) Train models
   - C) Centralize, version, and serve ML features for reuse
   - D) Monitor model performance

2. **What's the difference between offline and online feature stores?**
   - A) Offline is old data, online is new data
   - B) Offline for training (batch), online for serving (real-time)
   - C) They're the same thing
   - D) Offline is free, online costs money

3. **True or False: Every ML project should use a feature store from day one.**

<details>
<summary>Answers</summary>

1. **C** - Feature stores centralize feature definitions and values for reuse across models
2. **B** - Offline supports batch training queries; online supports low-latency serving lookups
3. **False** - Feature stores add complexity. Start simple (S3 + Parquet), add feature store when you have multiple teams/models.

</details>

---

## Summary

- Feature stores centralize feature definitions, values, and metadata
- Solve: duplication, training/serving skew, discovery, governance, performance
- Two modes: Offline (batch, training) and Online (real-time, serving)
- Use when: multiple teams, feature reuse, real-time serving needs
- Alternatives for simple cases: S3 + Parquet, database tables
- Popular tools: Feast (open source), Tecton, AWS/GCP/Databricks feature stores
- Don't over-engineer early—add feature store when complexity justifies it

---

## Next Steps

→ Continue to **Lecture 5.6**: Where Data Engineer Ends and MLOps Starts (Responsibility Boundaries)

---

## Additional Resources

- [Feast Documentation](https://docs.feast.dev/)
- [Tecton: What is a Feature Store?](https://www.tecton.ai/blog/what-is-a-feature-store/)
- [AWS SageMaker Feature Store](https://aws.amazon.com/sagemaker/feature-store/)
