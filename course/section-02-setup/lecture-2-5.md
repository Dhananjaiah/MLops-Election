# Lecture 2.5 – Installing Required Python Packages & Virtual Environments

## In This Lecture You Will Learn

- [x] Master Python virtual environments for isolated dependency management
- [x] Install and manage project dependencies using requirements.txt and pip
- [x] Understand dependency versioning and reproducibility

---

## Real-World Context

> **Story**: A data scientist joined a new team and ran `pip install` globally for a project. Two weeks later, another project broke because incompatible package versions were installed. The team spent a full day fixing broken environments across 5 engineers' laptops. Their tech lead instituted a rule: "No global pip installs. Virtual environments for everything."
>
> Virtual environments aren't just best practice—they're essential for maintaining your sanity when working on multiple projects.

In the real world, dependency conflicts are one of the most common causes of "it works on my machine" problems.

---

## Main Content

### 1. Why Virtual Environments Matter

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THE DEPENDENCY HELL PROBLEM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  WITHOUT VIRTUAL ENVIRONMENTS:                                              │
│  ────────────────────────────                                               │
│  System Python                                                              │
│  └── pandas 1.5.0  ← Project A needs this                                  │
│  └── pandas 2.0.0  ← Project B needs this (CONFLICT!)                      │
│  └── scikit-learn 1.3.0                                                     │
│  └── [hundreds of other packages...]                                        │
│                                                                              │
│  Problems:                                                                  │
│  • Only one version of each package can be installed                        │
│  • Upgrading for one project breaks another                                │
│  • Hard to track which project needs what                                   │
│  • Difficult to reproduce on another machine                                │
│                                                                              │
│  WITH VIRTUAL ENVIRONMENTS:                                                 │
│  ─────────────────────────                                                  │
│  System Python (clean)                                                      │
│  │                                                                           │
│  ├── venv_project_a/                                                        │
│  │   └── pandas 1.5.0                                                       │
│  │   └── scikit-learn 1.2.0                                                 │
│  │                                                                           │
│  └── venv_project_b/                                                        │
│      └── pandas 2.0.0                                                       │
│      └── scikit-learn 1.3.0                                                 │
│                                                                              │
│  Benefits:                                                                  │
│  ✅ Complete isolation between projects                                     │
│  ✅ Each project has exactly what it needs                                  │
│  ✅ Easy to delete and recreate environments                                │
│  ✅ Reproducible with requirements.txt                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Creating and Managing Virtual Environments

#### **Method 1: Using venv (Built-in, Recommended)**

```bash
# Create a new virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# When activated, your prompt changes:
(venv) user@machine:~/project$

# Deactivate when done
deactivate
```

#### **Method 2: Using virtualenv (Third-party)**

```bash
# Install virtualenv first
pip install virtualenv

# Create environment
virtualenv venv

# Same activation commands as above
```

#### **Method 3: Using conda (For Data Science)**

```bash
# Create environment with specific Python version
conda create -n mlops-env python=3.10

# Activate
conda activate mlops-env

# Deactivate
conda deactivate
```

**For this course, we use `venv` (Method 1) because:**
- Built into Python 3.3+, no installation needed
- Simple and lightweight
- Works identically across all platforms
- Industry standard for Python projects

### 3. Installing Packages with pip

#### **The Project Requirements File**

Every Python project should have a `requirements.txt`:

```txt
# Core ML and Data
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0

# API and Web
fastapi==0.103.1
uvicorn[standard]==0.23.2
pydantic==2.3.0

# Testing
pytest==7.4.0
pytest-cov==4.1.0

# Development tools
black==23.7.0
pylint==2.17.5
ipython==8.14.0
```

**Installing from requirements.txt:**

```bash
# Activate your virtual environment first!
source venv/bin/activate

# Install all packages
pip install -r requirements.txt

# Verify installation
pip list
```

#### **Adding New Packages**

```bash
# Install a new package
pip install requests

# Add it to requirements.txt (with version)
pip freeze | grep requests >> requirements.txt

# Or manually edit requirements.txt
echo "requests==2.31.0" >> requirements.txt
```

### 4. Dependency Version Management

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VERSION PINNING STRATEGIES                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  EXACT PINNING (Most Reproducible):                                         │
│  ───────────────────────────────                                            │
│  pandas==2.0.3                                                              │
│  • Guarantees exact same version everywhere                                 │
│  • Use for production deployments                                           │
│  • Can miss important security patches                                      │
│                                                                              │
│  COMPATIBLE RELEASE (Flexible):                                             │
│  ──────────────────────────────                                             │
│  pandas~=2.0.0                                                              │
│  • Allows 2.0.1, 2.0.2, etc., but not 2.1.0                                │
│  • Gets bug fixes automatically                                             │
│  • Recommended for most projects                                            │
│                                                                              │
│  MINIMUM VERSION (Risky):                                                   │
│  ────────────────────────                                                   │
│  pandas>=2.0.0                                                              │
│  • Allows any version 2.0.0 or higher                                       │
│  • Can break unexpectedly with major updates                                │
│  • Avoid in production                                                      │
│                                                                              │
│  RANGE (Constrained Flexibility):                                           │
│  ────────────────────────────────                                           │
│  pandas>=2.0.0,<3.0.0                                                       │
│  • Allows 2.x versions but not 3.x                                          │
│  • Good for libraries with semantic versioning                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5. Our Course Project Setup

For our MLOps course project, we use this dependency structure:

```bash
project/
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development/testing tools
└── requirements-docs.txt     # Documentation tools (optional)
```

**Why separate files?**
- Production containers don't need pytest or jupyter
- Smaller Docker images = faster deployment
- Clear separation of concerns

---

## Diagrams

