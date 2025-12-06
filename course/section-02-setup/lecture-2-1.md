# Lecture 2.1 – Skills You Need (and Don't Need) Before Starting

## In This Lecture You Will Learn

- [x] Assess your current skill level against course prerequisites
- [x] Identify specific gaps you need to fill (and how to fill them)
- [x] Understand what you DON'T need, so you don't waste time

---

## Real-World Context

> **Story**: Maria was a marketing analyst who wanted to transition into ML. She spent 6 months studying calculus, linear algebra, and probability theory—because "that's what you need for ML." When she finally started learning applied ML, she realized she'd only needed 10% of that math. She wished someone had told her: "Here's exactly what you need, nothing more."
>
> This lecture is that guidance. We'll tell you exactly what skills you need (and don't need) to succeed in this course.

Don't over-prepare. Let's calibrate your starting point.

---

## Main Content

### 1. The Honest Prerequisites Assessment

Let's be clear about what this course requires:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PREREQUISITE SKILL MATRIX                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ✅ REQUIRED (Must Have)                                                    │
│  ───────────────────────                                                    │
│  • Python basics (functions, classes, file I/O, pip)                        │
│  • Basic command line (cd, ls, running scripts)                             │
│  • Understanding of what ML is (training, testing, predictions)             │
│                                                                              │
│  📈 HELPFUL (Nice to Have)                                                  │
│  ────────────────────────                                                   │
│  • Git basics (clone, commit, push)                                         │
│  • Basic SQL                                                                │
│  • Some exposure to pandas/NumPy                                            │
│  • Have seen a Jupyter notebook before                                      │
│                                                                              │
│  🚫 NOT REQUIRED (Don't Worry About)                                        │
│  ─────────────────────────────────                                          │
│  • Deep learning / neural networks                                          │
│  • Advanced statistics or mathematics                                       │
│  • Cloud certifications                                                     │
│  • Prior Docker or Kubernetes experience                                    │
│  • DevOps background                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Self-Assessment Checklist

Rate yourself on each skill: ✅ Confident | ⚠️ Need Review | ❌ Never Done

#### **Python (Required)**

| Skill | Example | Your Rating |
|-------|---------|-------------|
| Variables & Data Types | `x = 5`, `name = "Alice"`, `items = [1,2,3]` | ⬜ |
| Functions | `def calculate(x, y): return x + y` | ⬜ |
| Classes | `class Dog: def bark(self): ...` | ⬜ |
| File I/O | `with open('file.txt') as f: data = f.read()` | ⬜ |
| pip/packages | `pip install pandas`, `import pandas as pd` | ⬜ |
| Error handling | `try: ... except Exception as e: ...` | ⬜ |
| Dictionaries | `config = {"name": "model", "version": 1}` | ⬜ |

**If you have 5+ ✅:** You're ready!
**If you have 3-4 ✅:** Spend a few hours reviewing basics.
**If you have <3 ✅:** Take a Python crash course first (see resources).

#### **Command Line (Required)**

| Skill | Example | Your Rating |
|-------|---------|-------------|
| Navigate directories | `cd project`, `cd ..`, `pwd` | ⬜ |
| List files | `ls`, `ls -la` | ⬜ |
| Run Python scripts | `python script.py` | ⬜ |
| Environment variables | `export API_KEY=xxx`, `echo $PATH` | ⬜ |
| Pipes and redirection | `cat file.txt \| grep "error"` | ⬜ |

**If you have 3+ ✅:** You're good!
**If you have <3 ✅:** Practice basic terminal commands.

#### **ML Concepts (Required Understanding, Not Implementation)**

| Concept | What You Should Know | Your Rating |
|---------|---------------------|-------------|
| Training vs Testing | Data is split; model learns on training, evaluated on test | ⬜ |
| Features & Labels | Features = inputs, Labels = what we predict | ⬜ |
| Overfitting | Model memorizes training data, fails on new data | ⬜ |
| Classification vs Regression | Categories vs continuous numbers | ⬜ |
| Model evaluation | Accuracy, precision, recall (basic awareness) | ⬜ |

**If you have 3+ ✅:** You understand enough!
**If you have <3 ✅:** Watch a 1-hour ML intro video.

### 3. What You DON'T Need (Stop Worrying!)

Let's explicitly clear some anxiety:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THINGS YOU DON'T NEED FOR THIS COURSE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ❌ ADVANCED MATH                                                           │
│     • No calculus, no linear algebra, no probability theory                 │
│     • We use libraries that handle math internally                          │
│     • If you know what a "mean" is, you're fine                            │
│                                                                              │
│  ❌ DEEP LEARNING                                                           │
│     • No TensorFlow, PyTorch, or neural networks required                   │
│     • We use scikit-learn (simple, interpretable models)                    │
│     • Deep learning is a separate skill you can add later                   │
│                                                                              │
│  ❌ CLOUD CERTIFICATIONS                                                    │
│     • No AWS/GCP/Azure certification needed                                 │
│     • We run everything locally first                                       │
│     • Cloud deployment is optional/bonus material                           │
│                                                                              │
│  ❌ DEVOPS EXPERTISE                                                        │
│     • No prior Docker or Kubernetes experience needed                       │
│     • We teach Docker from scratch                                          │
│     • Kubernetes sections explain everything step-by-step                   │
│                                                                              │
│  ❌ A POWERFUL COMPUTER                                                     │
│     • 8GB RAM is enough                                                     │
│     • No GPU required                                                       │
│     • Works on Mac, Windows, or Linux                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. Filling the Gaps (If You Need To)

If your self-assessment revealed gaps, here's exactly what to study:

#### **Python Gap? (3-5 hours)**
- Free: [Python for Everybody](https://www.py4e.com/) (Chapters 1-10)
- Focus on: Functions, classes, file handling, dictionaries

#### **Command Line Gap? (1-2 hours)**
- Free: [Learn the Command Line](https://www.codecademy.com/learn/learn-the-command-line)
- Focus on: Navigation, running scripts, basic file operations

#### **ML Concepts Gap? (2-3 hours)**
- Free: [StatQuest ML Fundamentals](https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF)
- Focus on: What ML is, training/testing split, overfitting

#### **Git Gap? (2-3 hours)**
- Free: [Git Tutorial for Beginners](https://www.atlassian.com/git/tutorials)
- Focus on: clone, add, commit, push, pull, branches

---

## Diagrams

```
Skill Level Visualization:
══════════════════════════

                     EXPERT
                        │
                    ┌───┴───┐
                    │ BONUS │  ← Optional for this course
                    │ ZONE  │    (Deep learning, advanced infra)
                    └───┬───┘
                        │
              ┌─────────┴─────────┐
              │  COURSE TEACHES   │  ← We'll teach you this!
              │  Docker, K8s, CI/ │    (All MLOps content)
              │  CD, Monitoring   │
              └─────────┬─────────┘
                        │
              ┌─────────┴─────────┐
        ✅ →  │   YOU START HERE  │  ← Python, CLI, ML basics
              │   (Prerequisites) │
              └─────────┬─────────┘
                        │
                    BEGINNER

    You don't need to be an expert to start!
    We build on basic skills systematically.
```

---

## Lab / Demo

### Prerequisites

- Computer with internet access
- 15 minutes for self-assessment

### Step-by-Step Instructions

Complete this hands-on skill check:

```bash
# Step 1: Check Python installation
python --version
# Expected: Python 3.9 or higher

# Step 2: Check pip works
pip --version
# Expected: pip 21.x or higher

# Step 3: Run a simple Python script
python -c "
def greet(name):
    return f'Hello, {name}!'

class Student:
    def __init__(self, name):
        self.name = name
    def introduce(self):
        return greet(self.name)

s = Student('MLOps Learner')
print(s.introduce())
"
# Expected: Hello, MLOps Learner!

# Step 4: Check command line navigation
pwd          # Print working directory
ls           # List files
cd /tmp      # Change directory
cd -         # Go back

# Step 5: Check Git (optional but helpful)
git --version
# Expected: git version 2.x or higher
```

### Expected Output

```
$ python --version
Python 3.10.8

$ pip --version
pip 23.0.1 from /usr/local/lib/python3.10/site-packages

$ python -c "..."
Hello, MLOps Learner!

$ git --version
git version 2.39.0
```

### Explanation

1. **Python check**: We need Python 3.9+ for modern features
2. **pip check**: We'll install many packages throughout the course
3. **Python script**: Tests functions, classes, f-strings—core concepts
4. **CLI check**: You'll navigate directories constantly
5. **Git check**: Version control is fundamental (we'll teach more in 2.6)

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Over-preparing. Don't spend 3 months studying prerequisites. If you pass the self-assessment, start the course. You'll learn more by doing.

- ⚠️ **Pitfall 2**: Imposter syndrome. "Everyone else must know more than me." False. The skill range in ML is huge; you're in the right place.

- ⚠️ **Pitfall 3**: Thinking you need a CS degree. You don't. Many successful MLOps engineers came from biology, physics, economics, or self-study.

---

## Homework / Practice

1. **Exercise 1**: Complete the self-assessment checklist above. Count your ✅, ⚠️, and ❌ marks. Write down your total for each section.

2. **Exercise 2**: If you have any ❌ marks in the "Required" sections, spend 2-3 hours this week filling that specific gap using the resources provided.

3. **Stretch Goal**: Write a simple Python script that:
   - Defines a class `Customer` with `name` and `tenure` attributes
   - Has a method `is_loyal()` that returns `True` if tenure > 24
   - Saves customer data to a JSON file

---

## Quick Quiz

1. **Which of these is REQUIRED for this course?**
   - A) TensorFlow experience
   - B) AWS certification
   - C) Python basics (functions, classes)
   - D) Kubernetes production experience

2. **What's the minimum Python version needed?**
   - A) Python 2.7
   - B) Python 3.6
   - C) Python 3.9+
   - D) Python 4.0

3. **True or False: You need a GPU to complete this course.**

<details>
<summary>Answers</summary>

1. **C** - Python basics are the core prerequisite
2. **C** - Python 3.9+ gives us modern features we'll use
3. **False** - Everything runs on CPU; 8GB RAM is sufficient

</details>

---

## Summary

- Required: Python basics, command line basics, ML concept awareness
- Helpful: Git, SQL, pandas—but we'll teach/review as needed
- NOT required: Advanced math, deep learning, cloud certs, DevOps background
- Use the self-assessment to identify specific gaps
- Fill gaps with targeted 2-3 hour resources, not months of study
- Start the course when you pass the basic Python and CLI checks

---

## Next Steps

→ Continue to **Lecture 2.2**: Tech Stack Overview (Python, Git, Docker, CI/CD, Cloud/Kubernetes)

---

## Additional Resources

- [Python for Everybody](https://www.py4e.com/) - Comprehensive Python basics
- [The Missing Semester](https://missing.csail.mit.edu/) - Command line and developer tools
- [StatQuest ML Playlist](https://www.youtube.com/c/joshstarmer) - ML concepts explained simply
- [Git Tutorial](https://www.atlassian.com/git/tutorials) - Version control fundamentals
