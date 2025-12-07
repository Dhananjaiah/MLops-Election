# Lecture 7.2 – Writing a Clean Inference Function (predict())

## In This Lecture You Will Learn

- [x] Design clean, production-ready inference functions
- [x] Handle preprocessing, prediction, and postprocessing properly
- [x] Implement error handling and validation for predict()

---

## Real-World Context

> **Story**: A fintech startup deployed a fraud detection model. The training code was messy but worked. When integrating with their payment system, the engineering team discovered: the predict() function expected a DataFrame with 47 columns in a specific order, threw cryptic errors on missing values, and returned raw probabilities without any interpretation. After 3 weeks of debugging and 2 production incidents, they rewrote it with proper input validation, clear error messages, and documented output format. The lesson: Your predict() function is your model's public interface—make it bulletproof.

In the real world, your predict() function will be called millions of times by code you don't control. Design it for maximum clarity and robustness.

---

## Main Content

### 1. Anatomy of a Production Predict Function

**The Three Phases**:
```python
def predict(input_data):
    # Phase 1: Preprocess (raw input → model-ready)
    processed = preprocess(input_data)
    
    # Phase 2: Predict (model inference)
    raw_output = model.predict(processed)
    
    # Phase 3: Postprocess (model output → business output)
    result = postprocess(raw_output)
    
    return result
```

**Why Separate These?**
- **Testability**: Each phase can be unit tested independently
- **Debuggability**: Know exactly where failures occur
- **Reusability**: Preprocessing might be used elsewhere
- **Clarity**: Each function has one job

### 2. Input Validation & Preprocessing

**Bad Example** (Training notebook style):
```python
def predict(data):
    # Assumes data is already perfect
    X = data[['age', 'tenure', 'charges']]
    return model.predict(X)
```
**Problems**: No validation, assumes structure, crashes on bad input

**Good Example** (Production style):
```python
from typing import Dict, List, Union
import pandas as pd
from pydantic import BaseModel, Field, validator

class ChurnPredictionInput(BaseModel):
    """Validated input for churn prediction."""
    age: int = Field(..., ge=18, le=120, description="Customer age")
    tenure: int = Field(..., ge=0, description="Months as customer")
    monthly_charges: float = Field(..., gt=0, description="Monthly bill")
    
    @validator('age')
    def age_reasonable(cls, v):
        if v < 18 or v > 100:
            raise ValueError(f"Age {v} outside typical range")
        return v

def preprocess(input_data: Union[Dict, ChurnPredictionInput]) -> pd.DataFrame:
    """
    Convert raw input to model-ready format.
    
    Args:
        input_data: Dict or validated Pydantic model
        
    Returns:
        DataFrame ready for model.predict()
        
    Raises:
        ValueError: If input data is invalid
    """
    # Validate using Pydantic
    if isinstance(input_data, dict):
        input_data = ChurnPredictionInput(**input_data)
    
    # Convert to DataFrame with exact columns model expects
    df = pd.DataFrame([{
        'age': input_data.age,
        'tenure': input_data.tenure,
        'charges': input_data.monthly_charges
    }])
    
    # Apply same transformations as training
    # (e.g., scaling, encoding - loaded from training artifacts)
    df_scaled = scaler.transform(df)
    
    return df_scaled

def predict(input_data):
    """Main prediction function."""
    try:
        # Phase 1: Validate and preprocess
        X = preprocess(input_data)
        
        # Phase 2: Get prediction
        proba = model.predict_proba(X)[0]
        
        # Phase 3: Postprocess
        result = postprocess(proba)
        
        return result
        
    except ValueError as e:
        return {"error": "Invalid input", "details": str(e)}
    except Exception as e:
        return {"error": "Prediction failed", "details": str(e)}
```

### 3. Model Loading & Caching

**Problem**: Loading model on every prediction is slow
**Solution**: Load once, predict many

