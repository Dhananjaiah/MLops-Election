# Lecture 4.1 – Defining Our Use Case (Customer Churn Prediction)

## In This Lecture You Will Learn

- [x] Understand what customer churn is and why it's a critical business problem
- [x] Frame a business problem into a well-defined ML problem
- [x] Identify the key stakeholders and success criteria for a churn prediction project

---

## Real-World Context

> **Story**: Meet Alex, a ML engineer at "StreamFlix," a video streaming service with 5 million subscribers. The CEO just learned that they're losing 8% of customers every month—that's 400,000 subscribers churning annually, costing $48M in lost revenue! The marketing team has been sending generic "we miss you" emails to random users with poor results. Alex's mission: build a ML system that predicts *which* customers will churn *before* they do, so targeted retention campaigns can save them. This isn't just a cool ML problem—it's directly tied to the company's survival.

In the real world, customer churn prediction is one of the most common and impactful ML use cases. From telecom to SaaS to banking, every subscription-based business needs to predict and prevent churn. This makes it the perfect project to learn MLOps—it's relevant, well-understood, and has clear business value.

---

## Main Content

### 1. What Is Customer Churn?

**Definition**: Churn is when a customer stops using your product or service. In subscription businesses, it's when they cancel, don't renew, or stop paying.

**Why It Matters**:
- **Cost**: Acquiring a new customer costs 5-25x more than retaining an existing one
- **Revenue**: A 5% increase in retention can increase profits by 25-95%
- **Growth**: High churn makes growth impossible (you're filling a leaky bucket)

**Types of Churn**:
- **Voluntary Churn**: Customer actively cancels (dissatisfied, found competitor, too expensive)
- **Involuntary Churn**: Payment fails, credit card expires (easier to prevent)
- **Partial Churn**: Downgrades to cheaper plan (less severe but still negative)

### 2. From Business Problem to ML Problem

**The Business Ask**:
> "We're losing too many customers. Can ML help us keep them?"

**Translation to ML Problem**:
- **Type**: Binary classification problem
- **Target Variable**: Will customer churn in next 30 days? (Yes/No)
- **Prediction Window**: 30 days (gives time to intervene)
- **Input Features**: Customer demographics, usage patterns, support tickets, payment history
- **Output**: Probability score (0-100%) that customer will churn

**Why 30 Days?**
- Too short (7 days): Not enough time for retention campaign
- Too long (6 months): Prediction becomes inaccurate, loses urgency
- 30 days: Sweet spot for actionable interventions

### 3. Our Specific Use Case

**Company**: "TeleConnect" - A telecommunications provider with 2 million customers

**Current Situation**:
- Monthly churn rate: 5% (100,000 customers/year)
- Average customer lifetime value (CLV): $1,200
- Annual revenue lost to churn: $120 million
- Current retention budget: $20 million (mostly wasted on non-churners)

**Our Goal**:
Build a ML system that:
1. Predicts which customers will churn in the next 30 days
2. Scores them by churn probability (0-100%)
3. Enables targeted retention campaigns
4. Runs automatically every week
5. Monitors its own performance and alerts when accuracy drops

**Success Criteria** (covered in next lecture):
- Model accuracy targets
- Business impact metrics
- Operational requirements

---

## Diagrams

```
┌─────────────────────────────────────────────────────────────────────┐
│              Business Problem → ML Problem Framework                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Business Problem: "We're losing customers!"                        │
│         ↓                                                           │
│  Quantify:  "5% monthly churn = $120M lost/year"                   │
│         ↓                                                           │
│  Frame:     "Predict who will churn in next 30 days"               │
│         ↓                                                           │
│  ML Problem: Binary Classification                                  │
│              Input:  Customer features                              │
│              Output: Churn probability (0-100%)                     │
│         ↓                                                           │
│  Action:    "Target high-risk customers with retention offers"      │
│         ↓                                                           │
│  Measure:   "Reduced churn from 5% to 4% = $24M saved"            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-4-1-diagram.png)

> Diagram shows the churn prediction lifecycle: Customer → Usage Data → ML Model → Risk Score → Retention Campaign → Outcome

---

## Lab / Demo

### Prerequisites

- Completed Section 1-3 lectures
- Basic understanding of classification problems

### Step-by-Step Instructions

```bash
# Step 1: Navigate to the project directory
cd project

# Step 2: Review the business problem document
cat docs/business_problem.md

# Step 3: Explore the sample customer data
head -20 data/raw/customers.csv

# Step 4: Check the data dictionary
cat docs/data_dictionary.md
```

### Expected Output

```
customer_id,tenure_months,monthly_charges,total_charges,contract_type,payment_method,num_support_tickets,churned
C001,24,89.99,2159.76,Month-to-Month,Credit Card,2,0
C002,6,65.50,393.00,Month-to-Month,Bank Transfer,5,1
C003,48,110.25,5292.00,Two Year,Credit Card,0,0
...
```

### Explanation

1. **Step 1**: Navigate to project root where all our work will happen
2. **Step 2**: Read the business requirements and understand the problem context
3. **Step 3**: Look at actual customer data to understand what features we have
4. **Step 4**: Learn what each column means and its data type

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Defining churn too broadly. "Not active" doesn't mean churned—they might be on vacation. Be specific: canceled subscription, payment failed, explicitly unsubscribed.

- ⚠️ **Pitfall 2**: Choosing the wrong prediction window. If you predict "will churn within 6 months," the prediction becomes stale quickly. 30 days is typical for most businesses.

- ⚠️ **Pitfall 3**: Ignoring the cost-benefit analysis. Not all churned customers are worth saving. A customer paying $10/month isn't worth a $100 retention offer.

---

## Homework / Practice

1. **Exercise 1**: Write a one-paragraph problem statement for a churn prediction project at a fictional gym membership company. Include: business impact, prediction window, and target variable.

2. **Exercise 2**: List 10 features you think would be predictive of customer churn for a mobile phone service provider. Think about: usage patterns, billing, support interactions, demographics.

3. **Stretch Goal**: Research a real company's churn problem (Netflix, Spotify, etc.). Find public information about their churn rate and calculate the annual revenue impact if they have 100M subscribers at $15/month.

---

## Quick Quiz

1. **What is customer churn?**
   - A) When customers complain about your service
   - B) When customers stop using your product or cancel their subscription
   - C) When customers reduce their usage
   - D) When customers refer other customers

2. **Why is a 30-day prediction window common for churn prediction?**
   - A) It's the easiest to predict accurately
   - B) It gives enough time to intervene but stays actionable
   - C) It's required by regulations
   - D) Customers always decide to churn exactly 30 days in advance

3. **True or False: In churn prediction, we should try to save every customer regardless of cost.**

<details>
<summary>Answers</summary>

1. **B** - Churn specifically means customers stop using or cancel the service
2. **B** - 30 days balances prediction accuracy with time to take action
3. **False** - We need to consider customer lifetime value vs. retention cost

</details>

---

## Summary

- Customer churn is when customers stop using your service—it's expensive and common across subscription businesses
- Churn prediction is a binary classification problem: predict which customers will churn in the next N days
- Our project: predict churn for "TeleConnect" with 2M customers losing $120M/year to churn
- Good ML problems have clear business value, measurable success criteria, and actionable outputs
- 30-day prediction window is typical—balances accuracy with time to intervene

---

## Next Steps

→ Continue to **Lecture 4.2**: Business Requirements & Success Metrics (How Will We Know It Works?)

---

## Additional Resources

- [Harvard Business Review: The Value of Keeping the Right Customers](https://hbr.org/2014/10/the-value-of-keeping-the-right-customers)
- [Kaggle Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) - Real data for practice
- [AWS: Customer Churn Prediction Blog](https://aws.amazon.com/blogs/machine-learning/build-a-customer-churn-prediction-model-using-amazon-sagemaker/) - Industry best practices
