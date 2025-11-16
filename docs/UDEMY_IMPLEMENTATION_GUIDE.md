# 🎓 Udemy MLOps Course - Election Prediction System Implementation Guide

## 📚 Course Overview

Welcome to the **Complete MLOps Course: Production Machine Learning Systems**! This guide will walk you through implementing a real-world, production-ready Election Prediction System using industry-standard MLOps practices.

### What You'll Build

By the end of this course, you'll have built a complete machine learning system that:
- ✅ Predicts election outcomes using demographic, historical, and survey data
- ✅ Implements the full ML lifecycle (data → training → serving → monitoring)
- ✅ Uses modern MLOps tools (MLflow, DVC, Airflow, Kubernetes, Prometheus)
- ✅ Follows production best practices (security, monitoring, CI/CD)
- ✅ Can be deployed to production environments

### Learning Objectives

After completing this course, you will be able to:
1. Design and implement end-to-end ML pipelines
2. Version control your data and models
3. Track experiments and manage model lifecycle
4. Deploy ML models as scalable APIs
5. Monitor model performance and detect drift
6. Implement automated retraining pipelines
7. Apply security best practices
8. Deploy to Kubernetes with auto-scaling

### Course Structure

This course consists of **14 comprehensive modules** covering the entire MLOps lifecycle:

```
Module 1-2:  Fundamentals & Setup
Module 3-5:  Data Pipeline & Versioning
Module 6-8:  Model Training & Tracking
Module 9-10: Model Serving & APIs
Module 11:   Monitoring & Drift Detection
Module 12:   Orchestration with Airflow
Module 13:   Kubernetes & Deployment
Module 14:   CI/CD & Production Best Practices
```

---

## 🎯 Prerequisites

### Required Knowledge
- **Python**: Intermediate level (functions, classes, decorators)
- **Machine Learning**: Basic understanding (supervised learning, classification)
- **Git**: Basic commands (clone, commit, push)
- **Command Line**: Basic terminal usage

### Nice to Have
- Docker basics
- REST APIs
- Cloud platforms (AWS/GCP/Azure)
- Linux/Unix systems

### System Requirements
- **OS**: Linux, macOS, or Windows with WSL2
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 10GB free space
- **Python**: 3.9 or higher
- **Docker**: Latest version
- **Kubernetes**: Minikube or Docker Desktop with K8s

---

## 📦 Initial Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/MLops-Election.git
cd MLops-Election

# Verify you're in the right directory
ls -la
```

You should see directories: `src/`, `data/`, `models/`, `notebooks/`, etc.

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
make install
# Or manually:
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
# Run a quick test
python -c "import sklearn, pandas, numpy, mlflow; print('All packages installed successfully!')"

# Check Make commands
make help
```

---

## 📖 Module-by-Module Implementation Guide

## Module 1-2: Fundamentals & Project Setup

### Learning Objectives
- Understand MLOps lifecycle
- Set up development environment
- Understand project architecture

### Theory
MLOps combines Machine Learning, DevOps, and Data Engineering to:
1. **Automate** ML workflows
2. **Monitor** model performance
3. **Version** data and models
4. **Deploy** models reliably

### Hands-On Exercise

**Exercise 1.1: Explore the Project Structure**

```bash
# Examine the directory structure
tree -L 2 .

# Key directories:
# src/ - Source code
# data/ - Datasets
# models/ - Trained models
# notebooks/ - Jupyter notebooks
# docker/ - Docker configurations
# kubernetes/ - K8s manifests
```

**Exercise 1.2: Understand the Makefile**

```bash
# View available commands
make help

# Each command automates a part of the MLOps lifecycle
# Example: make data, make train, make serve
```

**Exercise 1.3: Review the README**

Open `README.md` and familiarize yourself with:
- Project overview
- Architecture diagram
- Tech stack
- Features

### 🎯 Module Checkpoint
- [ ] Environment set up successfully
- [ ] All dependencies installed
- [ ] Understand project structure
- [ ] Can run `make help`

---

## Module 3-5: Data Pipeline & Versioning

### Learning Objectives
- Generate and process election data
- Implement feature engineering
- Version data with DVC
- Validate data quality

### Theory

**Why Data Versioning Matters:**
- Track data changes over time
- Reproduce experiments
- Share datasets with team
- Rollback to previous versions

**DVC (Data Version Control):**
- Git for data and models
- Lightweight metadata in Git
- Actual data in remote storage

### Hands-On Implementation

**Exercise 3.1: Generate Synthetic Data**

```bash
# Generate election dataset
python src/data/make_dataset.py

# Check generated data
ls -lh data/raw/
head data/raw/election_data.csv
```

