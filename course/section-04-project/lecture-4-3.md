# Lecture 4.3 – Data Sources & Data Contracts (Who Owns the Data?)

## In This Lecture You Will Learn

- [x] Identify and document all data sources needed for a churn prediction model
- [x] Understand the concept of data contracts and why they matter
- [x] Navigate data ownership and access in a real organization

---

## Real-World Context

> **Story**: Maya's churn model was ready to deploy. Then the CRM system was "upgraded" overnight, and the `last_login_date` column disappeared—renamed to `last_activity_ts`. Her model broke instantly. No one told her. She found out when customers started complaining. Meanwhile, the payments team changed how they calculate `monthly_charges`, affecting 30% of her training features. The problem? No data contract. No agreement about what data looks like, who owns it, or who to notify about changes. Maya spent 3 months building a model that broke in 3 hours.

In the real world, data infrastructure is constantly changing. Without clear contracts about data structure, ownership, and change management, ML systems become fragile and break silently.

---

## Main Content

### 1. Data Sources for Our Churn Model

**Source 1: Customer Master Database (CRM)**
- **Owner**: Sales & Marketing team
- **System**: Salesforce / PostgreSQL database
- **Refresh**: Real-time (updates on every customer interaction)
- **Access**: Read-only API, requires authentication
- **Key Fields**: customer_id, signup_date, account_type, contract_type, region

**Source 2: Usage & Activity Logs**
- **Owner**: Product Engineering team
- **System**: Clickstream data warehouse (BigQuery/Snowflake)
- **Refresh**: Hourly batch loads
- **Access**: SQL query access, requires VPN
- **Key Fields**: customer_id, last_login_date, session_duration, feature_usage_count

**Source 3: Billing & Payments**
- **Owner**: Finance team
- **System**: Payment processor API + internal billing DB
- **Refresh**: Daily (end of day)
- **Access**: Limited to finance team + approved data scientists
- **Key Fields**: customer_id, monthly_charges, payment_method, failed_payments, account_balance

**Source 4: Customer Support Tickets**
- **Owner**: Customer Success team
- **System**: Zendesk / ServiceNow
- **Refresh**: Near real-time via webhook
- **Access**: API access with rate limits
- **Key Fields**: customer_id, ticket_count, avg_resolution_time, satisfaction_score

### 2. What Is a Data Contract?

A **data contract** is a formal agreement between data producers (teams who create/own data) and data consumers (your ML system) that specifies:

1. **Schema**: Exact field names, data types, allowed values
2. **SLA**: How often data is updated, expected latency
3. **Quality**: Completeness requirements, validation rules
4. **Versioning**: How and when schema changes happen
5. **Ownership**: Who to contact when things break
6. **Access**: Authentication, permissions, rate limits

**Example Data Contract for Customer Data**:
```yaml
data_source: customer_master
owner: sales_team@company.com
version: 2.1.0

schema:
  customer_id:
    type: string (UUID)
    required: true
    description: "Unique customer identifier"
  
  signup_date:
    type: date (YYYY-MM-DD)
    required: true
    description: "Date customer created account"
  
  contract_type:
    type: enum ["Month-to-Month", "One Year", "Two Year"]
    required: true
    description: "Contract commitment level"

sla:
  update_frequency: "real-time"
  max_delay: "5 minutes"
  uptime: "99.9%"

change_policy:
  breaking_changes: "30 days advance notice"
  deprecation_period: "90 days"
  notification_channel: "#data-changes Slack channel"
```

### 3. Navigating Data Ownership & Access

**Key Stakeholders**:
- **Data Engineering**: Builds pipelines, maintains data warehouse
- **Platform Teams**: Own databases, APIs, infrastructure
- **Business Teams**: Own the meaning and quality of their data
- **Data Governance**: Sets policies, approves access

**How to Get Access**:
1. **Identify the owner**: Check data catalog or ask data engineering
2. **Explain the use case**: Why you need the data, how it will be used
3. **Request access**: Submit ticket/form with security approval
4. **Sign data agreement**: Commit to using data appropriately
5. **Get credentials**: API keys, database credentials, VPN access

**Common Access Issues**:
- PII (Personally Identifiable Information) requires extra approvals
- Production databases often read-only to prevent accidents
- Cross-region data access may be blocked by compliance
- Some data is "too sensitive" and requires anonymization first

---