```python
import joblib
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_model():
    """
    Load model once and cache.
    Returns same instance on subsequent calls.
    """
    model_path = Path(__file__).parent / "artifacts" / "model.pkl"
    return joblib.load(model_path)

@lru_cache(maxsize=1)
def load_scaler():
    """Load preprocessing scaler."""
    scaler_path = Path(__file__).parent / "artifacts" / "scaler.pkl"
    return joblib.load(scaler_path)

# Global singletons (loaded on module import)
MODEL = load_model()
SCALER = load_scaler()

def predict(input_data):
    """Predict using cached model."""
    X = preprocess(input_data, SCALER)
    return MODEL.predict_proba(X)
```

### 4. Output Format & Postprocessing

**Bad**: Return raw numpy arrays
```python
return model.predict_proba(X)  # array([[0.73, 0.27]])
```

**Good**: Return structured, documented format
```python
def postprocess(probabilities):
    """
    Convert model output to business-friendly format.
    
    Args:
        probabilities: Model's predict_proba output
        
    Returns:
        Dict with prediction, confidence, and metadata
    """
    churn_proba = float(probabilities[1])  # Convert numpy to Python float
    
    return {
        "prediction": "churn" if churn_proba >= 0.5 else "no_churn",
        "churn_probability": round(churn_proba, 3),
        "confidence": "high" if abs(churn_proba - 0.5) > 0.3 else "low",
        "model_version": "1.2.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# Example output:
{
    "prediction": "churn",
    "churn_probability": 0.734,
    "confidence": "high",
    "model_version": "1.2.0",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### 5. Complete Production Example

```python
"""
churn_predictor/inference.py - Production-ready inference module
"""
import logging
from typing import Dict, Union
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Models loaded once on module import
MODEL_PATH = Path(__file__).parent / "artifacts" / "model.pkl"
SCALER_PATH = Path(__file__).parent / "artifacts" / "scaler.pkl"

MODEL = joblib.load(MODEL_PATH)
SCALER = joblib.load(SCALER_PATH)
MODEL_VERSION = "1.2.0"

class PredictionInput(BaseModel):
    """Input schema for predictions."""
    customer_id: str = Field(..., description="Unique customer ID")
    age: int = Field(..., ge=18, le=100)
    tenure_months: int = Field(..., ge=0)
    monthly_charges: float = Field(..., gt=0)

def preprocess(data: Union[Dict, PredictionInput]) -> pd.DataFrame:
    """Validate and transform input."""
    if isinstance(data, dict):
        data = PredictionInput(**data)
    
    df = pd.DataFrame([{
        'age': data.age,
        'tenure': data.tenure_months,
        'charges': data.monthly_charges
    }])
    
    return pd.DataFrame(
        SCALER.transform(df),
        columns=['age', 'tenure', 'charges']
    )

def postprocess(proba, customer_id: str) -> Dict:
    """Format prediction output."""
    churn_proba = float(proba[0][1])
    
    return {
        "customer_id": customer_id,
        "prediction": "churn" if churn_proba >= 0.5 else "retain",
        "churn_probability": round(churn_proba, 3),
        "confidence": "high" if abs(churn_proba - 0.5) > 0.3 else "medium",
        "model_version": MODEL_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

def predict(input_data: Union[Dict, PredictionInput]) -> Dict:
    """
    Main prediction function.
    
    Args:
        input_data: Customer data as dict or PredictionInput
        
    Returns:
        Prediction results with metadata
        
    Example:
        >>> predict({"customer_id": "C123", "age": 45, 
        ...          "tenure_months": 24, "monthly_charges": 89.5})
        {
            "customer_id": "C123",
            "prediction": "churn",
            "churn_probability": 0.734,
            "confidence": "high",
            "model_version": "1.2.0",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    """
    try:
        # Extract customer_id before preprocessing
        if isinstance(input_data, dict):
            customer_id = input_data.get("customer_id", "unknown")
        else:
            customer_id = input_data.customer_id
            
        # Preprocess
        X = preprocess(input_data)
        
        # Predict
        proba = MODEL.predict_proba(X)
        
        # Postprocess
        result = postprocess(proba, customer_id)
        
        logger.info(f"Prediction for {customer_id}: {result['prediction']}")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"error": "Invalid input", "details": str(e)}
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        return {"error": "Prediction failed", "details": "Internal server error"}