**What's happening?**
The script generates synthetic data with:
- **Demographics**: population, age, income, education
- **Voting history**: turnout, margins, registration
- **Surveys**: polls, sentiment scores
- **Target**: which candidate wins

**Exercise 3.2: Preprocess Data**

```bash
# Run preprocessing
python src/data/preprocess.py

# Check processed data
ls -lh data/processed/
```

**Preprocessing steps:**
1. Handle missing values
2. Detect and handle outliers
3. Normalize numerical features
4. Validate data quality

**Exercise 3.3: Feature Engineering**

```bash
# Generate features
python src/data/features.py

# Check engineered features
ls -lh data/features/
python -c "import pandas as pd; df = pd.read_csv('data/features/train_features.csv'); print(df.columns.tolist())"
```

**New features created:**
- `turnout_margin_interaction`
- `demographic_score`
- `poll_spread`
- `sentiment_favorability_ratio`
- And 15+ more!

**Exercise 3.4: Data Versioning with DVC**

```bash
# Initialize DVC (if not already done)
dvc init

# Add data to DVC tracking
dvc add data/raw/election_data.csv
dvc add data/processed/
dvc add data/features/

# Commit DVC metadata
git add data/.gitignore data/raw/.dvc data/processed/.dvc data/features/.dvc
git commit -m "Add data versioning with DVC"

# Configure remote storage (example with S3)
dvc remote add -d storage s3://my-mlops-bucket/election-data

# Push data to remote
dvc push
```

**Exercise 3.5: Complete Data Pipeline**

```bash
# Run entire data pipeline
make data

# This runs:
# 1. make_dataset.py
# 2. preprocess.py
# 3. features.py
```

### 🎯 Module Checkpoint
- [ ] Understand data generation process
- [ ] Can run data preprocessing
- [ ] Feature engineering completed
- [ ] DVC initialized and configured
- [ ] Data versioned with DVC

### 💡 Common Pitfalls
- **Issue**: DVC push fails
  - **Solution**: Check remote storage configuration and credentials
- **Issue**: Missing data files
  - **Solution**: Run `dvc pull` to fetch data from remote
- **Issue**: Feature engineering crashes
  - **Solution**: Ensure preprocessing completed successfully first

---

## Module 6-8: Model Training & Experiment Tracking

### Learning Objectives
- Train multiple ML models
- Track experiments with MLflow
- Compare model performance
- Select and register best model

### Theory

**MLflow Components:**
1. **Tracking**: Log parameters, metrics, artifacts
2. **Projects**: Package code in reusable format
3. **Models**: Standardize model format
4. **Registry**: Manage model lifecycle

**Model Training Strategy:**
- Train multiple algorithms (Random Forest, XGBoost, Logistic Regression)
- Hyperparameter tuning with GridSearchCV
- Cross-validation for robust evaluation
- Select best model based on metrics

### Hands-On Implementation

**Exercise 6.1: Start MLflow Tracking Server**

```bash
# Terminal 1: Start MLflow UI
make mlflow-ui
# Or manually:
mlflow ui --host 0.0.0.0 --port 5000

# Open browser: http://localhost:5000
```

**Exercise 6.2: Train Models**

```bash
# Train all models with MLflow tracking
make train
# Or manually:
python src/train/train.py
```

**What's happening?**
The training script:
1. Loads processed data
2. Splits into train/validation/test sets
3. Trains 3 different models
4. Logs everything to MLflow:
   - Parameters (hyperparameters)
   - Metrics (accuracy, precision, recall, F1, AUC)
   - Artifacts (model files, plots)

**Exercise 6.3: Explore MLflow UI**

Open http://localhost:5000 and:
1. Click on "election_prediction" experiment
2. View all training runs
3. Compare metrics across runs
4. Examine logged artifacts (confusion matrices, ROC curves)
5. Review parameters for each run

**Exercise 6.4: Hyperparameter Tuning**

Examine `src/train/train.py` to see GridSearchCV setup:

```python
# Random Forest hyperparameters
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}
```

**Exercise 6.5: Model Evaluation**

```bash
# Evaluate all trained models
make evaluate
# Or manually:
python src/train/evaluate.py

# Compare models
python src/train/compare_models.py

# Check evaluation reports
cat reports/model_comparison.txt
```

**Exercise 6.6: Register Best Model**

```bash
# Best model is automatically registered in MLflow
# View in MLflow UI > Models section

# Or register manually via Python
python -c "
import mlflow
mlflow.set_tracking_uri('http://localhost:5000')
# Get best run ID from UI
run_id = 'YOUR_RUN_ID'
model_uri = f'runs:/{run_id}/model'
mlflow.register_model(model_uri, 'election_prediction_model')
"
```

