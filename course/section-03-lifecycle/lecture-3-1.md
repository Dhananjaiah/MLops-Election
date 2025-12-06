# Lecture 3.1 – Business Problem → ML Problem (Framing Correctly)

## In This Lecture You Will Learn

- [x] Translate business problems into ML problems correctly
- [x] Identify when ML is (and isn't) the right solution
- [x] Define success metrics that matter to the business

---

## Real-World Context

> **Story**: A retail company asked their data science team to "use AI to increase sales." The team built a sophisticated product recommendation system—94% accuracy! But sales didn't increase. Why? The bottleneck was inventory, not recommendations. They solved the wrong problem with the right algorithm.
>
> The most common ML failure isn't bad models—it's solving problems that don't need ML or don't move business metrics.

Before writing any code, understand: What business problem are we solving? Why does it matter?

---

## Main Content

### 1. The Business-to-ML Translation Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FROM BUSINESS TO ML PROBLEM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  BUSINESS PROBLEM                       ML PROBLEM                          │
│  ────────────────────                  ────────────────                     │
│                                                                              │
│  "Reduce customer churn"               Binary classification               │
│  → Predict: Will customer cancel?      → Output: 0 (stay) or 1 (churn)     │
│  → Action: Offer retention deal        → Features: usage, tenure, support   │
│                                                                              │
│  "Recommend products"                   Ranking / Recommendation            │
│  → Suggest items user might buy        → Output: Ranked list of items      │
│  → Action: Show on homepage            → Features: past purchases, clicks   │
│                                                                              │
│  "Detect fraud"                         Anomaly detection                   │
│  → Flag suspicious transactions        → Output: Normal/Anomaly score       │
│  → Action: Block or review             → Features: amount, location, time   │
│                                                                              │
│  "Forecast demand"                      Time series regression              │
│  → Predict next month's sales          → Output: Continuous number          │
│  → Action: Adjust inventory            → Features: historical data, trends  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. When ML Is the Right Solution

**ML Makes Sense When:**

✅ **Pattern exists but rules are complex**
- Example: Spam detection (millions of patterns, constantly evolving)
- Alternative: Writing rules would be impossible to maintain

✅ **You have data and need predictions**
- Example: House price prediction (historical sales data exists)
- Alternative: Manual appraisal is too slow/expensive

✅ **Problem is repeatable at scale**
- Example: Image classification (millions of photos)
- Alternative: Human labeling doesn't scale

**ML Does NOT Make Sense When:**

❌ **Simple rules work fine**
- Example: "If age < 18, deny alcohol purchase"
- Solution: if/else statement, not ML

❌ **No data exists**
- Example: Predicting sales for a brand new product
- Solution: Market research, not ML

❌ **Problem happens once**
- Example: Optimizing one-time event layout
- Solution: Manual planning, not ML

❌ **Cost of wrong prediction is catastrophic**
- Example: Medical diagnosis without human oversight
- Solution: ML assists, human decides

### 3. Defining Success Metrics

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BUSINESS VS ML METRICS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  BUSINESS METRIC                 ML METRIC                                  │
│  (What stakeholders care about)  (What data scientists optimize)            │
│                                                                              │
│  Revenue increase                Precision/Recall                           │
│  Customer satisfaction           F1-Score                                   │
│  Cost reduction                  AUC-ROC                                    │
│  User engagement                 Accuracy                                   │
│                                                                              │
│  THE GAP: ML metrics don't always correlate with business outcomes!         │
│                                                                              │
│  SOLUTION: Define both metrics and track their relationship                 │
│  • ML metric: "Model achieves 85% precision on test set"                   │
│  • Business metric: "Retention offers save $500K/month"                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. The Problem Framing Checklist

Before starting any ML project, answer these questions:

| Question | Why It Matters | Example Answer |
|----------|----------------|----------------|
| What's the business goal? | Clarifies purpose | Reduce churn from 20% to 15% |
| What decision will the model inform? | Ensures actionability | Which customers to offer discounts |
| What data do we have? | Checks feasibility | 2 years of customer transactions |
| What's the baseline? | Sets expectations | Current churn rate is 20% |
| What's success? | Defines done | Save $1M annually in lost revenue |
| What's the cost of being wrong? | Risk assessment | False positives cost $50 per customer |

### 5. Our Course Project: Churn Prediction

Let's apply the framework to our project:

```
Business Problem:
────────────────
"Customers are canceling their subscriptions. We need to reduce churn."

ML Problem:
──────────
Binary classification: Predict which customers will churn in next 30 days

Input:
─────
• Customer demographics (age, location)
• Usage patterns (logins, feature usage)
• Support history (tickets, complaints)
• Billing info (plan, payment history)

Output:
──────
Probability score: 0.0 (won't churn) to 1.0 (will churn)

Action:
──────
• Score > 0.7: Proactive outreach, retention offer
• Score 0.4-0.7: Monitor closely
• Score < 0.4: No action needed

Success Metrics:
───────────────
• ML: AUC-ROC > 0.80, Precision > 0.70
• Business: Reduce churn from 20% to 15%
• Financial: Save $2M annually in lost revenue
```

---

## Diagrams

```
Problem Framing Flow:
════════════════════

Business Stakeholder Says:
"We need to use AI for X"
         │
         ▼
Ask: "What outcome do you want?"
         │
         ├─ More revenue → How?
         ├─ Fewer costs → Which costs?
         ├─ Better experience → Measured how?
         └─ Faster process → What's slow?
         │
         ▼
Define specific, measurable goal
         │
         ▼
Check: Can ML help?
         │
         ├─ YES → Define ML problem
         │         (classification/regression/etc.)
         │
         └─ NO → Suggest alternative
                  (rules, process change, etc.)
```

---

## Lab / Demo

### Prerequisites

- Understanding of basic ML concepts
- Familiarity with the course project

### Step-by-Step Instructions

```bash
# Step 1: Review the project brief
cd project
cat README.md | grep -A 20 "Business Problem"

# Step 2: Explore the data
head data/customer_data.csv

# Step 3: Calculate baseline metrics
python -c "
import pandas as pd
df = pd.read_csv('data/customer_data.csv')
churn_rate = df['churned'].mean()
print(f'Baseline churn rate: {churn_rate:.2%}')
"

# Step 4: Define what success looks like
# Create a file with success criteria
echo "Success Criteria:
- Reduce churn rate from 20% to 15%
- Model precision > 70%
- Implementation cost < $100K
" > success_criteria.txt
```

### Expected Output

```
$ cat success_criteria.txt
Success Criteria:
- Reduce churn rate from 20% to 15%
- Model precision > 70%
- Implementation cost < $100K

$ python -c "import pandas as pd; df = pd.read_csv('data/customer_data.csv'); print(f'Baseline churn rate: {df[\"churned\"].mean():.2%}')"
Baseline churn rate: 20.00%
```

### Explanation

1. **Step 1**: Understanding the business context is essential before coding
2. **Step 2**: Data exploration validates that the problem is solvable with ML
3. **Step 3**: Baseline metrics set expectations for model performance
4. **Step 4**: Written success criteria prevent scope creep and misaligned expectations

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Building a model before understanding the business problem. Always start with "why."

- ⚠️ **Pitfall 2**: Optimizing ML metrics that don't correlate with business outcomes. Track both.

- ⚠️ **Pitfall 3**: Assuming ML is always the answer. Sometimes a simple rule or process change works better.

---

## Homework / Practice

1. **Exercise 1**: Take a real business problem from your company or daily life. Frame it as an ML problem using the checklist above.

2. **Exercise 2**: Find 3 examples where ML was used but a simple rule would have been better. (Hint: Look for over-engineered solutions)

3. **Stretch Goal**: Calculate the ROI of our churn prediction model. If we save 5% churn on 10,000 customers at $50/month, what's the annual savings?

---

## Quick Quiz

1. **What's the first step in framing an ML problem?**
   - A) Collect data
   - B) Choose an algorithm
   - C) Understand the business goal
   - D) Build a prototype

2. **When is ML NOT a good solution?**
   - A) When simple rules work fine
   - B) When you have lots of data
   - C) When patterns are complex
   - D) When scaling is needed

3. **True or False: High model accuracy always means business success.**

<details>
<summary>Answers</summary>

1. **C** - Always start with the business goal before any technical work
2. **A** - If simple rules work, use them instead of ML
3. **False** - ML metrics don't always correlate with business outcomes

</details>

---

## Summary

- Translate business problems into specific, measurable ML problems
- ML makes sense for complex patterns at scale with available data
- ML doesn't make sense for simple rules or one-time problems
- Define both ML metrics (accuracy, precision) and business metrics (revenue, costs)
- Always ask: What decision will the model inform? What's the action?
- Our course project: Churn prediction to save $2M/year

---

## Next Steps

→ Continue to **Lecture 3.2**: The Classic ML Lifecycle (CRISP-DM Style)

---

## Additional Resources

- [Google's Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) - When to use ML
- [Designing ML Systems](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) - Problem framing chapter
- [ML Canvas](https://www.louisdorard.com/machine-learning-canvas) - Template for framing ML problems
- [Hidden Technical Debt in ML Systems](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) - Google's foundational paper
