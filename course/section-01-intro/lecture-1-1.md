# Lecture 1.1 – Course Welcome & How to Use This Course

## In This Lecture You Will Learn

- [x] Understand the structure and organization of this MLOps course
- [x] Know how to navigate the repository and course materials effectively
- [x] Set realistic expectations for what you'll build and learn

---

## Real-World Context

> **Story**: Meet Sarah, a data scientist at a mid-size e-commerce company. She's brilliant at building models in Jupyter notebooks—her churn prediction model achieved 92% accuracy! But when her manager asked, "Can we deploy this to production by Friday?", Sarah froze. She had no idea how to get her notebook from her laptop to a system that could serve predictions 24/7. Six months later, after multiple failed deployments, Sarah found an MLOps course. Within weeks, she understood not just *how* to deploy models, but *why* certain practices matter. That's exactly what this course will do for you.

In the real world, the gap between a working notebook and a production system is where most ML projects fail. This course bridges that gap.

---

## Main Content

### 1. Who Is This Course For?

This course is designed for:

| Background | What You'll Gain |
|------------|------------------|
| **Data Scientists** | Learn to deploy your own models without depending on engineering teams |
| **ML Engineers** | Formalize your practices and fill knowledge gaps |
| **DevOps Engineers** | Understand ML-specific deployment challenges |
| **Software Engineers** | Transition into the ML engineering space |
| **Career Changers** | Build a portfolio project that showcases end-to-end ML skills |

**Prerequisites (What You Need):**
- Basic Python programming (functions, classes, file I/O)
- Familiarity with ML concepts (training, testing, evaluation)
- Basic command line knowledge (cd, ls, running scripts)

**Not Required:**
- Advanced mathematics or statistics
- Prior Docker or Kubernetes experience
- Cloud certifications
- A PhD or formal ML education

### 2. Course Structure & Navigation

```
📁 Repository Structure
├── 📖 course/          ← You are here! 15 sections of lectures
│   ├── section-01-intro/
│   ├── section-02-setup/
│   └── ...
├── 🔧 project/         ← Hands-on code (Customer Churn Prediction)
├── 📊 infra/           ← CI/CD pipelines and Kubernetes configs
├── 📝 quizzes/         ← Test yourself after each section
├── 🎨 slides/          ← Presentation materials
└── 📷 assets/          ← Diagrams and images
```

**How to Progress Through the Course:**

1. **Watch/Read** - Each lecture file contains theory, stories, and explanations
2. **Practice** - Follow the lab exercises in each lecture
3. **Build** - Work on the project code alongside the lectures
4. **Quiz** - Test your understanding after each section
5. **Repeat** - Move to the next section

### 3. What We're Building Together

Throughout this course, we build a **Customer Churn Prediction System** from scratch:

```
📈 The Journey of Our Project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Week 1: Notebook → Scripts
        "I have a working model in Jupyter"
        
Week 2: Scripts → Package  
        "My code is organized and reusable"
        
Week 3: Package → API
        "My model can receive HTTP requests"
        
Week 4: API → Container → Deployment
        "My model runs in production 24/7"
        
Week 5: Deployment → Monitored System
        "I know when my model needs retraining"
```

**Business Context:**
- **Problem**: Predict which customers will cancel their subscription
- **Impact**: Save $2M/year by intervening with at-risk customers
- **Reality**: This exact use case exists in Netflix, Spotify, and thousands of SaaS companies

---

## Diagrams

```
┌─────────────────────────────────────────────────────────────────┐
│                    Course Learning Path                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📚 Foundation (Sections 1-3)                                   │
│  └──> What is MLOps? Why does it matter? Who does what?        │
│                                                                  │
│  🔬 Project & Data (Sections 4-6)                               │
│  └──> Our use case, data engineering, experiments              │
│                                                                  │
│  📦 Packaging (Sections 7-9)                                    │
│  └──> Python packages, APIs, Docker, pipelines                 │
│                                                                  │
│  🚀 Deployment (Sections 10-12)                                 │
│  └──> CI/CD, Kubernetes, monitoring                            │
│                                                                  │
│  🎯 Mastery (Sections 13-15)                                    │
│  └──> Governance, capstone, career prep                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Lab / Demo

### Prerequisites

- Git installed on your machine
- GitHub account (for cloning the repository)

### Step-by-Step Instructions

```bash
# Step 1: Clone the course repository
git clone https://github.com/yourusername/mlops-course.git
cd mlops-course