**Exercise 6.7: Complete Training Pipeline**

```bash
# Run complete pipeline: data + train + evaluate
make pipeline
```

### 🎯 Module Checkpoint
- [ ] MLflow UI accessible
- [ ] Multiple models trained successfully
- [ ] Experiments visible in MLflow
- [ ] Understand metrics comparison
- [ ] Best model registered in MLflow
- [ ] Model artifacts saved

### 💡 Best Practices
- **Log Everything**: Parameters, metrics, artifacts, environment
- **Meaningful Names**: Use descriptive experiment and run names
- **Version Control**: Commit code before each experiment
- **Document**: Add notes/tags to runs in MLflow
- **Compare Fairly**: Use same data splits and random seeds

---

## Module 9-10: Model Serving & API Development

### Learning Objectives
- Create REST API with FastAPI
- Implement prediction endpoints
- Add health checks and monitoring
- Export Prometheus metrics
- Containerize with Docker

### Theory

**Why FastAPI?**
- Fast performance (async support)
- Automatic API documentation
- Type validation with Pydantic
- Easy integration with ML models

**API Design Principles:**
1. **RESTful**: Standard HTTP methods
2. **Versioned**: Support multiple API versions
3. **Documented**: Auto-generated docs
4. **Monitored**: Metrics and health checks
5. **Secure**: Input validation, rate limiting

### Hands-On Implementation

**Exercise 9.1: Understand API Structure**

```bash
# Review API code
cat src/serving/api.py | head -100

# Key components:
# - Pydantic models for input/output
# - Prediction endpoint
# - Health check endpoint
# - Metrics endpoint
```

**Exercise 9.2: Start API Locally**

```bash
# Ensure you have a trained model
ls models/best_model.pkl

# Start API server
make serve
# Or manually:
uvicorn src.serving.api:app --host 0.0.0.0 --port 8000 --reload

# API is now running at http://localhost:8000
```

**Exercise 9.3: Test API Endpoints**

```bash
# 1. API Information
curl http://localhost:8000/

# 2. Health Check
curl http://localhost:8000/health

# 3. Model Information
curl http://localhost:8000/model/info

# 4. Single Prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "population": 150000,
    "median_age": 42.5,
    "median_income": 55000,
    "education_rate": 0.85,
    "urban_ratio": 0.7,
    "prev_election_turnout": 0.68,
    "prev_winner_margin": 0.05,
    "voter_registration_rate": 0.82,
    "social_sentiment_score": 0.15,
    "candidate_a_favorability": 0.55,
    "candidate_b_favorability": 0.48,
    "poll_candidate_a": 0.48,
    "poll_candidate_b": 0.45,
    "undecided_rate": 0.07
  }'
```

**Exercise 9.4: Explore API Documentation**

Open your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try making predictions through the interactive UI!

**Exercise 9.5: Batch Predictions**

```bash
# Test batch prediction endpoint
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [
      {
        "population": 150000,
        "median_age": 42.5,
        ... (full features)
      },
      {
        "population": 200000,
        "median_age": 38.0,
        ... (full features)
      }
    ]
  }'

# Or run batch prediction script
make batch-predict
```

**Exercise 9.6: Prometheus Metrics**

```bash
# Check Prometheus metrics
curl http://localhost:8000/metrics

# You'll see metrics like:
# - election_api_requests_total
# - election_api_request_latency_seconds
# - election_prediction_confidence
```

**Exercise 9.7: Docker Containerization**

```bash
# Build Docker image
make docker-build
# Or manually:
docker build -t election-prediction-api:latest -f docker/Dockerfile.api .

# Run container
make docker-run
# Or manually:
docker run -d -p 8000:8000 --name election-api election-prediction-api:latest

# Test containerized API
curl http://localhost:8000/health

# View logs
docker logs election-api

# Stop container
make docker-stop
```

**Exercise 9.8: Load Testing**

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Run load test
ab -n 1000 -c 10 -p request.json -T application/json http://localhost:8000/predict

