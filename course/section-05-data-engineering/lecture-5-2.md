# Lecture 5.2 – Data Ingestion Patterns (Batch, Streaming, APIs)

## In This Lecture You Will Learn

- [x] Understand batch vs. streaming vs. real-time data ingestion patterns
- [x] Choose the right ingestion pattern for ML use cases
- [x] Implement data pipelines using common orchestration tools

---

## Real-World Context

> **Story**: Jason built a churn model that trained on last month's data. It took 2 days to notice when a data source stopped sending updates. By then, predictions were stale and business decisions were wrong. He learned: data ingestion isn't just about moving bytes—it's about reliability, monitoring, and choosing the right pattern (batch vs. streaming) for your SLA. Batch is simple but can be hours old. Streaming is real-time but complex. APIs are flexible but can be rate-limited. Each pattern has trade-offs that directly impact your ML system.

In the real world, the data ingestion pattern you choose determines your system's freshness, complexity, and reliability. Choose wrong, and you'll either over-engineer or under-deliver.

---

## Main Content

### 1. Three Ingestion Patterns

**Batch Ingestion**
- **What**: Load data in scheduled chunks (hourly, daily, weekly)
- **Examples**: Nightly ETL jobs, weekly model retraining
- **Tools**: Apache Airflow, cron jobs, AWS Glue, dbt
- **Best for**: Historical analysis, training pipelines, reports
- **Pros**: Simple, reliable, easy to debug, can replay/reprocess
- **Cons**: Data can be hours/days old, not suitable for real-time needs

**Streaming Ingestion**
- **What**: Continuous real-time data flow
- **Examples**: Clickstream, IoT sensors, transaction logs
- **Tools**: Apache Kafka, AWS Kinesis, Google Pub/Sub, Apache Flink
- **Best for**: Real-time features, fraud detection, live dashboards
- **Pros**: Low latency (seconds), always fresh, event-driven
- **Cons**: Complex infrastructure, harder to debug, more expensive

**API-Based Ingestion**
- **What**: Pull data on-demand via REST/GraphQL APIs
- **Examples**: Third-party services, SaaS platforms, webhooks
- **Tools**: Python requests, Apache Airflow HTTP operators, Zapier
- **Best for**: Small volumes, external data, triggered updates
- **Pros**: Flexible, no infrastructure needed, pay-per-use
- **Cons**: Rate limits, API availability risks, authentication complexity

### 2. Decision Framework: Which Pattern?

| Criteria | Batch | Streaming | API |
|----------|-------|-----------|-----|
| **Latency Required** | Hours/days OK | Seconds/minutes | Minutes/hours |
| **Data Volume** | GB-TB per run | MB-GB per second | KB-MB per call |
| **Complexity** | Low | High | Medium |
| **Cost** | Low | High | Variable |
| **Infrastructure** | Scheduler only | Message queue + processors | None (external) |
| **Use Case Example** | Model training | Fraud detection | Weather API |

**For Our Churn Model**: 
Batch (daily) is sufficient. Churn doesn't change hourly—daily updates are fine and much simpler than streaming.

### 3. Implementing Batch Pipelines with Airflow

```python
# Example: Daily churn data pipeline
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def extract_customer_data():
    # Pull from CRM database
    pass

def transform_features():
    # Calculate churn features
    pass

def load_to_feature_store():
    # Write to S3/Parquet
    pass

dag = DAG(
    'churn_data_pipeline',
    schedule_interval='@daily',  # Run every day at midnight
    start_date=datetime(2024, 1, 1),
    catchup=False
)

extract = PythonOperator(task_id='extract', python_callable=extract_customer_data, dag=dag)
transform = PythonOperator(task_id='transform', python_callable=transform_features, dag=dag)
load = PythonOperator(task_id='load', python_callable=load_to_feature_store, dag=dag)

extract >> transform >> load
```

**Key Concepts**:
- **DAG** (Directed Acyclic Graph): Defines task dependencies
- **Schedule**: When to run (cron syntax or presets like @daily)
- **Idempotency**: Same input always produces same output
- **Retries**: Automatic retry on failure

---

## Diagrams