## Diagrams

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Data Sources for Churn Model                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   📊 Customer CRM          📈 Usage Logs         💳 Billing DB      │
│   (Salesforce)             (Data Warehouse)      (Finance System)   │
│        │                         │                      │            │
│        │ API                     │ SQL                  │ API        │
│        └─────────────┬───────────┴──────────────────────┘           │
│                      │                                               │
│                      ↓                                               │
│              🔄 Data Pipeline                                        │
│         (Extract, Transform, Load)                                   │
│                      │                                               │
│                      ↓                                               │
│         📦 Feature Store / Data Lake                                 │
│         (Unified, versioned features)                                │
│                      │                                               │
│                      ↓                                               │
│              🤖 ML Training Pipeline                                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-4-3-diagram.png)

> Diagram shows data flow from multiple source systems through data contracts to the ML system

---

## Lab / Demo

### Prerequisites

- Completed Lectures 4.1 and 4.2
- Access to project repository

### Step-by-Step Instructions

```bash
# Step 1: Review the data sources documentation
cd project/docs
cat data_sources.md

# Step 2: View sample data contracts
cat contracts/customer_data_contract.yaml
cat contracts/usage_data_contract.yaml

# Step 3: Check data access credentials setup
cat config/data_access.yaml.example

# Step 4: Test connection to data sources (mock)
cd ../scripts
python test_data_connections.py --dry-run
```

### Expected Output

```
✓ Customer CRM: Connection successful (mock mode)
  - Schema version: 2.1.0
  - Last updated: 2024-01-15 10:30:00
  - Records available: 2,000,000

✓ Usage Logs: Connection successful (mock mode)
  - Schema version: 1.5.2
  - Last updated: 2024-01-15 09:00:00
  - Records available: 150,000,000

✓ Billing Database: Connection successful (mock mode)
  - Schema version: 3.0.1
  - Last updated: 2024-01-14 23:59:59
  - Records available: 2,000,000

⚠ Customer Support: Rate limited (100 requests/hour)
  - Consider using daily batch export instead
```

### Explanation

1. **Step 1**: Understand what data is needed and where it lives
2. **Step 2**: Review formal contracts that define data structure and SLAs
3. **Step 3**: Learn how credentials are managed (never hardcoded!)
4. **Step 4**: Validate that connections work before building the pipeline

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Assuming data will never change. It will. Systems get upgraded, schemas evolve, fields get renamed. Build defensive code and monitoring to detect schema changes.

- ⚠️ **Pitfall 2**: Not documenting data lineage. If your model starts performing poorly, you need to trace back: did the data change? Which upstream system? Without lineage, debugging is impossible.

- ⚠️ **Pitfall 3**: Hardcoding database credentials in code. Use environment variables, secret managers, or configuration files that are never committed to git.

---

## Homework / Practice

1. **Exercise 1**: Create a data contract for one of our sources (choose: customer, usage, or billing). Include schema, SLA, owner, and change policy.

2. **Exercise 2**: List 3 potential data quality issues that could break our churn model and how you'd detect each one early.

3. **Stretch Goal**: Design a data lineage diagram showing how raw data flows from source systems through transformations to the final features used by the model.

---

## Quick Quiz

1. **What is a data contract?**
   - A) A legal document signed with vendors
   - B) A formal agreement defining data structure, ownership, and SLAs
   - C) A database schema
   - D) An API endpoint

2. **Why do ML systems need data contracts?**
   - A) To meet compliance requirements
   - B) To prevent silent failures when upstream data changes
   - C) To bill other teams for data usage
   - D) To make documentation look professional

3. **True or False: Once you have access to a data source, you can assume it will stay the same forever.**

<details>
<summary>Answers</summary>

1. **B** - A data contract is a formal agreement about data structure, SLAs, and change management
2. **B** - Contracts prevent breakage when upstream systems change without warning
3. **False** - Data sources change constantly. Always plan for schema evolution and have monitoring in place.

</details>

---

## Summary

- Our churn model needs data from 4 sources: CRM, usage logs, billing, and support tickets
- Each source has different owners, update frequencies, and access requirements
- Data contracts formalize what data looks like and how/when it can change
- Good data contracts include: schema, SLAs, versioning, ownership, and change policies
- Always plan for data to change—build monitoring and defensive code

---

## Next Steps

→ Continue to **Lecture 4.4**: High-Level Architecture for Our Project (Big Diagram)

---

## Additional Resources

- [Google Cloud: Data Contracts Best Practices](https://cloud.google.com/architecture/devops/devops-process-work-visibility-in-value-stream)
- [The Rise of Data Contracts (article)](https://www.datafold.com/blog/data-contracts)
- [dbt: Building Data Contracts](https://docs.getdbt.com/docs/collaborate/govern/about-data-contracts)