# Monitor metrics during load
watch -n 1 'curl -s http://localhost:8000/metrics | grep election_api'
```

### 🎯 Module Checkpoint
- [ ] FastAPI server running
- [ ] Can make predictions via API
- [ ] API documentation accessible
- [ ] Health checks working
- [ ] Prometheus metrics exported
- [ ] Docker image built and running

### 💡 Best Practices
- **Validation**: Always validate input data
- **Error Handling**: Return meaningful error messages
- **Logging**: Log all requests and errors
- **Versioning**: Include model version in responses
- **Documentation**: Keep API docs up to date

---

## Module 11: Monitoring & Drift Detection

### Learning Objectives
- Implement data drift detection
- Set up Prometheus monitoring
- Create Grafana dashboards
- Configure alerting rules
- Implement automated retraining triggers

### Theory

**Why Monitoring Matters:**
- Models degrade over time
- Data distributions change
- Catch issues early
- Ensure reliability

**Types of Drift:**
1. **Data Drift**: Input data distribution changes
2. **Concept Drift**: Relationship between features and target changes
3. **Prediction Drift**: Model predictions change

**Monitoring Stack:**
- **Evidently**: Drift detection library
- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **Alertmanager**: Alert routing

### Hands-On Implementation

**Exercise 11.1: Understand Drift Detection**

```bash
# Review drift monitoring code
cat src/monitoring/drift_monitoring.py

# Key concepts:
# - Reference data (training data)
# - Current data (production data)
# - Statistical tests (KS test, PSI)
# - Drift reports
```

**Exercise 11.2: Run Drift Detection**

```bash
# Check for drift
make monitor-drift
# Or manually:
python src/monitoring/drift_monitoring.py

# View drift report
ls -lh reports/
cat reports/drift_report.json
# Open HTML report in browser
open reports/drift_report.html
```

**Exercise 11.3: Interpret Drift Reports**

The report shows:
- **Dataset summary**: Statistics comparison
- **Feature drift**: Per-feature drift scores
- **Alerts**: Features with significant drift
- **Recommendations**: Actions to take

**Exercise 11.4: Set Up Prometheus**

```bash
# Review Prometheus configuration
cat prometheus/prometheus.yml

# Start Prometheus (via Docker Compose)
docker-compose up -d prometheus

# Access Prometheus UI
open http://localhost:9090
```

**Exercise 11.5: Query Prometheus Metrics**

In Prometheus UI (http://localhost:9090):

```promql
# Request rate
rate(election_api_requests_total[5m])

# Average latency
rate(election_api_request_latency_seconds_sum[5m]) / 
rate(election_api_request_latency_seconds_count[5m])

# P95 latency
histogram_quantile(0.95, 
  rate(election_api_request_latency_seconds_bucket[5m]))

# Prediction confidence
rate(election_prediction_confidence_sum[5m]) / 
rate(election_prediction_confidence_count[5m])
```

**Exercise 11.6: Set Up Grafana**

```bash
# Start Grafana
docker-compose up -d grafana

# Access Grafana
open http://localhost:3000
# Default credentials: admin/admin
```

**Configure Grafana:**
1. Add Prometheus data source:
   - URL: http://prometheus:9090
2. Import dashboard:
   - Upload `grafana/dashboards/election_prediction.json`
3. Explore the dashboard:
   - API metrics
   - Model performance
   - Drift detection status

**Exercise 11.7: Configure Alerts**

```bash
# Review alert rules
cat prometheus/rules/alerts.yml

# Key alerts:
# - HighAPILatency
# - HighErrorRate
# - DataDriftDetected
# - LowModelAccuracy
```

**Exercise 11.8: Implement Automated Retraining**

When drift is detected, trigger retraining:

```python
# In drift_monitoring.py
if drift_detected:
    logger.warning("Drift detected! Triggering retraining...")
    # Option 1: Direct call
    subprocess.run(["python", "src/train/train.py"])
    
    # Option 2: Airflow trigger (Module 12)
    # trigger_dag('model_retraining')
```

### 🎯 Module Checkpoint
- [ ] Drift detection running
- [ ] Understand drift reports
- [ ] Prometheus collecting metrics
- [ ] Grafana dashboard created
- [ ] Alert rules configured
- [ ] Understand retraining triggers

### 💡 Key Insights
- **Baseline**: Always compare against reference data
- **Thresholds**: Set appropriate drift thresholds
- **Automation**: Automate drift detection and retraining
- **Alerting**: Configure alerts for critical issues
- **Documentation**: Document what metrics mean

---

## Module 12: Orchestration with Airflow

### Learning Objectives
- Set up Apache Airflow
- Create DAGs for ML pipelines
- Schedule automated workflows
- Implement dependencies and retries
- Monitor pipeline execution

### Theory

**Apache Airflow:**
- Workflow orchestration platform
- DAGs (Directed Acyclic Graphs)
- Schedule and monitor tasks
- Handle dependencies and failures

**Our Pipelines:**
1. **Training Pipeline**: Weekly model retraining
2. **Batch Prediction**: Daily predictions
3. **Drift Detection**: Every 6 hours

### Hands-On Implementation

**Exercise 12.1: Initialize Airflow**

```bash
# Initialize Airflow database
make airflow-init
# Or manually:
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

