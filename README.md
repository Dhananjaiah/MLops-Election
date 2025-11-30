# 🚀 Complete MLOps Course: From Notebook to Production

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Course](https://img.shields.io/badge/Course-Udemy%20Style-orange)

A production-grade, Udemy-style MLOps course repository featuring hands-on labs, slides, and a complete end-to-end Customer Churn Prediction project.

## 📋 Table of Contents

- [Course Overview](#course-overview)
- [Who Is This Course For?](#who-is-this-course-for)
- [What You'll Learn](#what-youll-learn)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Course Sections](#course-sections)
- [The Reference Project](#the-reference-project)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Course Overview

This course takes you from a Jupyter notebook prototype to a production-ready ML system. You'll learn the complete MLOps lifecycle through:

- **15 comprehensive sections** covering every aspect of MLOps
- **Hands-on labs** with real code you can run
- **A single end-to-end project** (Customer Churn Prediction) that evolves throughout the course
- **Production-grade infrastructure** templates and configurations

> 📖 For detailed syllabus and how to navigate this repo, see [COURSE_OVERVIEW.md](COURSE_OVERVIEW.md)

## 👤 Who Is This Course For?

- **Data Scientists** who want to deploy their models
- **ML Engineers** looking to formalize their MLOps practices
- **DevOps Engineers** expanding into ML systems
- **Software Engineers** transitioning to ML
- **Anyone** interested in production machine learning

### Prerequisites

- Basic Python programming
- Familiarity with ML concepts (training, evaluation, etc.)
- Basic command line knowledge
- No advanced math or PhD required!

## 📚 What You'll Learn

By the end of this course, you will be able to:

- ✅ Structure ML projects for production
- ✅ Version data, code, and models together
- ✅ Build reproducible training pipelines
- ✅ Package models as REST APIs
- ✅ Containerize ML applications with Docker
- ✅ Set up CI/CD for ML systems
- ✅ Deploy to Kubernetes
- ✅ Monitor model performance and detect drift
- ✅ Implement governance and security best practices
- ✅ Present your MLOps project in job interviews

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.9+ |
| **ML Framework** | scikit-learn |
| **API Framework** | FastAPI |
| **Containerization** | Docker, Docker Compose |
| **Version Control** | Git, GitHub |
| **CI/CD** | GitHub Actions |
| **Experiment Tracking** | MLflow (optional) |
| **Orchestration** | Overview of Airflow, Prefect, etc. |
| **Deployment** | Kubernetes basics |
| **Monitoring** | Prometheus, Grafana concepts |

## 📁 Repository Structure

```
.
├── README.md                 # This file - course overview
├── COURSE_OVERVIEW.md        # Detailed syllabus
├── course/                   # Course content (15 sections)
│   ├── section-01-intro/
│   ├── section-02-setup/
│   ├── ...
│   └── section-15-career/
├── project/                  # End-to-end reference project
│   ├── src/churn_mlops/      # Python package
│   ├── notebooks/            # Exploration notebooks
│   ├── config/               # Configuration files
│   ├── tests/                # Unit tests
│   ├── Dockerfile
│   └── docker-compose.yml
├── infra/                    # Infrastructure templates
│   ├── ci/                   # GitHub Actions workflows
│   └── k8s/                  # Kubernetes manifests
├── slides/                   # Slide deck placeholders
├── quizzes/                  # Section quizzes
└── assets/                   # Diagrams and images
    ├── diagrams/
    └── images/
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mlops-course.git
cd mlops-course
```

### 2. Set Up Your Environment

```bash
cd project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Navigate the Course

1. Start with [COURSE_OVERVIEW.md](COURSE_OVERVIEW.md) for the complete syllabus
2. Follow the sections in order under `/course`
3. Complete hands-on labs in `/project`
4. Test your knowledge with quizzes in `/quizzes`

### 4. Run the Project

```bash
# Train a model
cd project
python -m churn_mlops.models.train

# Start the API
uvicorn churn_mlops.serving.app:app --reload

# Or use Docker
docker-compose up
```

## 📖 Course Sections

| Section | Title | Topics |
|---------|-------|--------|
| 1 | Welcome & Big Picture | What is MLOps, why we need it, course agenda |
| 2 | Prerequisites & Setup | Dev environment, tools, Git basics |
| 3 | ML Lifecycle | CRISP-DM, where things break, responsibilities |
| 4 | Project Overview | Use case, requirements, architecture |
| 5 | Data Engineering | Data types, ingestion, quality, feature stores |
| 6 | Experimentation | Reproducibility, experiment tracking, MLflow |
| 7 | Model Packaging | Python packages, APIs, Docker |
| 8 | Versioning & Registry | Data/model versioning, model registry |
| 9 | Training Pipelines | Orchestration, DAGs, scheduling |
| 10 | CI/CD for ML | Testing, building, deploying ML systems |
| 11 | Deployment | Serving patterns, Kubernetes basics |
| 12 | Monitoring | Metrics, drift detection, alerting |
| 13 | Governance | Security, compliance, model cards |
| 14 | Capstone | Complete end-to-end walkthrough |
| 15 | Career | Job roles, interviews, next steps |

## 🎯 The Reference Project

Throughout this course, we build a **Customer Churn Prediction** system:

- **Business Problem**: Predict which customers will cancel their subscription
- **Data**: Customer demographics, usage patterns, support interactions
- **Model**: Classification (Logistic Regression, Random Forest, etc.)
- **Serving**: REST API for real-time predictions
- **Deployment**: Docker → Kubernetes
- **Monitoring**: Performance metrics, drift detection

This single project evolves from a simple notebook to a production-ready ML system.

## 🤝 Contributing

We welcome contributions! Please see our contribution guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Areas for Contribution

- Fix typos or improve explanations
- Add new lab exercises
- Create additional quiz questions
- Improve code examples
- Add diagrams and visualizations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact & Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: mlops-course@example.com

---

**⭐ If you find this course helpful, please give it a star!**

Happy Learning! 🎓
