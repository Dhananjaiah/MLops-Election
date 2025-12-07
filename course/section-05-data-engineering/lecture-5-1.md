# Lecture 5.1 – Data Types & Storage (DB, Data Lake, CSV, Parquet)

## In This Lecture You Will Learn

- [x] Understand different data storage formats and when to use each
- [x] Compare databases vs. data lakes vs. data warehouses
- [x] Choose the right storage format for ML workloads (CSV, Parquet, etc.)

---

## Real-World Context

> **Story**: Emma's ML training job took 4 hours to load data from CSV files. Her colleague showed her Parquet format—same data, 15-minute load time, 10x smaller files. But then she tried to debug a Parquet file with `cat` and got gibberish. Each format has trade-offs. CSV is human-readable but slow and large. Parquet is fast and compact but binary. Databases are queryable but expensive to scan. Data lakes are cheap but lack structure. The right choice depends on your use case, and as an MLOps engineer, you need to know all of them.

In the real world, choosing the wrong storage format can make your ML system 10x slower or 10x more expensive. Data engineering fundamentals aren't optional for MLOps.

---

## Main Content

### 1. Storage System Types

**Databases (OLTP - Online Transaction Processing)**
- **Purpose**: Handle live transactions (create, read, update, delete)
- **Examples**: PostgreSQL, MySQL, MongoDB
- **Best for**: Operational data, real-time lookups, transactional consistency
- **ML Use Case**: Storing model metadata, experiment results, predictions
- **Pros**: Fast queries, ACID guarantees, structured
- **Cons**: Expensive for large scans, not optimized for analytics

**Data Warehouses (OLAP - Online Analytical Processing)**
- **Purpose**: Optimized for analytical queries on large datasets
- **Examples**: Snowflake, BigQuery, Redshift
- **Best for**: Historical analysis, aggregations, complex joins
- **ML Use Case**: Feature engineering, training data preparation
- **Pros**: Fast analytics, columnar storage, SQL interface
- **Cons**: Higher cost, not real-time, overkill for simple reads

**Data Lakes**
- **Purpose**: Store massive amounts of raw data cheaply
- **Examples**: AWS S3, Google Cloud Storage, Azure Data Lake
- **Best for**: Long-term storage, mixed data types, archive
- **ML Use Case**: Storing training datasets, model artifacts, logs
- **Pros**: Cheap, scalable, flexible schema
- **Cons**: No built-in querying, can become "data swamp" without governance

### 2. File Formats for ML

| Format | Type | Human Readable? | Size | Speed | Best For |
|--------|------|-----------------|------|-------|----------|
| **CSV** | Text | ✅ Yes | Large | Slow | Small datasets, debugging, sharing |
| **JSON** | Text | ✅ Yes | Large | Slow | Nested data, APIs, config files |
| **Parquet** | Binary | ❌ No | Small | Fast | ML training, analytics, big data |
| **Avro** | Binary | ❌ No | Small | Fast | Streaming data, schema evolution |
| **Feather/Arrow** | Binary | ❌ No | Small | Very Fast | Python↔R data exchange, in-memory |
| **HDF5** | Binary | ❌ No | Small | Fast | Scientific computing, arrays, tensors |

**Parquet Deep Dive** (Most common for ML):
- Columnar storage (read only columns you need)
- Built-in compression (snappy, gzip, etc.)
- Schema embedded in file
- Efficient for filtering and aggregations
- Standard in Spark, Pandas, Dask

**Example**:
```python
# Same data, different formats
df.to_csv('data.csv')        # 500 MB, 60s to read
df.to_parquet('data.parquet') # 50 MB, 5s to read
```

### 3. Choosing the Right Storage for ML

**For Training Data**:
- Store in Data Lake (S3/GCS) as Parquet
- Cheap, fast to read, versioned, scales to TB/PB
- Example: `s3://ml-data/churn/train/year=2024/month=01/data.parquet`

**For Model Artifacts**:
- Store in Data Lake (S3/GCS) or Model Registry
- Models (pickle, ONNX), metadata, evaluation results
- Example: `s3://ml-models/churn/v1.2.3/model.pkl`

**For Feature Metadata**:
- Store in Database (PostgreSQL)
- Feature names, types, statistics, lineage
- Fast lookups for serving time

**For Real-time Predictions**:
- Database (Redis, PostgreSQL) or Feature Store
- Pre-computed features for low-latency serving
- Sub-millisecond lookups

---

## Diagrams