# Start Airflow
make airflow-start
```

**Exercise 12.2: Explore Airflow DAGs**

```bash
# View DAG files
ls airflow/dags/

# Key DAGs:
# - training_pipeline_dag.py
# - batch_prediction_dag.py
# - drift_monitoring_dag.py
```

**Exercise 12.3: Training Pipeline DAG**

```python
# airflow/dags/training_pipeline_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mlops-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'training_pipeline',
    default_args=default_args,
    schedule_interval='@weekly',  # Run every week
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Tasks
generate_data = PythonOperator(
    task_id='generate_data',
    python_callable=run_data_generation,
    dag=dag,
)

preprocess_data = PythonOperator(
    task_id='preprocess_data',
    python_callable=run_preprocessing,
    dag=dag,
)

train_models = PythonOperator(
    task_id='train_models',
    python_callable=run_training,
    dag=dag,
)

evaluate_models = PythonOperator(
    task_id='evaluate_models',
    python_callable=run_evaluation,
    dag=dag,
)

# Dependencies
generate_data >> preprocess_data >> train_models >> evaluate_models
```

**Exercise 12.4: Access Airflow UI**

```bash
# Airflow UI
open http://localhost:8080
# Login: admin/admin
```

In the UI:
1. View all DAGs
2. Enable DAGs
3. Trigger manual runs
4. View task logs
5. Monitor task status

**Exercise 12.5: Batch Prediction DAG**

```bash
# Review batch prediction DAG
cat airflow/dags/batch_prediction_dag.py

# This DAG:
# 1. Loads new data
# 2. Runs predictions
# 3. Saves results
# 4. Generates reports
# Schedule: Daily at 2 AM
```

**Exercise 12.6: Drift Monitoring DAG**

```bash
# Review drift monitoring DAG
cat airflow/dags/drift_monitoring_dag.py

# This DAG:
# 1. Collects production data
# 2. Runs drift detection
# 3. Generates reports
# 4. Triggers retraining if needed
# Schedule: Every 6 hours
```

**Exercise 12.7: Trigger and Monitor DAGs**

In Airflow UI:
1. Click on "training_pipeline" DAG
2. Click "Trigger DAG" button
3. Watch tasks execute
4. Click on tasks to view logs
5. Check for errors or warnings

**Exercise 12.8: Configure Notifications**

Add email notifications on failure:

```python
from airflow.operators.email_operator import EmailOperator

send_failure_email = EmailOperator(
    task_id='send_failure_email',
    to='team@example.com',
    subject='Training Pipeline Failed',
    html_content='<p>Check Airflow logs</p>',
    trigger_rule='one_failed',
    dag=dag,
)
```

### 🎯 Module Checkpoint
- [ ] Airflow installed and running
- [ ] All DAGs visible in UI
- [ ] Can trigger DAGs manually
- [ ] Understand DAG structure
- [ ] Can view task logs
- [ ] Understand scheduling

### 💡 Best Practices
- **Idempotency**: Tasks should be rerunnable
- **Modularity**: Break complex tasks into smaller ones
- **Logging**: Add comprehensive logging
- **Error Handling**: Handle failures gracefully
- **Testing**: Test DAGs locally before deploying

---

## Module 13: Kubernetes Deployment

### Learning Objectives
- Understand Kubernetes concepts
- Deploy API to Kubernetes
- Configure auto-scaling
- Implement health checks
- Set up RBAC and security

### Theory

**Kubernetes Components:**
- **Pods**: Smallest deployable units
- **Deployments**: Manage pod replicas
- **Services**: Expose pods to network
- **HPA**: Horizontal Pod Autoscaler
- **ConfigMaps/Secrets**: Configuration management

**Why Kubernetes?**
- Container orchestration
- Auto-scaling
- Self-healing
- Load balancing
- Rolling updates

### Hands-On Implementation

**Exercise 13.1: Set Up Local Kubernetes**

```bash
# Option 1: Docker Desktop
# Enable Kubernetes in Docker Desktop settings

# Option 2: Minikube
minikube start --memory=4096 --cpus=2

# Verify cluster
kubectl cluster-info
kubectl get nodes
```

**Exercise 13.2: Review Kubernetes Manifests**

```bash
# View deployment configuration
cat kubernetes/deployment.yaml

