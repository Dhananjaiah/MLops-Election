# Makefile for Election Prediction MLOps System

.PHONY: help install clean test lint format train serve docker-build docker-run deploy monitor security all

# Variables
PYTHON := python3
PIP := pip3
DOCKER_IMAGE := election-prediction-api
DOCKER_TAG := latest
NAMESPACE := mlops

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(CYAN)Election Prediction MLOps System$(NC)"
	@echo "$(GREEN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install Python dependencies
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

install-dev: ## Install development dependencies
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 isort pylint
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

clean: ## Clean generated files and caches
	@echo "$(GREEN)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache .coverage htmlcov
	rm -rf build dist
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

format: ## Format code with black and isort
	@echo "$(GREEN)Formatting code...$(NC)"
	black src/
	isort src/
	@echo "$(GREEN)✓ Code formatted$(NC)"

lint: ## Run linting checks
	@echo "$(GREEN)Running linting checks...$(NC)"
	flake8 src/ --max-line-length=100 --ignore=E203,W503
	pylint src/ --disable=C0111,R0913,R0914
	@echo "$(GREEN)✓ Linting complete$(NC)"

test: ## Run unit tests
	@echo "$(GREEN)Running tests...$(NC)"
	pytest tests/ -v --cov=src --cov-report=term --cov-report=html
	@echo "$(GREEN)✓ Tests complete$(NC)"

data: ## Generate and preprocess data
	@echo "$(GREEN)Generating dataset...$(NC)"
	$(PYTHON) src/data/make_dataset.py
	@echo "$(GREEN)Preprocessing data...$(NC)"
	$(PYTHON) src/data/preprocess.py
	@echo "$(GREEN)Engineering features...$(NC)"
	$(PYTHON) src/data/features.py
	@echo "$(GREEN)✓ Data pipeline complete$(NC)"

train: ## Train models
	@echo "$(GREEN)Training models...$(NC)"
	$(PYTHON) src/train/train.py
	@echo "$(GREEN)✓ Training complete$(NC)"

evaluate: ## Evaluate trained models
	@echo "$(GREEN)Evaluating models...$(NC)"
	$(PYTHON) src/train/evaluate.py
	$(PYTHON) src/train/compare_models.py
	@echo "$(GREEN)✓ Evaluation complete$(NC)"

pipeline: data train evaluate ## Run complete ML pipeline
	@echo "$(GREEN)✓ Complete pipeline executed$(NC)"

serve: ## Start FastAPI server locally
	@echo "$(GREEN)Starting API server...$(NC)"
	uvicorn src.serving.api:app --host 0.0.0.0 --port 8000 --reload

batch-predict: ## Run batch predictions
	@echo "$(GREEN)Running batch predictions...$(NC)"
	$(PYTHON) src/serving/batch_predict.py
	@echo "$(GREEN)✓ Batch predictions complete$(NC)"

monitor-drift: ## Check for data drift
	@echo "$(GREEN)Monitoring for drift...$(NC)"
	$(PYTHON) src/monitoring/drift_monitoring.py
	@echo "$(GREEN)✓ Drift monitoring complete$(NC)"

security-scan: ## Run security scans
	@echo "$(GREEN)Running security scans...$(NC)"
	bash src/security/scan_cves.sh $(DOCKER_IMAGE) $(DOCKER_TAG)
	@echo "$(GREEN)✓ Security scan complete$(NC)"

security-sbom: ## Generate SBOM
	@echo "$(GREEN)Generating SBOM...$(NC)"
	bash src/security/sbom_generate.sh . spdx-json
	@echo "$(GREEN)✓ SBOM generated$(NC)"

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) -f docker/Dockerfile.api .
	@echo "$(GREEN)✓ Docker image built$(NC)"

docker-run: ## Run Docker container
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run -d -p 8000:8000 --name election-api $(DOCKER_IMAGE):$(DOCKER_TAG)
	@echo "$(GREEN)✓ Container started at http://localhost:8000$(NC)"

docker-stop: ## Stop Docker container
	@echo "$(GREEN)Stopping Docker container...$(NC)"
	docker stop election-api || true
	docker rm election-api || true
	@echo "$(GREEN)✓ Container stopped$(NC)"

k8s-deploy: ## Deploy to Kubernetes
	@echo "$(GREEN)Deploying to Kubernetes...$(NC)"
	kubectl apply -f kubernetes/deployment.yaml -n $(NAMESPACE)
	kubectl apply -f kubernetes/service.yaml -n $(NAMESPACE)
	kubectl apply -f kubernetes/hpa.yaml -n $(NAMESPACE)
	kubectl apply -f kubernetes/rbac.yaml -n $(NAMESPACE)
	@echo "$(GREEN)✓ Deployed to Kubernetes$(NC)"

k8s-status: ## Check Kubernetes deployment status
	@echo "$(GREEN)Checking deployment status...$(NC)"
	kubectl get all -n $(NAMESPACE) -l app=election-prediction
	@echo "$(GREEN)✓ Status check complete$(NC)"

k8s-logs: ## View Kubernetes logs
	@echo "$(GREEN)Fetching logs...$(NC)"
	kubectl logs -n $(NAMESPACE) -l app=election-prediction --tail=100

prometheus-deploy: ## Deploy Prometheus
	@echo "$(GREEN)Deploying Prometheus...$(NC)"
	kubectl apply -f prometheus/prometheus.yml -n monitoring
	@echo "$(GREEN)✓ Prometheus deployed$(NC)"

grafana-deploy: ## Deploy Grafana dashboards
	@echo "$(GREEN)Deploying Grafana dashboards...$(NC)"
	kubectl apply -f grafana/dashboards/ -n monitoring
	@echo "$(GREEN)✓ Grafana dashboards deployed$(NC)"

all: clean install pipeline docker-build ## Run complete setup
	@echo "$(GREEN)✓ Complete setup finished$(NC)"

dvc-init: ## Initialize DVC
	@echo "$(GREEN)Initializing DVC...$(NC)"
	dvc init
	dvc remote add -d storage s3://my-bucket/dvc-storage
	@echo "$(GREEN)✓ DVC initialized$(NC)"

dvc-push: ## Push data and models to DVC remote
	@echo "$(GREEN)Pushing to DVC remote...$(NC)"
	dvc push
	@echo "$(GREEN)✓ DVC push complete$(NC)"

dvc-pull: ## Pull data and models from DVC remote
	@echo "$(GREEN)Pulling from DVC remote...$(NC)"
	dvc pull
	@echo "$(GREEN)✓ DVC pull complete$(NC)"

mlflow-ui: ## Start MLflow UI
	@echo "$(GREEN)Starting MLflow UI...$(NC)"
	mlflow ui --host 0.0.0.0 --port 5000

airflow-init: ## Initialize Airflow
	@echo "$(GREEN)Initializing Airflow...$(NC)"
	airflow db init
	airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
	@echo "$(GREEN)✓ Airflow initialized$(NC)"

airflow-start: ## Start Airflow webserver and scheduler
	@echo "$(GREEN)Starting Airflow...$(NC)"
	airflow webserver -p 8080 -D
	airflow scheduler -D
	@echo "$(GREEN)✓ Airflow started at http://localhost:8080$(NC)"

ci: lint test ## Run CI checks
	@echo "$(GREEN)✓ CI checks passed$(NC)"

.DEFAULT_GOAL := help
