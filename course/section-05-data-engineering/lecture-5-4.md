# Lecture 5.4 – Feature Engineering Overview (Not Deep ML, Just Enough to Operate)

## In This Lecture You Will Learn

- [x] Understand feature engineering for ML systems (MLOps perspective, not deep ML theory)
- [x] Identify where feature engineering fits in the MLOps workflow
- [x] Document and version features for reuse and consistency

---

## Real-World Context

> **Story**: Two teams built the same "customer engagement" feature independently. Team A calculated it as `logins_per_month`. Team B calculated it as `total_session_minutes / 30`. Both called it "engagement"—but they were different! When they tried to share a model, it failed because features with the same name meant different things. The fix: a feature catalog with precise definitions, calculation code, and ownership. Feature engineering isn't just math—it's software engineering with documentation and governance.

In the real world, features are reusable assets, not one-off calculations. Good feature engineering is about maintainability, consistency, and collaboration—not just predictive power.

---

## Main Content

### 1. What Is Feature Engineering?

**Definition**: Transforming raw data into inputs the model can learn from.

**Example**:
- **Raw Data**: `last_login_date = "2024-01-15"`
- **Feature**: `days_since_login = 7` (calculated on 2024-01-22)

Why? Models learn better from numeric features that capture relationships. "7 days" is more meaningful than a date string.

### 2. Common Feature Types

**Numeric Features**
- Direct use: age, price, count
- Normalizations: (value - mean) / std_dev
- Log transforms: log(revenue + 1) for skewed distributions

**Categorical Features**
- One-hot encoding: country → {is_US, is_UK, is_CA}
- Label encoding: plan_type → {0, 1, 2}
- Target encoding: encode by average target value

**Temporal Features**
- Time since event: `days_since_signup`, `hours_since_last_purchase`
- Cyclical: `hour_of_day`, `day_of_week`, `is_weekend`
- Trends: `purchases_last_7_days vs purchases_last_30_days`

**Aggregations**
- Sum: `total_purchases_last_30_days`
- Average: `avg_session_duration`
- Count: `num_support_tickets_last_quarter`
- Min/Max: `max_transaction_amount`

**Ratios & Derived**
- `support_tickets_per_month = tickets / months_active`
- `charges_per_tenure = monthly_charges / tenure_months`
- `is_high_value = (monthly_charges > 100)`

**Example for Churn Model**:
```python
# Feature engineering for churn prediction
def engineer_churn_features(df):
    # Temporal
    df['days_since_signup'] = (pd.Timestamp.now() - df['signup_date']).dt.days
    df['is_new_customer'] = df['days_since_signup'] < 90
    
    # Aggregations
    df['avg_monthly_usage'] = df['total_usage'] / df['tenure_months']
    
    # Ratios
    df['support_ticket_rate'] = df['num_tickets'] / df['tenure_months']
    df['charge_to_usage_ratio'] = df['monthly_charges'] / (df['total_usage'] + 1)
    
    # Derived
    df['is_high_spender'] = df['monthly_charges'] > df['monthly_charges'].quantile(0.75)
    
    return df
```

### 3. Feature Engineering in the MLOps Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│              Feature Engineering Workflow                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Raw Data → [Feature Engineering Code] → Features           │
│                                                              │
│  Training Path:                                             │
│  Historical Data → Transform → Feature Store → Model        │
│                                                              │
│  Serving Path:                                              │
│  Live Data → SAME Transform → Features → Prediction         │
│                                                              │
│  ⚠️  Key Challenge: Training/Serving Skew                   │
│  Different code = Different features = Model breaks         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Training/Serving Skew**: The #1 feature engineering bug
- Training uses Python pandas script
- Serving uses different language/library
- Subtle differences break models
- **Solution**: Reuse exact same transformation code

### 4. Best Practices for Feature Engineering in MLOps

**1. Document Everything**
```yaml
# feature_catalog.yaml
days_since_signup:
  description: "Number of days between signup date and current date"
  type: integer
  calculation: "(current_date - signup_date).days"
  owner: "ml-team@company.com"
  version: "1.0"
  dependencies: ["signup_date"]
```

**2. Version Features**
- When logic changes, create new version: `engagement_v2`
- Keep old version running until all models migrate
- Track which model uses which feature version

**3. Reuse, Don't Duplicate**
- Multiple models need "customer lifetime value"?
- Calculate once, store in feature store, reuse everywhere
- Saves computation, ensures consistency

**4. Test Transformations**
```python
def test_days_since_signup():
    # Unit test for feature transformation
    df = pd.DataFrame({'signup_date': ['2024-01-01']})
    result = engineer_features(df)
    assert result['days_since_signup'].iloc[0] > 0
    assert result['days_since_signup'].iloc[0] < 365
```