# Key settings:
# - 3 replicas
# - Resource limits
# - Liveness/readiness probes
# - Environment variables
```

**Exercise 13.3: Create Namespace**

```bash
# Create mlops namespace
kubectl create namespace mlops

# Set as default
kubectl config set-context --current --namespace=mlops

# Verify
kubectl get namespaces
```

**Exercise 13.4: Deploy Application**

```bash
# Deploy all components
make k8s-deploy
# Or manually:
kubectl apply -f kubernetes/deployment.yaml -n mlops
kubectl apply -f kubernetes/service.yaml -n mlops
kubectl apply -f kubernetes/hpa.yaml -n mlops
kubectl apply -f kubernetes/rbac.yaml -n mlops

# Check deployment status
make k8s-status
# Or manually:
kubectl get all -n mlops
```

**Exercise 13.5: Understand Deployment**

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: election-prediction
spec:
  replicas: 3  # Run 3 pods
  selector:
    matchLabels:
      app: election-prediction
  template:
    spec:
      containers:
      - name: api
        image: election-prediction-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**Exercise 13.6: Access the Service**

```bash
# Get service URL
kubectl get svc -n mlops

# Port forward to local machine
kubectl port-forward svc/election-prediction 8000:8000 -n mlops

# Test API
curl http://localhost:8000/health
```

**Exercise 13.7: Configure Auto-Scaling**

```bash
# Review HPA configuration
cat kubernetes/hpa.yaml

# HPA automatically scales between 2-10 pods
# based on CPU utilization (>70%)

# Check HPA status
kubectl get hpa -n mlops

# Describe HPA
kubectl describe hpa election-prediction -n mlops
```

**Exercise 13.8: Load Test Auto-Scaling**

```bash
# Generate load
kubectl run -it --rm load-generator \
  --image=busybox \
  --restart=Never \
  -- /bin/sh -c "while true; do wget -q -O- http://election-prediction:8000/health; done"

# Watch pods scale up
watch kubectl get pods -n mlops

# Watch HPA metrics
watch kubectl get hpa -n mlops
```

**Exercise 13.9: View Logs**

```bash
# View logs from all pods
make k8s-logs

# View specific pod logs
kubectl logs -f <pod-name> -n mlops

# Stream logs from all pods
kubectl logs -f -l app=election-prediction -n mlops
```

**Exercise 13.10: Rolling Updates**

```bash
# Update image
kubectl set image deployment/election-prediction \
  api=election-prediction-api:v2.0 \
  -n mlops

# Watch rollout
kubectl rollout status deployment/election-prediction -n mlops

# View rollout history
kubectl rollout history deployment/election-prediction -n mlops

# Rollback if needed
kubectl rollout undo deployment/election-prediction -n mlops
```

### 🎯 Module Checkpoint
- [ ] Kubernetes cluster running
- [ ] Application deployed successfully
- [ ] Can access API through service
- [ ] Auto-scaling configured
- [ ] Health checks working
- [ ] Can view logs and metrics

### 💡 Production Tips
- **Resource Limits**: Always set CPU/memory limits
- **Health Checks**: Implement proper liveness/readiness probes
- **Secrets**: Never commit secrets to Git
- **Namespaces**: Isolate environments (dev/staging/prod)
- **Monitoring**: Integrate with Prometheus/Grafana

---

## Module 14: CI/CD & Production Best Practices

### Learning Objectives
- Implement CI/CD pipeline
- Set up automated testing
- Configure security scanning
- Deploy to multiple environments
- Implement best practices

### Theory

**CI/CD Benefits:**
- Automated testing
- Fast feedback
- Consistent deployments
- Reduced errors
- Increased velocity

**Pipeline Stages:**
1. **Lint**: Code quality checks
2. **Test**: Unit and integration tests
3. **Security**: Vulnerability scanning
4. **Build**: Docker image creation
5. **Deploy**: Push to environments

### Hands-On Implementation

**Exercise 14.1: Review CI/CD Workflow**

```bash
# View GitHub Actions workflow
cat .github/workflows/ci-cd.yml

# Pipeline stages:
# 1. Security scans (Gitleaks)
# 2. Code linting
# 3. Unit tests
# 4. Build Docker image
# 5. Security scan image (Trivy)
# 6. Deploy to environments
# 7. Smoke tests
```

**Exercise 14.2: Run Linting Locally**

```bash
# Run linting checks
make lint

# Or individually:
flake8 src/ --max-line-length=100
pylint src/ --disable=C0111
```

**Exercise 14.3: Run Tests Locally**

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html
```

**Exercise 14.4: Security Scanning**