# Batch prediction support
def predict_batch(inputs: List[Dict]) -> List[Dict]:
    """Predict for multiple customers efficiently."""
    return [predict(inp) for inp in inputs]
```

---

## Diagrams

```
┌────────────────────────────────────────────────────────────────────┐
│              Production Predict() Function Flow                     │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT                                                              │
│  ┌─────────────────────────────────────┐                          │
│  │ {"customer_id": "C123",              │                          │
│  │  "age": 45, "tenure_months": 24}    │                          │
│  └─────────────────────────────────────┘                          │
│             ↓                                                       │
│  PHASE 1: VALIDATION & PREPROCESSING                               │
│  ┌─────────────────────────────────────┐                          │
│  │ • Validate with Pydantic             │                          │
│  │ • Check ranges (age 18-100)          │                          │
│  │ • Transform to DataFrame             │                          │
│  │ • Apply scaler                       │                          │
│  └─────────────────────────────────────┘                          │
│             ↓                                                       │
│  PHASE 2: MODEL INFERENCE                                          │
│  ┌─────────────────────────────────────┐                          │
│  │ X_scaled → MODEL.predict_proba(X)    │                          │
│  │ Returns: [[0.27, 0.73]]              │                          │
│  └─────────────────────────────────────┘                          │
│             ↓                                                       │
│  PHASE 3: POSTPROCESSING                                           │
│  ┌─────────────────────────────────────┐                          │
│  │ • Extract churn probability          │                          │
│  │ • Classify (churn if >= 0.5)         │                          │
│  │ • Add metadata (version, timestamp)  │                          │
│  └─────────────────────────────────────┘                          │
│             ↓                                                       │
│  OUTPUT                                                             │
│  ┌─────────────────────────────────────┐                          │
│  │ {"customer_id": "C123",              │                          │
│  │  "prediction": "churn",              │                          │
│  │  "churn_probability": 0.73,          │                          │
│  │  "confidence": "high",               │                          │
│  │  "model_version": "1.2.0",           │                          │
│  │  "timestamp": "2024-01-15T10:30:00"} │                          │
│  └─────────────────────────────────────┘                          │
│                                                                     │
│  ERROR HANDLING: Try/except at each phase with clear error messages│
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-7-2-diagram.png)

> Diagram shows the three-phase predict() function with validation, inference, and postprocessing

---

## Lab / Demo

### Prerequisites

- Completed Lecture 7.1
- Python 3.8+, scikit-learn, pydantic

### Step-by-Step Instructions

```bash
# Step 1: Create project structure
mkdir -p churn_predictor/artifacts
cd churn_predictor

# Step 2: Create inference module
cat > inference.py << 'EOF'
import joblib
import pandas as pd
from pydantic import BaseModel, Field
from pathlib import Path

class PredictionInput(BaseModel):
    age: int = Field(..., ge=18, le=100)
    tenure: int = Field(..., ge=0)
    charges: float = Field(..., gt=0)

# Mock model for demo
class MockModel:
    def predict_proba(self, X):
        return [[0.3, 0.7]]  # Mock prediction

MODEL = MockModel()

def preprocess(data):
    validated = PredictionInput(**data)
    return pd.DataFrame([{
        'age': validated.age,
        'tenure': validated.tenure,
        'charges': validated.charges
    }])

def predict(input_data):
    X = preprocess(input_data)
    proba = MODEL.predict_proba(X)
    
    return {
        "prediction": "churn" if proba[0][1] >= 0.5 else "retain",
        "churn_probability": round(proba[0][1], 3),
        "confidence": "high"
    }
EOF

# Step 3: Test the predict function
python3 << 'EOF'
from inference import predict

# Valid input
result = predict({
    "age": 45,
    "tenure": 24,
    "charges": 89.5
})
print("Valid input:", result)

# Invalid input (age too low)
try:
    result = predict({"age": 10, "tenure": 5, "charges": 50})
except Exception as e:
    print("Caught validation error:", e)
EOF

# Step 4: Test batch predictions
python3 << 'EOF'
from inference import predict

customers = [
    {"age": 45, "tenure": 24, "charges": 89.5},
    {"age": 30, "tenure": 60, "charges": 45.0},
    {"age": 65, "tenure": 12, "charges": 120.0}
]

for i, customer in enumerate(customers, 1):
    result = predict(customer)
    print(f"Customer {i}: {result['prediction']} ({result['churn_probability']})")
EOF
```

