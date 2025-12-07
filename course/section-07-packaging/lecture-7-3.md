# Lecture 7.3 – Building a REST API with FastAPI / Flask for the Model

## In This Lecture You Will Learn

- [x] How to wrap your model inference function in a web service
- [x] FastAPI vs Flask: choosing the right framework for ML APIs
- [x] Designing production-ready API endpoints (health checks, predictions, metadata)
- [x] Request validation, error handling, and response formatting
- [x] Local testing and API documentation with Swagger/OpenAPI

---

## Real-World Context

> **Story**: The $2M Debugging Session
>
> A fintech startup deployed their fraud detection model by SSH'ing into a production server and running `python predict.py` manually. When fraud spiked on Black Friday, they couldn't scale—their data scientist was on vacation, and nobody else knew the magic command-line arguments. They lost $2M in fraudulent transactions while frantically texting her poolside in Bali.
>
> **The lesson**: Models that aren't wrapped in APIs aren't production systems—they're artisanal scripts.

### Why REST APIs for ML Models?

In the real world, teams often struggle with:
- **No standard interface**: Every consumer needs custom integration code
- **Can't scale**: Command-line scripts don't handle 1000 RPS
- **Manual dependency hell**: "It works on my laptop" syndrome
- **No observability**: No metrics, logs, or health checks
- **Security nightmare**: Direct model access = no authentication/rate limiting

**REST APIs solve this** by providing:
✅ Standard HTTP interface (any language can call it)  
✅ Horizontal scaling (load balancers + multiple instances)  
✅ Containerizable (Docker → Kubernetes)  
✅ Observable (Prometheus metrics, structured logs)  
✅ Secure (API keys, rate limits, input validation)

---

## Main Content

### 1. FastAPI vs Flask: Choosing Your Framework

| Feature | FastAPI | Flask | Recommendation |
|---------|---------|-------|---------------|
| **Speed** | 🚀 Fast (async) | 🐢 Slower (sync) | FastAPI for high-throughput |
| **Type Safety** | ✅ Pydantic models | ❌ Manual validation | FastAPI for complex inputs |
| **Auto Docs** | ✅ Built-in Swagger | ❌ Requires extensions | FastAPI for self-documenting APIs |
| **Learning Curve** | Moderate | Easy | Flask for simple prototypes |
| **Community** | Growing | Massive | Flask for legacy integration |

**For MLOps, we recommend FastAPI** because:
1. **Type validation** catches bad inputs before they hit your model
2. **Async support** handles concurrent predictions efficiently
3. **Auto-generated OpenAPI docs** = instant testing UI

### 2. Anatomy of a Production ML API

Every production ML API needs these endpoints:

```
┌─────────────────────────────────────────┐
│          ML Model API                   │
├─────────────────────────────────────────┤
│ GET  /health          → 200 OK          │  ← Load balancer checks
│ GET  /ready           → 200 OK/503      │  ← Model loaded?
│ GET  /metadata        → Model info      │  ← Version, metrics
│ POST /predict         → Predictions     │  ← Main inference
│ POST /predict/batch   → Bulk preds      │  ← Optional batch
└─────────────────────────────────────────┘
```

**Why each endpoint matters:**

1. **`/health`**: Kubernetes probes this to restart dead pods
2. **`/ready`**: Don't send traffic until model is loaded (can take 30s+)
3. **`/metadata`**: Debugging ("which model version is running?")
4. **`/predict`**: The money-maker (real-time inference)
5. **`/predict/batch`**: Cost-effective for bulk scoring

### 3. Request/Response Design Patterns

#### Pattern 1: Structured Input (Pydantic Models)

```python
from pydantic import BaseModel, Field, validator
from typing import List

class ChurnPredictionRequest(BaseModel):
    """Input schema for churn prediction"""
    customer_id: str = Field(..., example="CUST-12345")
    tenure_months: int = Field(..., ge=0, le=240, description="Months subscribed")
    monthly_charges: float = Field(..., ge=0, le=1000)
    total_charges: float = Field(..., ge=0)
    contract_type: str = Field(..., regex="^(Month-to-month|One year|Two year)$")
    
    @validator('total_charges')
    def total_must_be_reasonable(cls, v, values):
        """Sanity check: total ≈ monthly × tenure"""
        if 'monthly_charges' in values and 'tenure_months' in values:
            expected = values['monthly_charges'] * values['tenure_months']
            if abs(v - expected) > expected * 0.5:  # 50% tolerance
                raise ValueError(f'total_charges ({v}) inconsistent with monthly*tenure')
        return v

class ChurnPredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float = Field(..., ge=0.0, le=1.0)
    risk_category: str  # "Low", "Medium", "High"
    model_version: str
    prediction_timestamp: str
```

