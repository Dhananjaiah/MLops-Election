# Lecture 5.3 – Data Quality & Validation (Basic Checks MLOps Must Enforce)

## In This Lecture You Will Learn

- [x] Implement data quality checks in ML pipelines
- [x] Detect common data issues before they break models
- [x] Set up automated validation and monitoring for data health

---

## Real-World Context

> **Story**: Maria's model accuracy dropped from 85% to 62% overnight. Panic. After hours of debugging, she found: a new "country" value "N/A" appeared in the data (someone's database export script broke). Her model, trained on {US, UK, CA}, didn't know how to handle "N/A" and predicted randomly. Cost: 1 day of bad predictions, angry stakeholders, emergency fix. Solution: data validation checks that would have caught this in staging before production. The lesson: garbage in, garbage out—and garbage detection is non-optional.

In the real world, data quality issues are the #1 cause of ML system failures. Models assume clean data; when that assumption breaks, everything breaks.

---

## Main Content

### 1. The Five Data Quality Dimensions

1. **Completeness**: Are there missing values? NULL fields?
2. **Accuracy**: Is the data correct? Matches reality?
3. **Consistency**: Do related fields agree? (e.g., age=5, job="CEO"?)
4. **Timeliness**: Is the data fresh enough for our use case?
5. **Validity**: Do values match expected schema/ranges?

### 2. Common Data Issues in ML

**Schema Changes**
- Column renamed: `last_login` → `last_activity_date`
- Type changed: `age` from int to string
- New column added unexpectedly
- Column removed that model depends on

**Missing Values**
- True NULLs in database
- Empty strings ""
- Sentinel values (-999, "N/A", "Unknown")
- Entire rows missing (data pipeline failed)

**Outliers & Invalid Values**
- Age = 250 years
- Price = -$100
- Future dates in historical data
- Latitude = 500 (valid range: -90 to 90)

**Distribution Shift**
- Training: 50/50 churn ratio
- Production: 95/5 ratio (model breaks)
- New categories appear
- Value distributions change

**Staleness**
- Expected: daily updates
- Reality: last update was 7 days ago
- Pipeline silently failed, no alerts

### 3. Building a Validation Framework

```python
# Example: Data validation for churn model
from great_expectations import DataContext
import pandas as pd
from datetime import datetime, timedelta

def validate_churn_data(df: pd.DataFrame) -> dict:
    """
    Validate churn training data against expected schema and ranges.
    Returns dict with validation results.
    """
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    # 1. Completeness checks
    required_columns = ['customer_id', 'monthly_charges', 'tenure_months']
    for col in required_columns:
        if col not in df.columns:
            results["failed"].append(f"Missing required column: {col}")
        elif df[col].isna().any():
            pct = df[col].isna().mean() * 100
            if pct > 5:
                results["failed"].append(f"{col} has {pct:.1f}% missing values")
            else:
                results["warnings"].append(f"{col} has {pct:.1f}% missing values")
    
    # 2. Validity checks (ranges)
    if 'age' in df.columns:
        invalid_age = (~df['age'].between(18, 120)).sum()
        if invalid_age > 0:
            results["failed"].append(f"{invalid_age} customers have invalid age")
    
    if 'monthly_charges' in df.columns:
        invalid_charges = (df['monthly_charges'] <= 0).sum()
        if invalid_charges > 0:
            results["failed"].append(f"{invalid_charges} customers have invalid charges")
    
    # 3. Consistency checks
    if 'tenure_months' in df.columns and 'contract_type' in df.columns:
        # Two-year contract but only 2 months tenure?
        inconsistent = df[(df['contract_type'] == 'Two Year') & 
                         (df['tenure_months'] < 24)]
        if len(inconsistent) > 100:
            results["warnings"].append(f"{len(inconsistent)} customers on 2-year contract with <24 months tenure")
    
    # 4. Timeliness checks
    if 'last_updated' in df.columns:
        max_date = pd.to_datetime(df['last_updated']).max()
        days_old = (datetime.now() - max_date).days
        if days_old > 2:
            results["failed"].append(f"Data is {days_old} days old (expected <2)")
    
    # 5. Distribution checks
    if 'churned' in df.columns:
        churn_rate = df['churned'].mean()
        if churn_rate < 0.01 or churn_rate > 0.20:
            results["warnings"].append(f"Unusual churn rate: {churn_rate:.1%} (expected 2-10%)")
    
    return results

# Usage in pipeline
validation_results = validate_churn_data(df)
if validation_results["failed"]:
    raise ValueError(f"Data validation failed: {validation_results['failed']}")
```

### 4. Tools for Data Quality

**Great Expectations** (Python Library)
- Declarative expectations: "expect_column_values_to_be_between"
- Auto-generate documentation
- Integrates with Airflow, dbt

**dbt Tests** (SQL-based)
- Built into dbt (data build tool)
- Test data transformations
- Version-controlled with code

**Custom Validators**
- Python functions in your pipeline
- Full control, easy to understand
- Good for simple checks

---

## Diagrams