```
Virtual Environment Workflow:
═════════════════════════════

START PROJECT
     │
     ▼
Create venv
(python3 -m venv venv)
     │
     ▼
Activate venv
(source venv/bin/activate)
     │
     ▼
Install dependencies
(pip install -r requirements.txt)
     │
     ├──────────────────┐
     │                  │
     ▼                  ▼
Work on code      Add new packages
     │            (pip install <package>)
     │                  │
     │                  ▼
     │            Update requirements.txt
     │            (pip freeze > requirements.txt)
     │                  │
     └──────────────────┘
     │
     ▼
Deactivate when done
(deactivate)


Package Installation Flow:
══════════════════════════

requirements.txt
     │
     │ pip install -r requirements.txt
     ▼
Download from PyPI
     │
     ▼
Install in venv/lib/python3.10/site-packages/
     │
     ▼
Available for import in your code
     │
     ▼
Use: import pandas as pd
```


---

## Lab / Demo

### Prerequisites

- Completed Lecture 2.3 (environment setup)
- Python 3.9+ installed
- Terminal access

### Step-by-Step Instructions

```bash
# Step 1: Navigate to the course project
cd ~/mlops-course/project

# Step 2: Create a virtual environment
python3 -m venv venv

# Step 3: Verify the environment was created
ls -la venv/
# You should see: bin/, lib/, include/, pyvenv.cfg

# Step 4: Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 5: Verify activation (pip should point to venv)
which pip
# Should show: /path/to/project/venv/bin/pip

# Step 6: Upgrade pip to latest version
pip install --upgrade pip

# Step 7: Install project dependencies
pip install -r requirements.txt

# Step 8: Verify installations
pip list
# Should show all installed packages

# Step 9: Test that packages work
python -c "import pandas; import numpy; import fastapi; print('✅ All packages work!')"

# Step 10: Save current environment state
pip freeze > requirements-lock.txt
# This creates an exact snapshot of all versions
```

### Expected Output

```
$ python3 -m venv venv
# (No output means success)

$ source venv/bin/activate
(venv) $

$ which pip
/Users/yourname/mlops-course/project/venv/bin/pip

$ pip install -r requirements.txt
Collecting pandas==2.0.3
  Downloading pandas-2.0.3-cp310-cp310-macosx_11_0_arm64.whl (11.0 MB)
...
Successfully installed pandas-2.0.3 numpy-1.24.3 ...

$ pip list
Package         Version
--------------- ---------
pandas          2.0.3
numpy           1.24.3
scikit-learn    1.3.0
...

$ python -c "import pandas; print('✅ All packages work!')"
✅ All packages work!
```

### Explanation

1. **Step 1-2**: Creates an isolated Python environment in the `venv` directory
2. **Step 3**: The venv folder contains its own Python interpreter and package directory
3. **Step 4-5**: Activation modifies PATH so `python` and `pip` point to the virtual environment
4. **Step 6**: Ensures pip is up-to-date (old pip versions can have compatibility issues)
5. **Step 7**: Installs all dependencies specified in requirements.txt
6. **Step 9**: Quick sanity check that imports work
7. **Step 10**: Creates a snapshot for exact reproducibility

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Forgetting to activate the environment. Always check your prompt shows `(venv)`. Run `which python` to verify.

- ⚠️ **Pitfall 2**: Installing packages before activating venv. This installs globally, defeating the purpose. Always activate first!

- ⚠️ **Pitfall 3**: Committing the `venv` folder to Git. Add `venv/` to `.gitignore`. The venv folder can be recreated from requirements.txt.

- ⚠️ **Pitfall 4**: Using `pip freeze` with too many packages. Use `pipreqs` to generate requirements.txt from actual imports in your code.

---

## Homework / Practice

1. **Exercise 1**: Create two separate virtual environments for two different projects. Install different versions of pandas in each. Verify they don't interfere.

2. **Exercise 2**: Take an existing Python script you've written. Create a requirements.txt for it by:
   - Creating a venv
   - Installing packages manually as you import them
   - Running `pip freeze > requirements.txt`

3. **Stretch Goal**: Research and experiment with `pip-tools` for dependency management. Try `pip-compile` to generate a lock file from requirements.in.

---

## Quick Quiz

1. **What command creates a virtual environment?**
   - A) `pip install venv`
   - B) `python3 -m venv venv`
   - C) `virtualenv create venv`
   - D) `python3 --venv venv`

2. **Why use exact version pinning (==) in requirements.txt?**
   - A) It makes pip install faster
   - B) It ensures reproducible builds with exact same dependencies
   - C) It's required by Python
   - D) It reduces package size

3. **True or False: You should commit the venv folder to Git.**

<details>
<summary>Answers</summary>

1. **B** - `python3 -m venv venv` creates a new virtual environment
2. **B** - Exact versions ensure everyone uses the same dependencies
3. **False** - venv folders are large and machine-specific. Use requirements.txt instead

</details>

---

## Summary

- Virtual environments isolate project dependencies, preventing conflicts
- Use `python3 -m venv venv` to create, `source venv/bin/activate` to activate
- `requirements.txt` lists project dependencies with versions
- Use exact pinning (==) for production, compatible release (~=) for flexibility
- Always activate before installing packages, never commit venv to Git
- Separate production and development requirements for cleaner deployments

---

## Next Steps

→ Continue to **Lecture 2.6**: Git Basics for MLOps (Branching, PRs, Tags)

---

## Additional Resources

- [Python venv Documentation](https://docs.python.org/3/library/venv.html) - Official virtual environment guide
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/) - Package installation reference
- [pip-tools](https://github.com/jazzband/pip-tools) - Advanced dependency management
- [Python Packaging Guide](https://packaging.python.org/) - Comprehensive packaging docs

