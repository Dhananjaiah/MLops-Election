# 📖 Course Overview & Syllabus

## How to Use This Repository

This repository is designed to support a **Udemy-style video course** on MLOps. Here's how to navigate:

### Course Structure

1. **Watch the Videos**: Each lecture corresponds to a markdown file in `/course`
2. **Read the Notes**: Lecture files contain summaries, diagrams, and key concepts
3. **Do the Labs**: Hands-on exercises are included in each lecture
4. **Build the Project**: Follow along in `/project` to build a complete ML system
5. **Test Yourself**: Take quizzes in `/quizzes` after each section
6. **Review Slides**: Presentation materials are in `/slides`

### Suggested Learning Path

```
Week 1: Sections 1-3 (Foundation)
Week 2: Sections 4-6 (Project & Experimentation)
Week 3: Sections 7-9 (Packaging & Pipelines)
Week 4: Sections 10-12 (Deployment & Monitoring)
Week 5: Sections 13-15 (Governance, Capstone & Career)
```

---

## 📚 Complete Table of Contents

### Section 1 – Welcome, Agenda & Big Picture (Foundation)

| Lecture | Title | Duration |
|---------|-------|----------|
| 1.1 | Course Welcome & How to Use This Course | ~10 min |
| 1.2 | What Is MLOps? In One Story, Not a Definition | ~15 min |
| 1.3 | Why Do We Need MLOps? (From "Cool Model" → "Business Value") | ~12 min |
| 1.4 | End-to-End ML System Architecture (From Data to Dashboard) | ~18 min |
| 1.5 | Where Does MLOps Fit in the Overall Data/AI World? | ~10 min |
| 1.6 | Who Does What? (Data Engineer, ML Engineer, MLOps, DevOps, SRE, Product) | ~15 min |
| 1.7 | Agenda of the Entire Course (What We'll Build Step by Step) | ~8 min |
| 1.8 | Sneak Peek: Our End-to-End MLOps Project (What We're Building) | ~12 min |

### Section 2 – Prerequisites, Tools & Environment Setup

| Lecture | Title | Duration |
|---------|-------|----------|
| 2.1 | Skills You Need (and Don't Need) Before Starting | ~8 min |
| 2.2 | Tech Stack Overview (Python, Git, Docker, CI/CD, Cloud/Kubernetes) | ~15 min |
| 2.3 | Setting Up Local Dev Environment | ~20 min |
| 2.4 | Project Structure for an MLOps Course Project | ~12 min |
| 2.5 | Installing Required Python Packages & Virtual Environments | ~15 min |
| 2.6 | Git Basics for MLOps (Branching, PRs, Tags) | ~18 min |
| 2.7 | Running Labs on a Normal / Corporate Laptop (No Fancy GPU Needed) | ~10 min |
| 2.8 | Troubleshooting Common Setup Issues (Ports, Docker, Permissions, Proxies) | ~15 min |

### Section 3 – Understanding the ML Lifecycle & MLOps Responsibilities

| Lecture | Title | Duration |
|---------|-------|----------|
| 3.1 | Business Problem → ML Problem (Framing Correctly) | ~15 min |
| 3.2 | The Classic ML Lifecycle (CRISP-DM Style) | ~18 min |
| 3.3 | Where Things Break in Real Life (Why "Just a Notebook" Fails) | ~15 min |
| 3.4 | MLOps vs DevOps: Same, Similar, Different? | ~12 min |
| 3.5 | Online vs Batch ML Systems (Where Your Work Fits) | ~12 min |
| 3.6 | MLOps Responsibilities in Each Lifecycle Stage | ~15 min |

### Section 4 – Course Project Overview: Real-World Use Case

| Lecture | Title | Duration |
|---------|-------|----------|
| 4.1 | Defining Our Use Case (Customer Churn Prediction) | ~15 min |
| 4.2 | Business Requirements & Success Metrics (How Will We Know It Works?) | ~12 min |
| 4.3 | Data Sources & Data Contracts (Who Owns the Data?) | ~12 min |
| 4.4 | High-Level Architecture for Our Project (Big Diagram) | ~15 min |
| 4.5 | Where This Project Fits in a Real Company's Stack | ~10 min |
| 4.6 | What We Will Automate vs What Will Stay Manual | ~10 min |

### Section 5 – Data Engineering Basics for MLOps

| Lecture | Title | Duration |
|---------|-------|----------|
| 5.1 | Data Types & Storage (DB, Data Lake, CSV, Parquet) | ~15 min |
| 5.2 | Data Ingestion Patterns (Batch, Streaming, APIs) | ~15 min |
| 5.3 | Data Quality & Validation (Basic Checks MLOps Must Enforce) | ~18 min |
| 5.4 | Feature Engineering Overview (Not Deep ML, Just Enough to Operate) | ~15 min |
| 5.5 | Storing Data & Features for Re-use (Intro to Feature Stores) | ~15 min |
| 5.6 | Where Data Engineer Ends and MLOps Starts (Responsibility Boundaries) | ~10 min |

### Section 6 – Reproducible Experimentation: From Notebook to Pipeline

| Lecture | Title | Duration |
|---------|-------|----------|
| 6.1 | The Reproducibility Ladder: Experiments, Versioning & Pipelines | ~15 min |
| 6.2 | Problems with "One Big Notebook" | ~12 min |
| 6.3 | Structuring Experiments (Folders, Scripts, Configs) | ~15 min |
| 6.4 | Experiment Tracking Concepts (Runs, Params, Metrics, Artifacts) | ~15 min |
| 6.5 | Using MLflow (or Similar) to Track Experiments | ~20 min |
| 6.6 | Reproducing Results End-to-End (Same Code, Same Data, Same Model) | ~15 min |
| 6.7 | How MLOps Enforces Reproducibility in a Team | ~12 min |

### Section 7 – Model Packaging: From Script to Service

| Lecture | Title | Duration |
|---------|-------|----------|
| 7.1 | Turning Training Code into a Re-usable Python Package | ~18 min |
| 7.2 | Writing a Clean Inference Function (predict()) | ~15 min |
| 7.3 | Building a REST API with FastAPI / Flask for the Model | ~20 min |
| 7.4 | Introduction to Docker for MLOps (Images, Containers, Registries) | ~18 min |
| 7.5 | Dockerizing the Model Service (Best Practices for Images) | ~20 min |
| 7.6 | Local Testing of the Model API (curl, Postman, Simple UI) | ~15 min |

### Section 8 – Data & Model Versioning, Registry & Artifacts

| Lecture | Title | Duration |
|---------|-------|----------|
| 8.1 | Why Versioning Matters (Data + Code + Model Together) | ~12 min |
| 8.2 | Git for Code, DVC/Delta/etc. for Data (Concepts) | ~15 min |
| 8.3 | Model Registries (MLflow Model Registry / SageMaker / Custom) | ~18 min |
| 8.4 | Model States: Staging, Production, Archived | ~12 min |
| 8.5 | Storing and Retrieving Artifacts in Pipelines | ~15 min |
| 8.6 | Governance Basics: Who Can Promote a Model? How? | ~12 min |

### Section 9 – Automated Training Pipelines & Orchestration

| Lecture | Title | Duration |
|---------|-------|----------|
| 9.1 | Why We Need Pipelines (Not Manual "Run This Script") | ~12 min |
| 9.2 | Pipeline Building Blocks (Tasks / Steps / DAGs) | ~15 min |
| 9.3 | Overview of Common Orchestrators (Airflow, Prefect, Kubeflow, Tekton) | ~18 min |
| 9.4 | Designing a Training Pipeline for Our Project (Diagram) | ~15 min |
| 9.5 | Implementing the Training Pipeline (Example with One Tool) | ~25 min |
| 9.6 | Scheduling, Retries & Failure Handling | ~15 min |
| 9.7 | Where MLOps Sits vs Data Engineers in Orchestration | ~10 min |

### Section 10 – CI/CD for ML Systems (MLOps Delivery)

| Lecture | Title | Duration |
|---------|-------|----------|
| 10.1 | CI/CD Basics Refresher (Build, Test, Deploy) | ~12 min |
| 10.2 | Extra Complexity in ML CI/CD (Data, Drift, Longer Runs) | ~15 min |
| 10.3 | Writing Tests for ML Code (Unit, Integration, Smoke) | ~20 min |
| 10.4 | Building Docker Images & Pushing to Registry in CI | ~18 min |
| 10.5 | Continuous Delivery of Models & APIs (Staging → Prod) | ~15 min |
| 10.6 | Blue/Green & Canary Deployments for ML Services | ~15 min |
| 10.7 | Rollbacks: When a New Model Fails | ~12 min |

### Section 11 – Deployment Architectures & Serving Patterns

| Lecture | Title | Duration |
|---------|-------|----------|
| 11.1 | Online vs Offline vs Near-Real-Time Serving | ~15 min |
| 11.2 | Monolith vs Microservice Model APIs | ~12 min |
| 11.3 | Deploying on VM vs Managed Services vs Kubernetes (Pros & Cons) | ~18 min |
| 11.4 | Basic Kubernetes Concepts for MLOps (Pods, Services, Ingress) | ~20 min |
| 11.5 | Model Serving Frameworks (KFServing, Seldon, Bento – High Level) | ~15 min |
| 11.6 | Choosing a Simple Production-Like Deployment Pattern for Our Project | ~15 min |

### Section 12 – Monitoring, Observability & Model Health

| Lecture | Title | Duration |
|---------|-------|----------|
| 12.1 | What to Monitor in ML Systems (Infra, App, Model) | ~15 min |
| 12.2 | Metrics: Latency, Error Rate, Throughput, Resource Usage | ~15 min |
| 12.3 | Model-Specific Metrics: Drift, Data Skew, Concept Drift | ~18 min |
| 12.4 | Logging & Tracing for Model Services | ~15 min |
| 12.5 | Building Dashboards (Grafana / Cloud Tools) | ~18 min |
| 12.6 | Alerts & Incident Response Playbooks for ML | ~15 min |
| 12.7 | Closing the Loop: Feedback Data, New Labels & Retraining Triggers | ~15 min |
| 12.8 | Cost & Efficiency Considerations (Scaling, Resource Limits, Batch Windows) | ~12 min |

### Section 13 – Governance, Security, and Responsible MLOps

| Lecture | Title | Duration |
|---------|-------|----------|
| 13.1 | Access Control & Secrets Management (API Keys, DB Credentials) | ~15 min |
| 13.2 | Compliance Basics (PII, Data Retention, Audit Logs) | ~15 min |
| 13.3 | Explainability & Model Cards (Tracking What a Model Does) | ~15 min |
| 13.4 | Approval Workflows for Model Promotions | ~12 min |
| 13.5 | Handling Requests to "Delete My Data" or "Explain This Prediction" | ~12 min |
| 13.6 | Organizational Best Practices for MLOps Teams | ~15 min |

### Section 14 – Putting It All Together: End-to-End Capstone

| Lecture | Title | Duration |
|---------|-------|----------|
| 14.1 | Reviewing Our Final Architecture (Start → End Flow) | ~15 min |
| 14.2 | Walking Through the Code & Repos Structure | ~20 min |
| 14.3 | Running the Full Pipeline: Data → Training → Registry → Deploy → Monitor | ~25 min |
| 14.4 | Common Failure Scenarios & How to Debug Them | ~18 min |
| 14.5 | How to Present This Project in Interviews | ~15 min |
| 14.6 | How This Piece Fits into a Larger Enterprise Platform | ~12 min |

### Section 15 – Career, Interviews & Next Steps

| Lecture | Title | Duration |
|---------|-------|----------|
| 15.1 | MLOps Job Roles & Titles (What to Search For) | ~12 min |
| 15.2 | How to Talk About MLOps in Interviews (Storytelling) | ~15 min |
| 15.3 | Building a Portfolio: What Recruiters Actually Want to See | ~15 min |
| 15.4 | Extending This Project (Feature Store, A/B Testing, Online Learning) | ~15 min |
| 15.5 | Learning Path After This Course (Advanced MLOps / LLMOps / Agentic AI) | ~12 min |

---

## 🎯 Learning Objectives

By completing this course, you will be able to:

### Foundation (Sections 1-3)
- Explain what MLOps is and why it matters
- Describe the end-to-end ML system architecture
- Identify the roles and responsibilities in an ML team
- Understand the ML lifecycle and where things typically fail

### Technical Skills (Sections 4-12)
- Set up a production-ready ML project structure
- Build reproducible experiments with proper tracking
- Package ML models as APIs and Docker containers
- Implement CI/CD pipelines for ML systems
- Deploy models to Kubernetes
- Monitor model performance and detect drift

### Professional Skills (Sections 13-15)
- Implement governance and security best practices
- Complete an end-to-end capstone project
- Present your work effectively in interviews
- Plan your continued learning in MLOps

---

## 📝 Assessment

### Quizzes
- Each section has a quiz in `/quizzes`
- 5-10 questions per section
- Mix of multiple choice and short answer

### Hands-on Labs
- Labs are embedded in lecture files
- Follow step-by-step instructions
- Build the churn prediction project incrementally

### Capstone Project
- Section 14 ties everything together
- Run the complete pipeline end-to-end
- Document and present your work

---

## 🛠️ Environment Requirements

### Minimum Requirements
- 8GB RAM
- 20GB free disk space
- Internet connection

### Software
- Python 3.9+
- Docker Desktop
- Git
- VS Code (recommended) or any IDE

### Optional (for advanced labs)
- kubectl (for Kubernetes sections)
- Cloud account (AWS/GCP/Azure) for cloud deployment

---

## 📧 Getting Help

- **Course Forum**: Use GitHub Discussions
- **Bug Reports**: Open a GitHub Issue
- **Office Hours**: [Schedule TBD]
- **Email**: mlops-course@example.com

---

## 📅 Updates

This course is regularly updated. Check the [CHANGELOG.md](CHANGELOG.md) for recent updates.

Last updated: 2024