```
┌──────────────────────────────────────────────────────────────────┐
│              Data Quality Validation Pipeline                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  📊 Raw Data                                                     │
│  ↓                                                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. SCHEMA VALIDATION                                        │ │
│  │    ✓ All expected columns present?                         │ │
│  │    ✓ Correct data types?                                   │ │
│  │    ✓ No unexpected columns?                                │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ↓ PASS                                     FAIL → ⚠️ ALERT    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 2. COMPLETENESS CHECK                                       │ │
│  │    ✓ Missing values < 5%?                                  │ │
│  │    ✓ Required fields populated?                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ↓ PASS                                     FAIL → ⚠️ ALERT    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 3. VALIDITY CHECK                                           │ │
│  │    ✓ Values in expected ranges?                            │ │
│  │    ✓ Valid enum values?                                    │ │
│  │    ✓ No outliers beyond threshold?                         │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ↓ PASS                                     FAIL → ⚠️ ALERT    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 4. CONSISTENCY CHECK                                        │ │
│  │    ✓ Related fields agree?                                 │ │
│  │    ✓ No logical contradictions?                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ↓ PASS                                     FAIL → ⚠️ ALERT    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 5. TIMELINESS & FRESHNESS                                   │ │
│  │    ✓ Data updated recently?                                │ │
│  │    ✓ Within SLA window?                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ↓ ALL PASSED                                                   │
│  ✅ Clean Data → Feature Engineering                            │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-5-3-diagram.png)

> Diagram shows validation gates that data must pass through before being used for ML

---

## Lab / Demo

### Prerequisites

- Completed Lectures 5.1-5.2
- Python with pandas, great_expectations installed

### Step-by-Step Instructions

```bash
# Step 1: Install Great Expectations
pip install great-expectations

# Step 2: Initialize Great Expectations in project
cd project
great_expectations init

# Step 3: Review sample validation suite
cat great_expectations/expectations/churn_data_suite.json

# Step 4: Run validation on sample data
great_expectations checkpoint run churn_checkpoint

# Step 5: View validation report
# Open: great_expectations/uncommitted/data_docs/local_site/index.html
```

### Expected Output

```
Validation Results for churn_data_suite
========================================

✅ PASSED: expect_column_to_exist(customer_id)
✅ PASSED: expect_column_values_to_not_be_null(customer_id) [0 unexpected]
✅ PASSED: expect_column_values_to_be_between(age, 18, 120) [0 unexpected]
✅ PASSED: expect_column_values_to_be_in_set(contract_type, 
           ['Month-to-Month', 'One Year', 'Two Year']) [0 unexpected]
⚠️  WARNING: expect_column_mean_to_be_between(monthly_charges, 50, 150)
           [Observed: 45.2, Expected: 50-150]
❌ FAILED: expect_table_row_count_to_be_between(min=10000, max=None)
          [Observed: 8,543 rows, Expected: ≥10,000]

Overall: 4 passed, 1 warning, 1 failed
```

### Explanation

1. **Step 1**: Install the industry-standard data validation library
2. **Step 2**: Set up Great Expectations project structure
3. **Step 3**: See how expectations are defined (JSON/Python)
4. **Step 4**: Run validations and get pass/fail results
5. **Step 5**: Review auto-generated HTML documentation

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Validating only once at the start. Data quality degrades over time. Validate on every pipeline run, not just during development.

- ⚠️ **Pitfall 2**: Too strict validation = constant false alarms. Too loose = garbage gets through. Start loose, tighten based on observed failures.

- ⚠️ **Pitfall 3**: No alerts when validation fails. If a tree falls in the forest and no one hears it... Set up PagerDuty/Slack alerts for critical failures.

---

## Homework / Practice

1. **Exercise 1**: Write 5 validation rules for our churn dataset (customer_id, age, monthly_charges, contract_type, tenure_months). Include: completeness, validity, and consistency checks.

2. **Exercise 2**: A data validation fails: "expect_column_values_to_be_between(age, 18, 120)" shows 50 rows with age > 120. What are 3 possible root causes? How would you debug?

3. **Stretch Goal**: Install Great Expectations locally and create a validation suite for a CSV file you have. Run it and fix any issues found.

---

## Quick Quiz

1. **Which data quality dimension checks if values are in expected ranges?**
   - A) Completeness
   - B) Validity
   - C) Consistency
   - D) Timeliness

2. **What should you do when data validation fails in production?**
   - A) Ignore it and hope it goes away
   - B) Manually fix the data
   - C) Alert the team, block bad data from reaching the model
   - D) Retrain the model to handle bad data

3. **True or False: You only need to validate data during initial development, not in production.**

<details>
<summary>Answers</summary>

1. **B** - Validity checks ensure values are in expected ranges (e.g., age between 18-120)
2. **C** - Alert immediately and prevent bad data from corrupting model predictions
3. **False** - Production data quality degrades over time. Continuous validation is essential.

</details>

---

## Summary

- Data quality has 5 dimensions: completeness, accuracy, consistency, timeliness, validity
- Common issues: schema changes, missing values, outliers, distribution shift, staleness
- Validate at every pipeline run—fail fast, don't let bad data reach models
- Use tools like Great Expectations for declarative, reusable validations
- Monitor data quality metrics just like you monitor model metrics
- Set up alerts for validation failures—silent failures are the worst failures

---

## Next Steps

→ Continue to **Lecture 5.4**: Feature Engineering Overview (Not Deep ML, Just Enough to Operate)

---

## Additional Resources

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Google: Data Validation for ML](https://developers.google.com/machine-learning/data-prep/validation)
- [dbt: Testing Data Quality](https://docs.getdbt.com/docs/build/tests)
