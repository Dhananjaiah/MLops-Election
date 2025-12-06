# Lecture 4.2 – Business Requirements & Success Metrics (How Will We Know It Works?)

## In This Lecture You Will Learn

- [x] Define clear, measurable success criteria for ML projects
- [x] Balance business metrics with ML performance metrics
- [x] Set realistic expectations with stakeholders about what ML can and cannot do

---

## Real-World Context

> **Story**: Six months ago, DataCorp deployed a churn prediction model with "95% accuracy!" The team celebrated. But three months later, the CEO was furious: "We spent $500K on this model, and churn is still at 5%!" What went wrong? The model was technically accurate, but nobody defined *business* success. Did 95% accuracy translate to retained customers? How many false positives wasted marketing budget? Should they have optimized for precision instead of accuracy? The painful lesson: ML success ≠ business success unless you define both upfront.

In the real world, many ML projects fail not because of bad models, but because of misaligned expectations. Before writing a single line of code, everyone must agree on how to measure success.

---

## Main Content

### 1. The Three Levels of Success Metrics

**Level 1: Model Performance Metrics (ML Team)**
- Accuracy, Precision, Recall, F1, AUC-ROC
- These are technical measures of how well the model predicts
- Example: "Our model achieves 85% recall at 75% precision"

**Level 2: System Performance Metrics (MLOps Team)**
- API latency, uptime, throughput, error rates
- How well the system performs in production
- Example: "Model serves predictions in <100ms with 99.9% uptime"

**Level 3: Business Impact Metrics (Leadership)**
- Revenue saved, costs reduced, customer satisfaction
- The actual business outcome we care about
- Example: "Reduced churn from 5% to 4%, saving $24M annually"

**All three matter, but Level 3 is what executives care about.**

### 2. Defining Success for Our Churn Project

**Business Requirements** (from stakeholders):
1. **Primary Goal**: Reduce monthly churn rate from 5% to 4% (20% reduction)
2. **Secondary Goal**: Improve retention campaign ROI from 2:1 to 4:1
3. **Constraint**: Marketing budget for retention is fixed at $2M/month
4. **Timeline**: Show measurable impact within 6 months