**5. Monitor Drift**
- Feature distributions change over time
- If `avg_session_duration` was 45 min, now it's 10 min
- Model trained on old distribution performs poorly

---

## Diagrams

```
┌───────────────────────────────────────────────────────────────┐
│          Training vs Serving: Feature Consistency             │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  TRAINING (Offline)                 SERVING (Online)          │
│                                                                │
│  Historical Data                    Live Request              │
│       ↓                                  ↓                    │
│  feature_eng.py                     feature_eng.py            │
│  (Python/Pandas)                    (SAME CODE!)              │
│       ↓                                  ↓                    │
│  days_since_signup=365              days_since_signup=7       │
│  avg_usage=50                       avg_usage=45              │
│       ↓                                  ↓                    │
│  Model Training                     Model Prediction          │
│                                                                │
│  ✅ Using identical transformation code prevents skew         │
│  ❌ Different code paths = subtle bugs = broken models        │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-5-4-diagram.png)

> Diagram emphasizes that training and serving must use identical feature engineering code

---

## Lab / Demo

### Prerequisites

- Completed Lectures 5.1-5.3
- Python with pandas, sklearn

### Step-by-Step Instructions

```bash
# Step 1: Review feature engineering code
cd project/src/features
cat feature_engineering.py

# Step 2: Run feature engineering on sample data
python feature_engineering.py --input ../../data/raw/customers.csv \
                               --output ../../data/features/customers_features.parquet

# Step 3: Inspect generated features
python -c "import pandas as pd; df = pd.read_parquet('../../data/features/customers_features.parquet'); print(df.head()); print(df.describe())"

# Step 4: Run unit tests for feature transformations
pytest tests/test_features.py -v
```

### Expected Output

```
Feature Engineering Complete
----------------------------
Input: 10,000 rows, 8 columns
Output: 10,000 rows, 25 columns (17 new features)

New Features Created:
- days_since_signup (temporal)
- tenure_in_years (derived)
- avg_monthly_charges (aggregation)
- support_ticket_rate (ratio)
- is_high_value_customer (boolean)
- contract_type_onehot_* (categorical encoding)
...

Tests: 15 passed, 0 failed
```

### Explanation

1. **Step 1**: Review the centralized feature engineering code
2. **Step 2**: Transform raw data into ML-ready features
3. **Step 3**: Inspect feature distributions and statistics
4. **Step 4**: Ensure transformations work correctly via tests

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Training/serving skew. Using different code for training vs serving leads to subtle bugs. Solution: Package feature code as a library used by both.

- ⚠️ **Pitfall 2**: Data leakage. Using future information in features (e.g., using next month's data to predict this month). Always respect temporal order.

- ⚠️ **Pitfall 3**: Not documenting features. Six months later, no one remembers what "feat_17" means. Document name, calculation, and purpose.

---

## Homework / Practice

1. **Exercise 1**: For our churn model, design 5 features from customer demographics, usage, and billing data. For each, specify: name, type (numeric/categorical/temporal), and calculation.

2. **Exercise 2**: Explain training/serving skew to someone non-technical. Give an example of how different feature code in training vs serving breaks models.

3. **Stretch Goal**: Take a CSV dataset and write a Python function that engineers 3 features from it. Write unit tests for your function.

---

## Quick Quiz

1. **What is feature engineering?**
   - A) Training the model
   - B) Transforming raw data into model inputs
   - C) Deploying the model
   - D) Monitoring the model

2. **What is training/serving skew?**
   - A) Model performs differently on training vs test data
   - B) Features calculated differently during training vs serving
   - C) Training takes longer than serving
   - D) Model drifts over time

3. **True or False: It's okay to calculate features differently in training and serving as long as they're "similar enough."**

<details>
<summary>Answers</summary>

1. **B** - Feature engineering transforms raw data into features the model can learn from
2. **B** - Training/serving skew occurs when features are calculated differently in the two environments
3. **False** - Features must be calculated identically in training and serving. Even small differences break models.

</details>

---

## Summary

- Feature engineering transforms raw data into model inputs
- Common types: numeric, categorical, temporal, aggregations, ratios, derived
- Must use identical code in training and serving to avoid skew
- Document features with name, definition, calculation code, and owner
- Version features when logic changes
- Store in feature store for reuse across models and teams
- Test feature transformations like any other code
- Monitor feature distributions for drift

---

## Next Steps

→ Continue to **Lecture 5.5**: Storing Data & Features for Re-use (Intro to Feature Stores)

---

## Additional Resources

- [Google: Feature Engineering Best Practices](https://developers.google.com/machine-learning/data-prep/transform/introduction)
- [Feast: Feature Store Documentation](https://docs.feast.dev/)
- [Feature Engineering Book (O'Reilly)](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/)
