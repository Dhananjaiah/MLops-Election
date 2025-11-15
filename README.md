# 🗳️ Election Prediction System - Production MLOps

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![MLOps](https://img.shields.io/badge/MLOps-Production%20Ready-brightgreen)

A complete, production-ready MLOps system for predicting election outcomes using machine learning. This project demonstrates end-to-end ML lifecycle management including data pipelines, model training, serving, monitoring, and automated retraining.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project predicts which candidate will win in each region using features like:
- **Demographics**: Population, median age, income, education rates, urban ratio
- **Voting History**: Past turnout, winner margins, registration rates
- **Surveys**: Poll results, undecided voter rates
- **Sentiment**: Social media sentiment scores, candidate favorability

### Key Capabilities

- ✅ Automated data pipeline with DVC version control
- ✅ Multi-model training with MLflow tracking
- ✅ FastAPI REST API for real-time predictions
- ✅ Batch prediction pipeline with Airflow
- ✅ Drift detection and automated retraining
- ✅ Kubernetes deployment with auto-scaling
- ✅ Comprehensive monitoring with Prometheus & Grafana
- ✅ Security scanning and SBOM generation
- ✅ Complete CI/CD pipeline with GitHub Actions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA PIPELINE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  Raw Data → Preprocessing → Feature Engineering → Model Training        │
│     ↓            ↓                 ↓                    ↓                │
│   DVC        Validation       DVC Tracking         MLflow               │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                        MODEL REGISTRY                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  MLflow Model Registry → Best Model Selection → Version Control         │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                          SERVING LAYER                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  FastAPI REST API  ←→  Kubernetes  ←→  Load Balancer                   │
│       ↓                    ↓                                             │
│  Batch Predictions    Auto-scaling                                      │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                     MONITORING & OBSERVABILITY                          │
├─────────────────────────────────────────────────────────────────────────┤
│  Prometheus Metrics → Grafana Dashboards → Alertmanager                │
│  Evidently Drift Detection → Automated Retraining Trigger               │
└─────────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  Airflow DAGs:                                                          │
│    - Training Pipeline (Weekly)                                         │
│    - Batch Scoring (Daily)                                              │
│    - Drift Detection & Retrain (Every 6 hours)                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## ✨ Features

### Data Pipeline
- Automated data generation and validation
- Feature engineering with 20+ engineered features
- Data versioning with DVC
- Preprocessing with outlier detection and handling

### Model Training
- Multi-model training (Random Forest, XGBoost, Logistic Regression)
- Hyperparameter tuning with GridSearchCV
- Experiment tracking with MLflow
- Automated best model selection
- Model registry integration

### Serving
- FastAPI REST API with automatic documentation
- Health check and metrics endpoints
- Batch prediction capabilities
- Prometheus metrics export
- Docker containerization

### Monitoring
- Real-time drift detection with Evidently
- Performance metrics tracking
- Prometheus alerting rules
- Grafana dashboards with:
  - API latency and throughput
  - Model accuracy and confidence
  - Drift detection status
  - Resource utilization

### Automation
- Airflow DAGs for pipeline orchestration
- Automated retraining on drift detection
- Scheduled batch predictions
- CI/CD with GitHub Actions

### Security
- Trivy vulnerability scanning
- SBOM generation with Syft
- Gitleaks secret detection
- RBAC in Kubernetes
- Network policies

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **ML/Data** | Python, Pandas, NumPy, Scikit-learn, XGBoost |
| **MLOps** | MLflow, DVC, Evidently |
| **API** | FastAPI, Uvicorn |
| **Orchestration** | Apache Airflow |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes |
| **Monitoring** | Prometheus, Grafana |
| **CI/CD** | GitHub Actions |
| **Security** | Trivy, Syft, Gitleaks |

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Kubernetes cluster (optional, for deployment)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MLops-Election.git
   cd MLops-Election
   ```

2. **Install dependencies**
   ```bash
   make install
   # Or manually:
   pip install -r requirements.txt
   ```

3. **Set up configuration**
   ```bash
   # Copy and edit configuration
   export MLFLOW_TRACKING_URI=http://localhost:5000
   export API_PORT=8000
   ```

### Quick Start

Run the complete pipeline:
```bash
make pipeline
```

This will:
1. Generate synthetic election data
2. Preprocess and engineer features
3. Train multiple models
4. Evaluate and compare models
5. Select the best model

## 📖 Usage

### Training a Model

```bash
# Run complete data pipeline
make data

# Train models with MLflow tracking
make train

# Evaluate models
make evaluate
```

### Starting the API Server

```bash
# Local development
make serve

# Or with Docker
make docker-build
make docker-run
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Single prediction
- `POST /predict/batch` - Batch predictions
- `GET /metrics` - Prometheus metrics
- `GET /model/info` - Model information

### Example API Request

```bash
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

Response:
```json
{
  "predicted_winner": "Candidate_A",
  "confidence": 0.87,
  "probabilities": {
    "Candidate_A": 0.87,
    "Candidate_B": 0.13
  },
  "model_version": "1.0.0"
}
```

### Batch Predictions

```bash
make batch-predict
```

### Drift Monitoring

```bash
# Check for data drift
make monitor-drift

# View drift reports
cat reports/drift_report.json
open reports/drift_report.html
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build image
make docker-build

# Run container
make docker-run

# Check status
docker ps

# View logs
docker logs election-api
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes
make k8s-deploy

# Check deployment status
make k8s-status

# View logs
make k8s-logs
```

The deployment includes:
- Deployment with 3 replicas
- LoadBalancer service
- Horizontal Pod Autoscaler (2-10 replicas)
- RBAC and network policies

### CI/CD Pipeline

The GitHub Actions workflow automatically:
1. Runs security scans (Gitleaks)
2. Executes unit tests
3. Performs linting checks
4. Builds Docker image
5. Scans with Trivy
6. Deploys to dev/staging/production
7. Runs smoke tests
8. Sends notifications

## 📊 Monitoring

### Prometheus Metrics

- `election_api_requests_total` - Total API requests
- `election_api_request_latency_seconds` - Request latency
- `election_prediction_confidence` - Prediction confidence
- `election_drift_detected` - Drift detection status
- `election_model_accuracy` - Model accuracy

### Grafana Dashboards

Access Grafana at `http://localhost:3000` (default credentials: admin/admin)

The dashboard includes:
- API request rate and latency (P95, P99)
- Error rates
- Model accuracy gauge
- Drift detection status
- Prediction confidence distribution
- Resource utilization (CPU, memory)

### Alerts

Configured alerts for:
- High API latency (>1s)
- High error rate (>5%)
- Data drift detected
- Low model accuracy (<80%)
- High CPU/memory usage
- Pod crash looping

## 🔒 Security

### Security Scanning

```bash
# Scan Docker image for vulnerabilities
make security-scan

# Generate SBOM
make security-sbom

# Check for secrets
gitleaks detect --source . --config src/security/gitleaks.toml
```

### Security Features

- Non-root container user
- Read-only model volumes
- Network policies in Kubernetes
- RBAC for pod permissions
- Automated vulnerability scanning
- Secret detection in CI/CD
- SBOM generation

## 🐛 Troubleshooting

### Common Issues

**Issue: Model not found**
```bash
# Solution: Train the model first
make train
```

**Issue: API returns 500 error**
```bash
# Check logs
docker logs election-api
# Or in Kubernetes
kubectl logs -n mlops -l app=election-prediction
```

**Issue: High memory usage**
```bash
# Reduce batch size or workers
export API_WORKERS=2
```

**Issue: Drift detected but no retrain**
```bash
# Manually trigger retraining
python src/train/train.py
```

### Debugging

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python src/serving/api.py
```

View detailed metrics:
```bash
curl http://localhost:8000/metrics
```

## 📈 MLOps Roadmap

- [x] Data pipeline with versioning
- [x] Model training and tracking
- [x] API serving
- [x] Batch predictions
- [x] Drift monitoring
- [x] Automated retraining
- [x] Kubernetes deployment
- [x] Monitoring and alerting
- [x] CI/CD pipeline
- [x] Security scanning
- [ ] A/B testing framework
- [ ] Model explainability (SHAP)
- [ ] Multi-region deployment
- [ ] Model serving optimization
- [ ] Advanced feature store
- [ ] Real-time streaming predictions

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Credits

- Built as part of the 14-module MLOps course
- Inspired by real-world production ML systems
- Community contributions welcome

## 📧 Contact

For questions or feedback:
- Open an issue on GitHub
- Email: mlops-team@example.com
- Slack: #election-prediction

---

**⭐ If you find this project useful, please give it a star!**