**Why this matters:**
- Pydantic auto-validates inputs (tenure can't be negative)
- Custom validators catch business logic errors
- Auto-generated JSON schema for documentation
- Type hints = fewer production bugs

#### Pattern 2: Error Handling Hierarchy

```python
from fastapi import HTTPException, status

# Custom exceptions
class ModelNotLoadedError(Exception):
    pass

class InvalidInputError(Exception):
    pass

# Error handlers
@app.exception_handler(ModelNotLoadedError)
async def model_not_loaded_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"error": "model_not_ready", "detail": str(exc)}
    )

@app.exception_handler(ValueError)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "invalid_input", "detail": str(exc)}
    )
```

**HTTP Status Code Guide for ML APIs:**
- `200 OK`: Successful prediction
- `422 Unprocessable Entity`: Bad input (wrong schema/values)
- `429 Too Many Requests`: Rate limit exceeded
- `503 Service Unavailable`: Model not loaded/crashed
- `500 Internal Server Error`: Unexpected bugs (catch-all)

### 4. Practical FastAPI Implementation

#### Minimal FastAPI ML Server

```python
# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Churn Prediction API",
    description="Predict customer churn probability",
    version="1.0.0"
)

# Global model holder
class ModelService:
    model = None
    model_version = None
    
    @classmethod
    def load_model(cls):
        """Load model at startup"""
        try:
            cls.model = joblib.load("models/churn_model.pkl")
            cls.model_version = "v1.2.3"  # Load from metadata
            logger.info(f"Model {cls.model_version} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

@app.on_event("startup")
async def startup_event():
    """Initialize model when server starts"""
    ModelService.load_model()

# Schemas
class PredictionRequest(BaseModel):
    tenure_months: int
    monthly_charges: float
    total_charges: float
    contract_type: str

class PredictionResponse(BaseModel):
    churn_probability: float
    risk_category: str
    model_version: str

# Endpoints
@app.get("/health")
async def health_check():
    """Liveness probe - is the service running?"""
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check():
    """Readiness probe - can we serve predictions?"""
    if ModelService.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ready", "model_version": ModelService.model_version}

@app.get("/metadata")
async def get_metadata():
    """Model information"""
    return {
        "model_version": ModelService.model_version,
        "model_type": "RandomForestClassifier",
        "features": ["tenure_months", "monthly_charges", "total_charges", "contract_type"],
        "training_date": "2024-01-15",
        "accuracy": 0.87
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a single prediction"""
    if ModelService.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Prepare features (same order as training)
        features = np.array([[
            request.tenure_months,
            request.monthly_charges,
            request.total_charges,
            1 if request.contract_type == "Month-to-month" else 0
        ]])
        
        # Predict
        proba = ModelService.model.predict_proba(features)[0][1]
        
        # Categorize risk
        if proba < 0.3:
            risk = "Low"
        elif proba < 0.7:
            risk = "Medium"
        else:
            risk = "High"
        
        logger.info(f"Prediction: {proba:.3f} (risk: {risk})")
        
        return PredictionResponse(
            churn_probability=round(proba, 3),
            risk_category=risk,
            model_version=ModelService.model_version
        )
    
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch")
async def predict_batch(requests: List[PredictionRequest]):
    """Batch predictions (more efficient)"""
    if ModelService.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for req in requests:
        # Reuse single prediction logic
        result = await predict(req)
        results.append(result)
    
    return {"predictions": results, "count": len(results)}
```

#### Running the API

```bash
# Install dependencies
pip install fastapi uvicorn joblib scikit-learn

# Run locally (dev mode with auto-reload)
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Production mode (multiple workers)
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

**Access auto-generated docs:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 5. Flask Alternative (If You Prefer It)

```python
# api_flask.py
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model at startup
model = joblib.load("models/churn_model.pkl")
MODEL_VERSION = "v1.2.3"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Validate input
        required = ['tenure_months', 'monthly_charges', 'total_charges', 'contract_type']
        if not all(k in data for k in required):
            return jsonify({"error": "missing_fields", "required": required}), 422
        
        # Prepare features
        features = np.array([[
            data['tenure_months'],
            data['monthly_charges'],
            data['total_charges'],
            1 if data['contract_type'] == "Month-to-month" else 0
        ]])
        
        # Predict
        proba = model.predict_proba(features)[0][1]
        
        return jsonify({
            "churn_probability": round(proba, 3),
            "risk_category": "High" if proba > 0.7 else "Medium" if proba > 0.3 else "Low",
            "model_version": MODEL_VERSION
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**Flask Pros:**
- Simpler for quick prototypes
- Larger ecosystem of extensions
- More tutorials/Stack Overflow answers

**Flask Cons:**
- No built-in input validation (manual work)
- Slower for high-concurrency workloads
- No auto-generated API docs

---

## Diagrams

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Application                     │
│                  (Web App / Mobile / Batch Job)             │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP POST /predict
                             │ {"tenure_months": 12, ...}
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Server                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. Request Validation (Pydantic)                    │   │
│  │     ✓ Schema check                                   │   │
│  │     ✓ Type coercion                                  │   │
│  │     ✓ Custom validators                              │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │  2. Feature Preprocessing                            │   │
│  │     • Encode categorical                             │   │
│  │     • Scale numeric                                  │   │
│  │     • Handle missing                                 │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │  3. Model Inference                                  │   │
│  │     model.predict_proba(features)                    │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │  4. Response Formatting                              │   │
│  │     • Round probability                              │   │
│  │     • Add metadata                                   │   │
│  │     • Log prediction                                 │   │
│  └────────────────────┬─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼ HTTP 200 OK
        {"churn_probability": 0.734, "risk_category": "High"}
```

---

## Lab / Demo

### Prerequisites

- Completed Lecture 7.2 (clean inference function)
- Python 3.8+
- `pip install fastapi uvicorn pydantic joblib scikit-learn`

### Step-by-Step Instructions

#### Step 1: Create Project Structure

```bash
mkdir ml-api
cd ml-api

# Create files
touch api.py
touch test_api.py
mkdir models

# Add a dummy model (replace with real one later)
python -c "
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

# Train dummy model
X = np.random.rand(100, 4)
y = np.random.randint(0, 2, 100)
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)

# Save
joblib.dump(model, 'models/churn_model.pkl')
print('✓ Dummy model created')
"
```

#### Step 2: Implement FastAPI Server

Copy the `api.py` implementation from Section 4 above.

#### Step 3: Start the Server

```bash
# Terminal 1: Start server
uvicorn api:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
```

#### Step 4: Test with cURL

```bash
# Terminal 2: Test endpoints

# 1. Health check
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# 2. Readiness check
curl http://localhost:8000/ready
# Expected: {"status":"ready","model_version":"v1.2.3"}

# 3. Get metadata
curl http://localhost:8000/metadata
# Expected: Model info JSON

# 4. Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure_months": 12,
    "monthly_charges": 65.50,
    "total_charges": 786.00,
    "contract_type": "Month-to-month"
  }'

# Expected:
# {
#   "churn_probability": 0.734,
#   "risk_category": "High",
#   "model_version": "v1.2.3"
# }
```

#### Step 5: Explore Interactive Docs

1. Open browser: `http://localhost:8000/docs`
2. Click "Try it out" on `/predict`
3. Fill in example values
4. Click "Execute"
5. See response + status code

**Pro Tip**: Share this URL with frontend devs—they can test without bothering you!

#### Step 6: Test Error Handling

```bash
# Test with missing field
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"tenure_months": 12}'

# Expected: HTTP 422 Unprocessable Entity
# {
#   "detail": [
#     {
#       "loc": ["body", "monthly_charges"],
#       "msg": "field required",
#       "type": "value_error.missing"
#     }
#   ]
# }

# Test with invalid value
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure_months": -5,
    "monthly_charges": 65.50,
    "total_charges": 786.00,
    "contract_type": "Month-to-month"
  }'

# Expected: Validation error about negative tenure
```

#### Step 7: Load Test (Optional)

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Send 1000 requests with 10 concurrent connections
ab -n 1000 -c 10 -T 'application/json' \
   -p test_payload.json \
   http://localhost:8000/predict

# Sample output:
# Requests per second:    245.23 [#/sec]
# Time per request:       40.776 [ms] (mean)
```

---

## Common Pitfalls

### ❌ Pitfall 1: Forgetting to Load the Model

```python
# BAD: Model never loaded
model = None  # Oops!

@app.post("/predict")
def predict(data):
    return model.predict(data)  # AttributeError!
```

**Fix:** Use startup events:
```python
@app.on_event("startup")
async def load_model():
    global model
    model = joblib.load("model.pkl")
```

### ❌ Pitfall 2: No Input Validation

```python
# BAD: Trusting client input
@app.post("/predict")
def predict(data: dict):
    age = data['age']  # KeyError if missing!
    return model.predict([[age, ...]])
```

**Fix:** Use Pydantic models (FastAPI auto-validates)

### ❌ Pitfall 3: Synchronous Blocking Operations

```python
# BAD: Blocks entire server
@app.post("/predict")
def predict(data):
    time.sleep(5)  # Simulate slow model
    return {"result": 42}
```

**Fix:** Use async if doing I/O:
```python
@app.post("/predict")
async def predict(data):
    result = await slow_model_call(data)
    return {"result": result}
```

### ❌ Pitfall 4: Not Logging Predictions

**Why it matters:** Can't debug production issues without logs.

```python
# GOOD: Log every prediction
logger.info(f"Prediction request: {data.dict()}")
result = model.predict(features)
logger.info(f"Prediction result: {result}, latency: {latency_ms}ms")
```

---

## Quiz

**Question 1**: Why use FastAPI over Flask for ML APIs?

a) FastAPI has better marketing  
b) FastAPI provides auto input validation and async support  
c) Flask is deprecated  
d) FastAPI is easier to learn  

<details>
<summary>Answer</summary>

**b) FastAPI provides auto input validation and async support**

FastAPI's Pydantic integration catches bad inputs before they reach your model, and async support handles concurrent requests efficiently—critical for high-throughput ML services.
</details>

---

**Question 2**: What HTTP status code should `/ready` return if the model isn't loaded?

a) 200 OK  
b) 404 Not Found  
c) 503 Service Unavailable  
d) 500 Internal Server Error  

<details>
<summary>Answer</summary>

**c) 503 Service Unavailable**

503 tells load balancers "don't send traffic here yet"—the service exists but can't handle requests. 500 implies a bug, 404 implies the endpoint doesn't exist.
</details>

---

**Question 3**: What's the purpose of the `/metadata` endpoint?

a) Store model metadata in database  
b) Provide debugging info (version, metrics) to clients  
c) Download the model file  
d) Update model configuration  

<details>
<summary>Answer</summary>

**b) Provide debugging info (version, metrics) to clients**

When a prediction looks wrong, the first question is "which model version served it?" `/metadata` answers that.
</details>

---

## Exercises

### Exercise 1: Add Authentication

**Task:** Modify the API to require an API key in headers.

**Hints:**
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "secret-key-12345"
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.post("/predict")
async def predict(data: PredictionRequest, api_key: str = Security(verify_api_key)):
    # ... prediction logic
```

**Test:**
```bash
# Should fail
curl -X POST http://localhost:8000/predict -d '{...}'

# Should succeed
curl -X POST http://localhost:8000/predict \
  -H "X-API-Key: secret-key-12345" \
  -d '{...}'
```

### Exercise 2: Add Metrics Endpoint

**Task:** Add `/metrics` endpoint that returns:
- Total predictions served
- Average prediction latency
- Error count

**Hints:**
- Use a global dict to track counters
- Time each prediction with `time.time()`
- Prometheus format (bonus): `prediction_total 1234`

### Exercise 3: Batch Prediction Optimization

**Task:** Current `/predict/batch` calls `/predict` in a loop. Optimize it to process all requests in one model call.

**Hints:**
- Stack features into numpy array
- Call `model.predict_proba()` once
- Measure speedup (should be 5-10x faster)

---

## Key Takeaways

✅ **REST APIs make models accessible** to any client (web, mobile, batch jobs)  
✅ **FastAPI is recommended** for ML APIs (validation, async, auto-docs)  
✅ **Every API needs `/health`, `/ready`, `/metadata`** for operations  
✅ **Use Pydantic models** for bulletproof input validation  
✅ **Log everything** (requests, responses, latencies) for debugging  
✅ **Auto-generated docs** at `/docs` save time for everyone  

---

## Next Lecture

In **Lecture 7.4**, we'll learn about **Docker** so we can package this API into a portable container that runs anywhere (local, AWS, GCP, Azure).

**Preview**: By the end of Section 7, you'll have a Dockerized FastAPI server serving your churn model—ready to deploy!
