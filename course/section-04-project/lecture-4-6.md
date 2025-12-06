# Lecture 4.6 – What We Will Automate vs What Will Stay Manual

## In This Lecture You Will Learn

- [x] Decide which parts of the ML workflow should be automated vs. manual
- [x] Understand the trade-offs between automation and human oversight
- [x] Create a phased automation roadmap (MVP → Mature System)

---

## Real-World Context

> **Story**: Rachel's team spent 6 months building "fully automated" ML retraining. The system would automatically retrain models weekly, evaluate them, and deploy to production—no human in the loop. Week 1: a data bug caused the model to predict everyone would churn. It auto-deployed to production. Disaster. Week 4: a code change broke feature engineering. Auto-deployed. Another disaster. Week 7: a model improved accuracy from 82% to 83%... by always predicting "no churn." Auto-deployed. You see the pattern. After three outages, they added manual approval gates at every step. The lesson: automate the tedious parts, but keep humans in critical decision points—especially in the beginning.

In the real world, teams that automate too much, too soon create brittle systems that fail spectacularly. Teams that automate too little waste engineering time on repetitive tasks. The art is knowing what to automate when.

---

## Main Content

### 1. The Automation Spectrum

```
Manual              Semi-Automated          Fully Automated
  │                      │                        │
  │                      │                        │
  ↓                      ↓                        ↓
Human does         Human approves            Machine does
everything         machine's work            everything
```

**Example: Model Deployment**
- **Manual**: Data scientist manually copies model file to production server
- **Semi-Automated**: CI/CD builds Docker image, but human clicks "deploy to prod"
- **Fully Automated**: On passing tests, model auto-deploys to production with canary rollout

### 2. What to Automate (And When)

#### Phase 1: MVP (Month 1-3) - Minimal Automation

**Automate** ✅:
- Data pipeline runs on schedule (daily cron job)
- Code linting and unit tests on pull requests
- Docker image building in CI
- Basic monitoring alerts (API down, high error rate)

**Keep Manual** 🤚:
- Feature engineering decisions
- Model algorithm selection
- Hyperparameter tuning
- Model evaluation and approval
- Deployment to production
- Incident response and debugging

**Why**: In early stages, you're still figuring out what works. Premature automation locks in bad decisions.

#### Phase 2: Stable System (Month 4-6) - Moderate Automation

**Automate** ✅:
- Data validation checks (schema, ranges, nulls)
- Hyperparameter tuning (AutoML, grid search)
- Model training pipeline (triggered weekly)
- Experiment logging (automatic to MLflow)
- Staging deployment (auto-deploy to staging environment)
- Performance regression tests
- Basic drift detection

**Keep Manual** 🤚:
- Production deployment (human approval required)
- Model architecture changes
- Data pipeline major changes
- Incident response (humans investigate alerts)
- A/B test result interpretation

**Why**: You've validated the basics and can trust automation for repetitive, well-understood tasks.

#### Phase 3: Mature System (Month 7+) - High Automation

**Automate** ✅:
- End-to-end training pipeline
- Automatic model registration to registry
- Canary deployments (5% → 25% → 100% traffic)
- Automatic rollback on performance drops
- Drift detection triggers retraining
- Auto-scaling based on traffic
- Self-healing (restart failed pods)

**Keep Manual** 🤚:
- Major architecture changes
- Business logic changes
- Compliance reviews
- Incident root cause analysis
- Strategic decisions (e.g., "Should we even build this?")

**Why**: The system is proven and stable. Automation reduces toil and enables faster iterations.

### 3. Decision Framework: Should I Automate This?

Ask these questions:

1. **Is it repetitive?** (Runs >10x per month → Yes, automate)
2. **Is it error-prone when manual?** (Humans forget steps → Yes, automate)
3. **Is the cost of failure high?** (Can break production → No, keep manual approval)
4. **Is the process stable?** (Changes every week → No, wait to automate)
5. **Is it time-consuming?** (Takes >30 min → Yes, automate)
6. **Can it be tested?** (Hard to validate automatically → Keep manual oversight)

**Examples**:

| Task | Repetitive? | Error-Prone? | High Failure Cost? | Stable? | → Decision |
|------|-------------|--------------|-------------------|---------|-----------|
| Running tests | ✅ | ✅ | ❌ | ✅ | **Automate** |
| Building Docker images | ✅ | ✅ | ❌ | ✅ | **Automate** |
| Model training | ✅ | ❌ | ❌ | ✅ | **Automate** |
| Deploying to prod | ❌ | ✅ | ✅ | ✅ | **Semi-automate** (approval gate) |
| Interpreting drift | ❌ | ❌ | ✅ | ❌ | **Keep manual** |
| Responding to incidents | ❌ | ❌ | ✅ | ❌ | **Keep manual** |

### 4. Our Churn Project: Automation Roadmap

**Week 1-4 (Course Start)**:
- Automated: CI tests, Docker builds
- Manual: Everything else

**Week 5-8**:
- Automated: Data pipeline, experiment tracking
- Manual: Model evaluation, deployment

**Week 9-12**:
- Automated: Training pipeline, staging deployment
- Manual: Production deployment (with approval)

**Week 13-16**:
- Automated: Canary deployments, rollbacks
- Manual: Major changes, incident response

**Post-Course (If Continued)**:
- Automated: Drift-triggered retraining, auto-scaling
- Manual: Strategic decisions, compliance

---

## Diagrams