# Step 2: Explore the structure
ls -la
# You should see: course/, project/, infra/, quizzes/, slides/, assets/

# Step 3: Navigate to Section 1
cd course/section-01-intro
ls
# You should see: README.md, lecture-1-1.md, lecture-1-2.md, etc.

# Step 4: Preview the project we'll build
cd ../../project
ls
# You should see: src/, tests/, config/, Dockerfile, etc.
```

### Expected Output

```
$ ls -la
total 32
drwxr-xr-x  10 user  staff   320 Jan 15 10:30 .
drwxr-xr-x   5 user  staff   160 Jan 15 10:30 ..
drwxr-xr-x  13 user  staff   416 Jan 15 10:30 .git
-rw-r--r--   1 user  staff   245 Jan 15 10:30 .gitignore
-rw-r--r--   1 user  staff  8234 Jan 15 10:30 COURSE_OVERVIEW.md
-rw-r--r--   1 user  staff  5621 Jan 15 10:30 README.md
drwxr-xr-x  17 user  staff   544 Jan 15 10:30 course
drwxr-xr-x   4 user  staff   128 Jan 15 10:30 infra
drwxr-xr-x  12 user  staff   384 Jan 15 10:30 project
drwxr-xr-x  17 user  staff   544 Jan 15 10:30 quizzes
```

### Explanation

1. **Step 1**: Cloning gives you your own copy of all course materials
2. **Step 2**: Understanding the layout helps you navigate efficiently
3. **Step 3**: Section directories contain all lectures for that topic
4. **Step 4**: The project directory is where you'll write production code

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Skipping ahead too quickly. Each section builds on the previous one. If you skip Section 3 (ML Lifecycle), Section 9 (Pipelines) won't make sense.

- ⚠️ **Pitfall 2**: Just reading without doing. This course is hands-on. You'll learn 10x more by typing the commands than by just reading them.

- ⚠️ **Pitfall 3**: Trying to memorize everything. Focus on understanding *why* things work, not memorizing syntax. You can always look up commands later.

---

## Homework / Practice

1. **Exercise 1**: Clone the repository and explore each top-level directory. Write down what you find in each folder.

2. **Exercise 2**: Read the COURSE_OVERVIEW.md file completely. Identify which 3 sections you're most excited about learning.

3. **Stretch Goal**: Look at the project/src directory. Can you identify what each Python module might do based on its name? Write your guesses and check them against the README.

---

## Quick Quiz

1. **What is the primary focus of this course?**
   - A) Building the most accurate ML model possible
   - B) Learning advanced mathematics for ML
   - C) Taking ML models from notebooks to production systems
   - D) Becoming an expert in cloud platforms

2. **Where will you find the hands-on code for our project?**
   - A) `/course` directory
   - B) `/project` directory
   - C) `/quizzes` directory
   - D) `/slides` directory

3. **True or False: You need a PhD in Machine Learning to complete this course.**

<details>
<summary>Answers</summary>

1. **C** - The course focuses on operationalizing ML models
2. **B** - The `/project` directory contains all hands-on code
3. **False** - Basic Python and ML familiarity is sufficient

</details>

---

## Summary

- This course takes you from notebook to production in 15 comprehensive sections
- We build a real Customer Churn Prediction system together
- The repository is organized into course materials, project code, infrastructure, quizzes, and slides
- You'll learn best by doing—follow along with every lab exercise
- No advanced prerequisites required—just Python basics and ML familiarity

---

## Next Steps

→ Continue to **Lecture 1.2**: What Is MLOps? In One Story, Not a Definition

---

## Additional Resources

- [COURSE_OVERVIEW.md](../../COURSE_OVERVIEW.md) - Complete syllabus and learning objectives
- [project/README.md](../../project/README.md) - Project setup instructions
- [Google's MLOps Whitepaper](https://cloud.google.com/resources/mlops-whitepaper) - Industry perspective on MLOps