**ML Performance Targets**:
- **Recall ≥ 80%**: Catch 80% of customers who will actually churn (don't miss them!)
- **Precision ≥ 60%**: Of customers we flag, 60% truly churn (don't waste budget on false alarms)
- **AUC-ROC ≥ 0.85**: Overall discrimination ability

**Why These Numbers?**
- High recall: Missing churners is expensive—we'd rather have false positives
- Moderate precision: Some false positives are acceptable if we save more true churners
- Trade-off: We can adjust the threshold to balance recall vs. precision

**System Requirements**:
- Predictions refreshed weekly (batch scoring)
- Model retraining monthly or when performance drops >5%
- API latency <500ms for real-time scoring
- 99.5% uptime for the prediction service

### 3. What Good Looks Like: Success Scenarios

**Scenario A: Wildly Successful** 🎉
- Churn drops from 5% to 3.5% (30% reduction)
- ROI on retention campaigns: 6:1
- Model maintains performance for 6+ months without retraining
- **Business Impact**: $36M saved annually

**Scenario B: Success** ✅
- Churn drops from 5% to 4% (20% reduction as planned)
- ROI on retention campaigns: 4:1
- Model requires quarterly retraining
- **Business Impact**: $24M saved annually

**Scenario C: Partial Success** ⚠️
- Churn drops from 5% to 4.5% (10% reduction)
- ROI on retention campaigns: 3:1
- Model needs frequent retraining
- **Business Impact**: $12M saved annually (still positive!)

**Scenario D: Failure** ❌
- Churn stays at 5% or increases
- ROI on retention campaigns <2:1 (worse than before)
- Model predictions are random/useless
- **Business Impact**: Wasted engineering time and budget

---

## Diagrams

```
┌────────────────────────────────────────────────────────────────────┐
│                 Success Metrics Hierarchy                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🎯 Business Metrics (What Executives See)                        │
│     ├─ Churn rate: 5% → 4%                                        │
│     ├─ Revenue saved: $24M/year                                   │
│     └─ Campaign ROI: 2:1 → 4:1                                    │
│                 ↑                                                   │
│                 │ drives                                            │
│                 │                                                   │
│  📊 System Metrics (What DevOps Monitors)                         │
│     ├─ Prediction latency: <500ms                                 │
│     ├─ API uptime: 99.5%                                          │
│     └─ Predictions/week: 100K                                     │
│                 ↑                                                   │
│                 │ depends on                                        │
│                 │                                                   │
│  🔬 Model Metrics (What Data Scientists Optimize)                 │
│     ├─ Recall: 80%                                                │
│     ├─ Precision: 60%                                             │
│     └─ AUC-ROC: 0.85                                              │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-4-2-diagram.png)

> Diagram illustrates the trade-off between Precision and Recall, showing how threshold selection impacts business outcomes

---

## Lab / Demo

### Prerequisites

- Completed Lecture 4.1
- Understanding of precision, recall, and confusion matrix

### Step-by-Step Instructions

```bash
# Step 1: Review the requirements document
cd project/docs
cat requirements.md

# Step 2: Look at the success metrics template
cat metrics_template.yaml

# Step 3: Calculate potential business impact
python scripts/calculate_impact.py --current_churn=0.05 --target_churn=0.04 --customers=2000000 --clv=1200
```

### Expected Output

```yaml
# Success Metrics for Churn Prediction Project

business_metrics:
  primary:
    - metric: monthly_churn_rate
      baseline: 5.0%
      target: 4.0%
      measurement: percentage of customers canceling per month
  
  financial:
    - metric: revenue_saved
      baseline: $0
      target: $24M/year
      calculation: (0.05 - 0.04) * 2M * $1200

model_metrics:
  - recall: ">= 0.80"
  - precision: ">= 0.60"
  - auc_roc: ">= 0.85"

system_metrics:
  - latency: "< 500ms (p95)"
  - uptime: ">= 99.5%"
  - refresh_frequency: "weekly"
```

### Explanation

1. **Step 1**: Review documented requirements from stakeholder interviews
2. **Step 2**: See the standard format for tracking success metrics
3. **Step 3**: Calculate the dollar impact of different churn reduction scenarios

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Optimizing only for accuracy. An "accurate" model that predicts everyone won't churn is useless (100% precision, 0% recall). Focus on the metric that matters for the business—usually recall for churn.

- ⚠️ **Pitfall 2**: Not connecting ML metrics to business metrics. Your CEO doesn't care about AUC-ROC. Translate: "85% recall means we'll save 80 out of every 100 at-risk customers, worth $96K."

- ⚠️ **Pitfall 3**: Setting unrealistic targets. If your baseline churn is 5%, promising to reduce it to 0.5% will lead to disappointment and project cancellation.

---

## Homework / Practice

1. **Exercise 1**: For our TeleConnect project (2M customers, 5% churn, $1200 CLV), calculate the annual revenue saved if we reduce churn to: (a) 4.5%, (b) 4%, (c) 3.5%

2. **Exercise 2**: You have a model with 70% precision and 90% recall. If you flag 10,000 customers as high-risk, how many are true positives? How many are false positives? What's the cost if false positives get a $50 retention offer?

3. **Stretch Goal**: Design a dashboard that shows real-time progress toward our goals. What metrics would you show? How often would you update them? Who's the audience for each metric?

---

## Quick Quiz

1. **What is the most important type of metric for ML project success?**
   - A) Model metrics only (accuracy, precision, recall)
   - B) System metrics only (latency, uptime)
   - C) Business metrics only (revenue, churn rate)
   - D) All three types, with business metrics driving the others

2. **For churn prediction, why do we typically prioritize recall over precision?**
   - A) Recall is easier to calculate
   - B) Missing a churner is more expensive than a false positive
   - C) Precision doesn't matter in classification problems
   - D) Regulators require high recall

3. **True or False: A model with 95% accuracy always performs better than one with 85% accuracy.**

<details>
<summary>Answers</summary>

1. **D** - All three matter, but business metrics are what stakeholders care about
2. **B** - In churn, false negatives (missed churners) are costlier than false positives (unnecessary outreach)
3. **False** - Accuracy can be misleading with imbalanced classes. A model predicting "no churn" for everyone might have 95% accuracy if only 5% churn, but zero business value.

</details>

---

## Summary

- ML success requires three levels of metrics: model performance, system performance, and business impact
- For our churn project: reduce churn from 5% to 4%, saving $24M annually
- ML targets: 80% recall, 60% precision, 0.85 AUC-ROC (prioritize catching churners)
- System targets: <500ms latency, 99.5% uptime, weekly refresh
- Always translate technical metrics to business language for stakeholders

---

## Next Steps

→ Continue to **Lecture 4.3**: Data Sources & Data Contracts (Who Owns the Data?)

---

## Additional Resources

- [Google's Rules of ML: Rule #2 - First, design and implement metrics](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [Microsoft: Defining Success Criteria for ML Projects](https://docs.microsoft.com/en-us/azure/architecture/data-guide/big-data/machine-learning-at-scale)
- [The Practical Guide to Precision-Recall Trade-offs](https://machinelearningmastery.com/precision-recall-and-f-measure-for-imbalanced-classification/)