```
┌─────────────────────────────────────────────────────────────────┐
│              Data Ingestion Patterns Comparison                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📦 BATCH INGESTION                                             │
│  ┌──────────┐   Schedule   ┌──────────┐   Daily    ┌─────────┐│
│  │ Source   │─────@daily───│ Pipeline │───Chunk────│  Data   ││
│  │ System   │              │ (Airflow)│            │  Lake   ││
│  └──────────┘              └──────────┘            └─────────┘│
│  Latency: Hours            Complexity: Low         Cost: $     │
│                                                                  │
│  🌊 STREAMING INGESTION                                         │
│  ┌──────────┐  Real-time   ┌──────────┐  Continuous ┌────────┐│
│  │ Source   │───Events─────│  Kafka/  │────Stream───│ Data   ││
│  │ System   │              │  Kinesis │             │ Lake   ││
│  └──────────┘              └──────────┘             └────────┘│
│  Latency: Seconds          Complexity: High        Cost: $$$  │
│                                                                  │
│  🔌 API INGESTION                                               │
│  ┌──────────┐  On-demand   ┌──────────┐   REST     ┌────────┐│
│  │ External │───Request────│  Script  │───API──────│ Data   ││
│  │ Service  │              │ (Python) │            │ Lake   ││
│  └──────────┘              └──────────┘            └────────┘│
│  Latency: Minutes          Complexity: Medium      Cost: $$   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-5-2-diagram.png)

> Diagram illustrates the three ingestion patterns with their latency, complexity, and cost trade-offs

---

## Lab / Demo

### Prerequisites

- Completed Lecture 5.1
- Docker installed (for Airflow demo)
- Python 3.8+

### Step-by-Step Instructions

```bash
# Step 1: Review sample Airflow DAG
cd project/pipelines
cat dags/churn_data_pipeline.py

# Step 2: Set up a local Airflow environment (Docker)
docker-compose -f airflow-docker-compose.yml up -d

# Step 3: Access Airflow UI
# Open browser: http://localhost:8080
# Username: airflow, Password: airflow

# Step 4: Trigger the churn data pipeline manually
# In Airflow UI: Toggle DAG on, click "Trigger DAG"

# Step 5: View logs and task execution
# Click on task → View Logs
```

### Expected Output

```
Airflow DAG: churn_data_pipeline
Status: Running
---
[2024-01-15 10:00:00] Task extract: SUCCESS (Duration: 45s)
[2024-01-15 10:00:45] Task transform: SUCCESS (Duration: 120s)
[2024-01-15 10:02:45] Task load: SUCCESS (Duration: 30s)
---
Pipeline completed successfully.
Output: s3://ml-data/churn/features/2024-01-15/features.parquet
```

### Explanation

1. **Step 1**: Understand DAG structure and task dependencies
2. **Step 2**: Run Airflow locally in Docker (production-like environment)
3. **Step 3**: Use the web UI to monitor and manage pipelines
4. **Step 4**: Manually trigger to test (production would be scheduled)
5. **Step 5**: Debug by reading task logs

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Choosing streaming when batch is sufficient. Streaming is 10x more complex. Only use it when you need sub-minute latency. Most ML systems don't.

- ⚠️ **Pitfall 2**: Not making pipelines idempotent. If you run the same pipeline twice with the same input, you should get the same output. Use date partitions, not "append mode."

- ⚠️ **Pitfall 3**: Ignoring backfill requirements. What happens when a pipeline fails? Can you re-run just that day? Design for failure from day one.

---

## Homework / Practice

1. **Exercise 1**: Draw a timeline showing when data is available with batch (daily@2AM), streaming (real-time), and API (on-demand) ingestion. If a customer churns at 3PM, when does each pattern detect it?

2. **Exercise 2**: List 3 ML use cases from your experience/imagination. For each, choose batch, streaming, or API ingestion and justify why.

3. **Stretch Goal**: Install Airflow locally and create a simple DAG that downloads a CSV file, converts it to Parquet, and uploads to a local folder. Run it on schedule.

---

## Quick Quiz

1. **Which ingestion pattern is best for training ML models on historical data?**
   - A) Streaming - always use the latest technology
   - B) API - most flexible
   - C) Batch - simple, reliable, sufficient for historical analysis
   - D) All are equally good

2. **What is the main advantage of streaming ingestion over batch?**
   - A) Simpler to implement
   - B) Lower cost
   - C) Lower latency (seconds vs hours)
   - D) Easier to debug

3. **True or False: If your ML model only needs to retrain weekly, you should still use streaming ingestion for future-proofing.**

<details>
<summary>Answers</summary>

1. **C** - Batch is ideal for training: simple, can process large volumes, and latency doesn't matter for historical data
2. **C** - Streaming provides real-time data (seconds) vs batch (hours/days)
3. **False** - Don't over-engineer. Use batch for weekly retraining. You can always migrate to streaming later if requirements change.

</details>

---

## Summary

- Three patterns: Batch (scheduled chunks), Streaming (real-time), API (on-demand)
- Batch is simplest and sufficient for most ML use cases (including our churn model)
- Streaming adds complexity but needed for real-time requirements (<1 minute latency)
- Use decision framework: consider latency, volume, complexity, cost
- Airflow is industry standard for batch orchestration (DAGs, schedules, retries)
- Always design pipelines to be idempotent and backfill-friendly

---

## Next Steps

→ Continue to **Lecture 5.3**: Data Quality & Validation (Basic Checks MLOps Must Enforce)

---

## Additional Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [AWS: Batch vs Streaming Data](https://aws.amazon.com/what-is/batch-processing/)
- [Kafka vs Batch Processing (Confluent)](https://www.confluent.io/blog/kafka-vs-batch-processing/)
