# Customer Churn Prediction - Reference Project

This is the end-to-end reference project for the MLOps course. It demonstrates a complete ML system from data processing to production deployment.

## 🎯 Business Problem

**Goal**: Predict which customers are likely to cancel their subscription (churn) so the business can take proactive retention actions.

**Success Metrics**:
- Model accuracy > 80%
- API latency < 100ms (p95)
- System uptime > 99.9%

## 📁 Project Structure

```
project/
├── src/
│   └── churn_mlops/          # Main Python package
│       ├── data/             # Data loading & validation
│       ├── features/         # Feature engineering
│       ├── models/           # Model training & inference
│       ├── serving/          # FastAPI application
│       └── pipelines/        # Orchestration pipelines
├── notebooks/                # Exploration notebooks
├── config/                   # Configuration files
├── tests/                    # Unit & integration tests
├── Dockerfile               # Container definition
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Python dependencies
└── pyproject.toml           # Project metadata
```

## 🚀 Quick Start

### 1. Set Up Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Train a Model

```bash
# Train with default configuration
PYTHONPATH=src python -m churn_mlops.models.train

# Or with custom config
PYTHONPATH=src python -m churn_mlops.models.train --config config/config.yaml
```

### 3. Start the API

```bash
# Development mode
PYTHONPATH=src uvicorn churn_mlops.serving.app:app --reload

# Production mode
PYTHONPATH=src uvicorn churn_mlops.serving.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure": 24,
    "monthly_charges": 65.50,
    "total_charges": 1572.00
  }'
```

## 🐳 Docker

### Build and Run

```bash
# Build image
docker build -t churn-prediction-api .

# Run container
docker run -p 8000:8000 churn-prediction-api
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🧪 Testing

```bash
# Run all tests
PYTHONPATH=src pytest tests/ -v

# Run with coverage
PYTHONPATH=src pytest tests/ -v --cov=churn_mlops --cov-report=html

# Run specific test file
PYTHONPATH=src pytest tests/test_models.py -v
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Single prediction |
| `/predict/batch` | POST | Batch predictions |
| `/model/info` | GET | Model information |
| `/docs` | GET | OpenAPI documentation |

## 📝 Configuration

Edit `config/config.yaml` to customize:

- Model type and hyperparameters
- Data paths
- Feature engineering settings
- API configuration

## 🔧 Development

### Code Style

```bash
# Format code
black src tests
isort src tests

# Lint
flake8 src tests
mypy src
```

### Adding New Features

1. Add feature logic in `src/churn_mlops/features/`
2. Update configuration if needed
3. Add tests in `tests/`
4. Update documentation

## 📚 Related Course Sections

- **Section 4**: Project overview
- **Section 5**: Data engineering
- **Section 6**: Experimentation
- **Section 7**: Model packaging
- **Section 10**: CI/CD
- **Section 14**: Capstone walkthrough

## ❓ Troubleshooting

**Model not found**: Train a model first with `python -m churn_mlops.models.train`

**Import errors**: Ensure `PYTHONPATH=src` is set

**Port in use**: Change port in config or use different port: `--port 8001`

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details.