### Expected Output

```
Step 3 Output:
Valid input: {'prediction': 'churn', 'churn_probability': 0.7, 'confidence': 'high'}
Caught validation error: 1 validation error for PredictionInput
age
  ensure this value is greater than or equal to 18 (type=value_error.number.not_ge; limit_value=18)

Step 4 Output:
Customer 1: churn (0.7)
Customer 2: churn (0.7)
Customer 3: churn (0.7)
```

### Explanation

1. **Step 1**: Set up project structure for inference code
2. **Step 2**: Create production-ready predict() with validation
3. **Step 3**: Test with valid and invalid inputs (Pydantic catches errors)
4. **Step 4**: Demonstrate batch prediction capability

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Returning numpy arrays instead of Python types. APIs can't JSON-serialize numpy.float64. Always convert: `float(proba)`.

- ⚠️ **Pitfall 2**: No input validation. Production data is messy. Validate everything with Pydantic or similar.

- ⚠️ **Pitfall 3**: Loading model on every prediction. Load once at module/class initialization, reuse for all predictions.

---

## Homework / Practice

1. **Exercise 1**: Add logging to the predict function. Log every prediction with customer_id, input, and result.

2. **Exercise 2**: Implement a `predict_batch()` function that efficiently handles 1000 predictions at once.

3. **Stretch Goal**: Add caching with `functools.lru_cache` for predictions on the same input (useful for APIs with repeated requests).

---

## Quick Quiz

1. **What are the three phases of a production predict() function?**
   - A) Load, Process, Save
   - B) Preprocess, Predict, Postprocess
   - C) Input, Output, Error
   - D) Training, Validation, Testing

2. **Why use Pydantic for input validation?**
   - A) It makes code faster
   - B) It catches invalid inputs before they reach the model
   - C) It's required by FastAPI
   - D) It improves model accuracy

3. **True or False: It's okay to load the model from disk on every prediction.**

<details>
<summary>Answers</summary>

1. **B** - Preprocess (validate/transform), Predict (model inference), Postprocess (format output)
2. **B** - Pydantic validates types and ranges, catching bad data before it crashes your model
3. **False** - Loading from disk is slow. Load once and cache the model in memory.

</details>

---

## Summary

- Production predict() has three phases: preprocess, predict, postprocess
- Use Pydantic for input validation (types, ranges, required fields)
- Load models once and cache (global variable or singleton pattern)
- Return structured outputs (dicts with metadata, not raw arrays)
- Handle errors gracefully with try/except and clear error messages
- Document your predict() function's input/output format
- Test with edge cases: missing fields, out-of-range values, nulls

---

## Next Steps

→ Continue to **Lecture 7.3**: Building a REST API with FastAPI / Flask for the Model

---

## Additional Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [scikit-learn: Model Persistence](https://scikit-learn.org/stable/model_persistence.html)
- [Google ML Best Practices: Prediction](https://developers.google.com/machine-learning/guides/rules-of-ml)