```
┌────────────────────────────────────────────────────────────────┐
│              Data Storage Landscape for ML                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🗄️  Databases (OLTP)                                          │
│  PostgreSQL, MySQL                                             │
│  → Live transactions, model metadata                            │
│  → Use when: Need ACID, fast lookups                           │
│                                                                 │
│  🏢 Data Warehouses (OLAP)                                     │
│  Snowflake, BigQuery, Redshift                                 │
│  → Analytics, feature engineering                              │
│  → Use when: Complex SQL queries on TBs of data                │
│                                                                 │
│  🌊 Data Lakes                                                 │
│  S3, GCS, Azure Data Lake                                      │
│  → Raw data, training sets, model artifacts                    │
│  → Use when: Cheap storage, flexible schema                    │
│                                                                 │
│  📁 File Formats                                               │
│  ├─ CSV/JSON (text, slow, large)                              │
│  └─ Parquet/Avro (binary, fast, small)  ← Best for ML        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-5-1-diagram.png)

> Diagram illustrates data flowing from operational databases through data lakes (Parquet) to ML training

---

## Lab / Demo

### Prerequisites

- Python with pandas installed
- Basic understanding of file I/O

### Step-by-Step Instructions

```bash
# Step 1: Compare file formats
cd project/data
python scripts/compare_formats.py

# Step 2: Convert CSV to Parquet
python scripts/convert_to_parquet.py --input raw/customers.csv --output processed/customers.parquet

# Step 3: Benchmark read performance
python scripts/benchmark_read.py

# Step 4: Inspect Parquet schema
pip install pyarrow
python scripts/inspect_parquet.py processed/customers.parquet
```

### Expected Output

```
Format Comparison Results:
==========================
CSV:
  - Size: 523 MB
  - Read time: 45.2s
  - Compression: None

Parquet (snappy):
  - Size: 87 MB (6x smaller)
  - Read time: 6.1s (7x faster)
  - Compression: Built-in

Parquet Schema:
customer_id: int64
signup_date: datetime64
monthly_charges: float64
churned: bool
```

### Explanation

1. **Step 1**: See size and speed differences between formats
2. **Step 2**: Learn how to convert between formats
3. **Step 3**: Measure actual read performance on your machine
4. **Step 4**: Understand Parquet's self-describing schema

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Using CSV for large ML datasets. It's 5-10x slower than Parquet and wastes storage. Only use CSV for small data or human inspection.

- ⚠️ **Pitfall 2**: Treating a data lake like a database. You can't `SELECT * FROM s3://bucket/` —you need query engines (Athena, Presto, Spark) on top.

- ⚠️ **Pitfall 3**: Not partitioning large datasets. Always partition by date/category: `data/year=2024/month=01/` for faster reads.

---

## Homework / Practice

1. **Exercise 1**: Take a CSV file and convert it to Parquet. Measure the file size difference and read time difference.

2. **Exercise 2**: Research when you'd use Avro instead of Parquet. Hint: streaming data and schema evolution.

3. **Stretch Goal**: Set up a simple data lake structure on your local filesystem. Create folders for raw/, processed/, and features/, with partitions by date.

---

## Quick Quiz

1. **Which format is best for ML training datasets?**
   - A) CSV - human readable
   - B) JSON - flexible schema
   - C) Parquet - columnar, compressed, fast
   - D) XML - structured data

2. **What's the main difference between a data lake and a data warehouse?**
   - A) Data lakes are smaller
   - B) Data lakes store raw/unstructured data cheaply; warehouses are optimized for SQL analytics
   - C) They're the same thing
   - D) Data lakes are only for images

3. **True or False: You should store all your ML data in a transactional database for fast access.**

<details>
<summary>Answers</summary>

1. **C** - Parquet is the industry standard for ML: fast, compact, columnar
2. **B** - Lakes are cheap raw storage; warehouses are structured for analytics
3. **False** - Databases are expensive for large ML datasets. Use data lakes (S3/GCS) with Parquet.

</details>

---

## Summary

- Databases (OLTP) for transactions, warehouses (OLAP) for analytics, lakes for cheap storage
- File formats: CSV for debugging, Parquet for ML production (10x faster, smaller)
- Store training data in data lakes as Parquet, partitioned by date
- Store model artifacts and metadata in object storage (S3/GCS)
- Choose storage based on: query patterns, cost, scale, and latency requirements

---

## Next Steps

→ Continue to **Lecture 5.2**: Data Ingestion Patterns (Batch, Streaming, APIs)

---

## Additional Resources

- [Parquet Documentation](https://parquet.apache.org/docs/)
- [AWS: Data Lake vs Data Warehouse](https://aws.amazon.com/big-data/datalakes-and-analytics/what-is-a-data-lake/)
- [Databricks: Parquet Best Practices](https://www.databricks.com/glossary/what-is-parquet)