```
┌────────────────────────────────────────────────────────────────┐
│           Automation Roadmap (Our Churn Project)               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1 (MVP)         Phase 2 (Stable)      Phase 3 (Mature) │
│  Month 1-3             Month 4-6             Month 7+          │
│                                                                 │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐   │
│  │ Automated:  │      │ Automated:  │      │ Automated:  │   │
│  │ - CI tests  │      │ - Training  │      │ - Canary    │   │
│  │ - Docker    │      │ - Logging   │      │ - Rollback  │   │
│  │             │      │ - Staging   │      │ - Drift→    │   │
│  │             │      │   deploy    │      │   Retrain   │   │
│  └─────────────┘      └─────────────┘      └─────────────┘   │
│                                                                 │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐   │
│  │ Manual:     │      │ Manual:     │      │ Manual:     │   │
│  │ - Training  │      │ - Prod      │      │ - Strategy  │   │
│  │ - Eval      │      │   deploy    │      │ - Incidents │   │
│  │ - Deploy    │      │   approval  │      │             │   │
│  │ - Everything│      │ - Major     │      │             │   │
│    else!       │      │   changes   │      │             │   │
│  └─────────────┘      └─────────────┘      └─────────────┘   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

![Diagram Placeholder](../../assets/diagrams/lecture-4-6-diagram.png)

> Diagram shows automation increasing over time as system matures, but critical decisions remain manual

---

## Lab / Demo

### Prerequisites

- Completed all previous lectures in Section 4
- Understanding of CI/CD concepts

### Step-by-Step Instructions

```bash
# Step 1: Review our automation plan
cd project/docs
cat automation_roadmap.md

# Step 2: Check current automation level (what's already automated)
cd ../.github/workflows
ls -la
cat ci.yml

# Step 3: See manual approval gates in our deployment process
cd ../../deployment
cat deployment_checklist.md

# Step 4: View monitoring alerts (what triggers manual intervention)
cd ../monitoring
cat alert_rules.yaml
```

### Expected Output

```yaml
# ci.yml - What's automated today
name: CI
on: [push, pull_request]
jobs:
  test:
    - Run linting
    - Run unit tests
    - Build Docker image
  
# deployment_checklist.md - What requires human approval
- [ ] Model performance reviewed by data scientist
- [ ] Business stakeholders notified
- [ ] Rollback plan documented
- [ ] Deployed to staging and tested
- [ ] Approval from ML lead
→ Then: Deploy to production

# alert_rules.yaml - When humans get paged
alerts:
  - name: ModelAccuracyDrop
    condition: accuracy < 0.75
    action: Page on-call ML engineer
  
  - name: DataSchemaMismatch
    condition: schema_validation_failed
    action: Block pipeline, alert team
```

### Explanation

1. **Step 1**: Understand the phased plan for increasing automation
2. **Step 2**: See what's currently automated (CI tests, builds)
3. **Step 3**: Identify manual approval gates (safety checks)
4. **Step 4**: Learn when alerts trigger human intervention

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Automating too early. If your process changes weekly, automation becomes technical debt. Stabilize first, then automate.

- ⚠️ **Pitfall 2**: Removing all human oversight. Even mature systems need manual approval for production deployments, especially for high-stakes applications.

- ⚠️ **Pitfall 3**: Automating without monitoring. If you automate a process, you MUST have alerts for when it fails. Silent failures are worse than manual processes.

---

## Homework / Practice

1. **Exercise 1**: For our churn project, list 3 more tasks we should automate and 3 we should keep manual. Justify each decision using the 6-question framework.

2. **Exercise 2**: Imagine our model just auto-deployed to production and churn predictions are now 50% higher than yesterday. Write a 5-step incident response plan. What's automated? What's manual?

3. **Stretch Goal**: Design an approval workflow for production deployments. Who needs to approve? What checks must pass? What information do they see to make the decision?

---

## Quick Quiz

1. **When should you automate a task?**
   - A) Immediately, automation is always better
   - B) After the process is repetitive, stable, and well-understood
   - C) Never, humans should always be in control
   - D) Only if management approves the budget

2. **Which task should likely stay manual even in mature ML systems?**
   - A) Running unit tests
   - B) Building Docker images
   - C) Deploying to production (final approval)
   - D) Logging experiment metrics

3. **True or False: In Phase 1 (MVP), most tasks should be automated to save time.**

<details>
<summary>Answers</summary>

1. **B** - Automate when processes are repetitive, error-prone, and stable
2. **C** - Production deployments typically require human approval even in mature systems
3. **False** - In Phase 1, keep most things manual while you're still learning and iterating

</details>

---

## Summary

- Automation exists on a spectrum: manual → semi-automated → fully automated
- Start with minimal automation (MVP), increase as the system matures
- Automate: repetitive, error-prone, stable, low-risk tasks
- Keep manual: strategic decisions, incident response, high-risk changes
- Always monitor automated processes—silent failures are dangerous
- Even mature systems keep human oversight for production deployments

---

## Next Steps

→ Continue to **Lecture 5.1**: Data Types & Storage (DB, Data Lake, CSV, Parquet)

---

## Additional Resources

- [Google: The Production Maturity Model](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- [Microsoft: MLOps Maturity Model](https://docs.microsoft.com/en-us/azure/architecture/example-scenario/mlops/mlops-maturity-model)
- [The DevOps Handbook: When to Automate](https://itrevolution.com/book/the-devops-handbook/)