```bash
# Scan for secrets
gitleaks detect --source . --config src/security/gitleaks.toml

# Scan Docker image
make security-scan

# Generate SBOM
make security-sbom
```

**Exercise 14.5: Build and Tag Image**

```bash
# Build with version tag
docker build -t election-prediction-api:v1.0.0 -f docker/Dockerfile.api .

# Tag for registry
docker tag election-prediction-api:v1.0.0 \
  your-registry.com/election-prediction-api:v1.0.0

# Push to registry
docker push your-registry.com/election-prediction-api:v1.0.0
```

**Exercise 14.6: Multi-Environment Deployment**

```bash
# Deploy to dev
kubectl apply -f kubernetes/deployment.yaml -n dev

# Run smoke tests
curl https://api-dev.example.com/health

# Deploy to staging
kubectl apply -f kubernetes/deployment.yaml -n staging

# Run integration tests
pytest tests/integration/

# Deploy to production (with approval)
kubectl apply -f kubernetes/deployment.yaml -n production
```

**Exercise 14.7: Implement Blue-Green Deployment**

```bash
# Deploy green version
kubectl apply -f kubernetes/deployment-green.yaml

# Test green version
curl http://green.api.example.com/health

# Switch traffic to green
kubectl patch service election-prediction \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Keep blue for rollback
# Delete blue when stable
kubectl delete deployment election-prediction-blue
```

**Exercise 14.8: Configure Monitoring Alerts**

```yaml
# prometheus/rules/alerts.yml
groups:
  - name: election_prediction
    interval: 30s
    rules:
      - alert: HighAPILatency
        expr: histogram_quantile(0.95, 
                rate(election_api_request_latency_seconds_bucket[5m])) > 1
        for: 5m
        annotations:
          summary: "High API latency detected"
          
      - alert: DataDriftDetected
        expr: election_drift_detected == 1
        for: 1h
        annotations:
          summary: "Data drift detected, consider retraining"
```

**Exercise 14.9: Implement Backup Strategy**

```bash
# Backup models
aws s3 sync models/ s3://backup-bucket/models/$(date +%Y%m%d)/

# Backup data
dvc push

# Backup database (if using one)
pg_dump database > backup.sql
```

**Exercise 14.10: Documentation and Runbooks**

Create runbooks for common scenarios:

```markdown
# Runbook: Model Accuracy Degradation

## Symptoms
- Model accuracy below 80%
- Increased prediction errors
- User complaints

## Diagnosis
1. Check Grafana dashboard
2. Review drift reports
3. Examine recent data

## Resolution
1. Trigger retraining: `make train`
2. Validate new model: `make evaluate`
3. Deploy if improved: `make k8s-deploy`
4. Monitor for 24 hours

## Prevention
- Automated drift detection
- Regular retraining schedule
- Data quality checks
```

### 🎯 Module Checkpoint
- [ ] CI/CD pipeline configured
- [ ] All tests passing
- [ ] Security scans clean
- [ ] Multi-environment setup
- [ ] Monitoring and alerts configured
- [ ] Documentation complete

### 💡 Production Best Practices

**Code Quality:**
- Use type hints
- Write comprehensive tests
- Follow PEP 8 style guide
- Code reviews mandatory

**Security:**
- Scan dependencies regularly
- Use secrets management
- Implement RBAC
- Enable audit logging

**Monitoring:**
- Track all key metrics
- Set up alerts
- Create dashboards
- Regular reviews

**Operations:**
- Automate everything
- Document procedures
- Test disaster recovery
- Regular backups

---

## 🎓 Final Project Assessment

### Project Completion Checklist

**Data Pipeline (20 points)**
- [ ] Data generation working
- [ ] Preprocessing implemented
- [ ] Feature engineering complete
- [ ] DVC versioning configured
- [ ] Data quality validation

**Model Training (20 points)**
- [ ] Multiple models trained
- [ ] MLflow tracking configured
- [ ] Hyperparameter tuning implemented
- [ ] Model evaluation complete
- [ ] Best model registered

**Model Serving (20 points)**
- [ ] FastAPI endpoints working
- [ ] Input validation implemented
- [ ] Error handling robust
- [ ] API documentation complete
- [ ] Docker containerization

**Monitoring (15 points)**
- [ ] Drift detection implemented
- [ ] Prometheus metrics exported
- [ ] Grafana dashboards created
- [ ] Alerts configured
- [ ] Automated retraining

**Orchestration (10 points)**
- [ ] Airflow DAGs created
- [ ] Pipelines scheduled
- [ ] Task dependencies correct
- [ ] Error handling implemented

**Deployment (15 points)**
- [ ] Kubernetes deployment
- [ ] Auto-scaling configured
- [ ] Health checks working
- [ ] CI/CD pipeline functional
- [ ] Multi-environment setup

**Total: 100 points**

### Advanced Challenges (Bonus)

1. **A/B Testing (10 points)**
   - Implement model A/B testing
   - Route traffic between models
   - Compare performance

2. **Model Explainability (10 points)**
   - Add SHAP values
   - Create explanation endpoint
   - Visualize feature importance

3. **Real-time Streaming (15 points)**
   - Kafka integration
   - Real-time predictions
   - Stream processing

4. **Multi-region Deployment (15 points)**
   - Deploy to multiple regions
   - Global load balancing
   - Data replication

---

## 🐛 Troubleshooting Guide

### Common Issues and Solutions

**Issue: MLflow UI not accessible**
```bash
# Solution 1: Check if running
ps aux | grep mlflow

# Solution 2: Restart MLflow
pkill mlflow
make mlflow-ui

# Solution 3: Check firewall
sudo ufw allow 5000
```

**Issue: Docker build fails**
```bash
# Solution 1: Clean Docker cache
docker system prune -a

# Solution 2: Check Dockerfile path
ls docker/Dockerfile.api

# Solution 3: Build with no cache
docker build --no-cache -t election-prediction-api .
```

**Issue: Kubernetes pods not starting**
```bash
# Solution 1: Check pod status
kubectl describe pod <pod-name> -n mlops

# Solution 2: Check logs
kubectl logs <pod-name> -n mlops

# Solution 3: Check resource limits
kubectl top nodes
kubectl top pods -n mlops

# Solution 4: Check image pull
kubectl get events -n mlops
```

**Issue: Model predictions incorrect**
```bash
# Solution 1: Verify model file
ls -lh models/best_model.pkl

# Solution 2: Check feature names
python -c "import joblib; model = joblib.load('models/best_model.pkl'); print(model.feature_names_in_)"

# Solution 3: Validate input data
# Ensure feature order matches training data
```

**Issue: Drift detection always triggers**
```bash
# Solution 1: Check reference data
ls data/features/train_features.csv

# Solution 2: Adjust thresholds
# Edit src/monitoring/drift_monitoring.py
# Increase drift threshold

# Solution 3: Update reference data
# Retrain with recent data
make pipeline
```

---

## 📚 Additional Resources

### Recommended Reading
- **Books:**
  - "Designing Machine Learning Systems" by Chip Huyen
  - "Machine Learning Engineering" by Andriy Burkov
  - "Building Machine Learning Powered Applications" by Emmanuel Ameisen

### Online Courses
- MLOps Specialization (DeepLearning.AI)
- Full Stack Deep Learning
- Made With ML

### Documentation
- MLflow: https://mlflow.org/docs/
- DVC: https://dvc.org/doc
- FastAPI: https://fastapi.tiangolo.com/
- Kubernetes: https://kubernetes.io/docs/
- Prometheus: https://prometheus.io/docs/

### Communities
- MLOps Community Slack
- r/MachineLearning Reddit
- Kubernetes Slack

---

## 🎉 Congratulations!

You've completed the **Complete MLOps Course**! You now have:

✅ Built a production-ready ML system  
✅ Implemented the full ML lifecycle  
✅ Mastered modern MLOps tools  
✅ Deployed to Kubernetes  
✅ Set up monitoring and alerts  
✅ Created CI/CD pipelines  

### Next Steps

1. **Customize the project**: Add your own features and models
2. **Deploy to cloud**: Try AWS, GCP, or Azure
3. **Contribute**: Improve the project and share with community
4. **Build portfolio**: Showcase this project to employers
5. **Keep learning**: Explore advanced topics (A/B testing, feature stores, etc.)

### Share Your Success

- Star this repository ⭐
- Share on LinkedIn
- Write a blog post about your learnings
- Help other students in the community

---

## 📞 Support and Feedback

### Getting Help

- **GitHub Issues**: https://github.com/yourusername/MLops-Election/issues
- **Slack Channel**: #mlops-course
- **Email**: mlops-course@example.com
- **Office Hours**: Tuesdays 2-4 PM EST

### Course Feedback

We continuously improve this course. Please share your feedback:

- What worked well?
- What was confusing?
- What topics need more coverage?
- Suggestions for improvement?

### Certificate

Upon completing all modules and the final project:
1. Submit your completed project
2. Pass the assessment (70% minimum)
3. Receive your **MLOps Professional Certificate**

---

**Made with ❤️ by the MLOps Course Team**

*Last Updated: November 2024*
