# Lecture 2.3 – Setting Up Local Dev Environment

## In This Lecture You Will Learn

- [x] Install Python, Docker, and all required development tools
- [x] Configure your IDE for Python ML development
- [x] Verify your environment is ready for the course

---

## Real-World Context

> **Story**: A senior ML engineer once spent 2 days debugging why a colleague's model produced different results. The culprit? Python 3.7 vs 3.10 with a subtle pandas behavior change. Now their team has a strict "everyone uses the same versions" policy with Docker.
>
> Environment consistency isn't glamorous, but it prevents painful debugging sessions. Let's set you up right from the start.

A consistent environment means less "works on my machine" problems.

---

## Main Content

### 1. System Requirements

Before we start, verify your system meets these requirements:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MINIMUM REQUIREMENTS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  HARDWARE                                                        │
│  ─────────                                                       │
│  • RAM: 8GB minimum (16GB recommended)                          │
│  • Disk: 20GB free space                                        │
│  • CPU: Any modern processor (no GPU needed!)                   │
│                                                                  │
│  OPERATING SYSTEM                                                │
│  ────────────────                                                │
│  • macOS 10.15+ (Catalina or later)                            │
│  • Windows 10/11 with WSL2                                      │
│  • Linux (Ubuntu 20.04+ recommended)                            │
│                                                                  │
│  NETWORK                                                         │
│  ───────                                                         │
│  • Internet access for downloading packages                     │
│  • No VPN issues (or know how to configure proxy)              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Installation by Operating System

#### **macOS Installation**

```bash
# Step 1: Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Step 2: Install Python 3.10
brew install python@3.10

# Step 3: Install Git
brew install git

# Step 4: Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop/
# Or use Homebrew:
brew install --cask docker

# Step 5: Install VS Code (recommended IDE)
brew install --cask visual-studio-code

# Step 6: Verify installations
python3 --version    # Should show Python 3.10.x
git --version        # Should show git 2.x
docker --version     # Should show Docker 24.x or later
code --version       # Should show VS Code version
```

#### **Windows Installation (with WSL2)**

```powershell
# Step 1: Enable WSL2 (run PowerShell as Administrator)
wsl --install

# Restart your computer, then continue...

# Step 2: Install Ubuntu from Microsoft Store
# Search for "Ubuntu" and install Ubuntu 22.04 LTS

# Step 3: Open Ubuntu terminal and run:
sudo apt update && sudo apt upgrade -y
sudo apt install python3.10 python3.10-venv python3-pip git -y

# Step 4: Install Docker Desktop for Windows
# Download from: https://www.docker.com/products/docker-desktop/
# Enable WSL2 backend in Docker settings

# Step 5: Install VS Code for Windows
# Download from: https://code.visualstudio.com/
# Install "Remote - WSL" extension

# Step 6: Verify (in WSL Ubuntu terminal)
python3 --version
git --version
docker --version
```

#### **Linux (Ubuntu/Debian) Installation**

```bash
# Step 1: Update system
sudo apt update && sudo apt upgrade -y

# Step 2: Install Python 3.10
sudo apt install python3.10 python3.10-venv python3-pip -y

# Step 3: Install Git
sudo apt install git -y

# Step 4: Install Docker
# Remove old versions
sudo apt remove docker docker-engine docker.io containerd runc
# Install Docker
sudo apt install ca-certificates curl gnupg lsb-release -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# Add user to docker group (no sudo needed for docker commands)
sudo usermod -aG docker $USER
newgrp docker

# Step 5: Install VS Code
sudo snap install code --classic

# Step 6: Verify
python3 --version
git --version
docker --version
code --version
```

### 3. IDE Setup (VS Code)

VS Code with the right extensions makes Python development much smoother:

```
Essential Extensions:
═════════════════════

┌─────────────────────────────────────────────────────────────────┐
│  EXTENSION                  │  PURPOSE                          │
├─────────────────────────────────────────────────────────────────┤
│  Python (Microsoft)         │  Python language support          │
│  Pylance                    │  Fast, type-aware Python          │
│  Python Debugger            │  Debug Python code                │
│  Docker                     │  Docker file support              │
│  GitLens                    │  Enhanced Git features            │
│  YAML                       │  YAML file support                │
│  Jupyter                    │  Notebook support                 │
│  Remote - SSH               │  Remote development               │
│  Remote - WSL (Windows)     │  WSL integration                  │
└─────────────────────────────────────────────────────────────────┘
```

**Install via command line:**

```bash
# Install all recommended extensions
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
code --install-extension ms-azuretools.vscode-docker
code --install-extension eamodio.gitlens
code --install-extension redhat.vscode-yaml
code --install-extension ms-toolsai.jupyter
```

### 4. Python Virtual Environment Setup

Always use virtual environments for Python projects:

```bash
# Navigate to the project directory
cd project

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (CMD):
.\venv\Scripts\activate.bat

# Verify activation (should show venv path)
which python  # macOS/Linux
where python  # Windows

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### 5. Git Configuration

Set up Git with your identity:

```bash
# Configure your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name to 'main'
git config --global init.defaultBranch main

# Enable colored output
git config --global color.ui auto

# Set VS Code as default editor
git config --global core.editor "code --wait"

# Verify configuration
git config --list
```

---

## Diagrams

```
Development Environment Architecture:
═════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│                         YOUR LAPTOP                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                      VS CODE IDE                         │   │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│   │  │   Editor    │  │  Terminal   │  │  Debugger   │     │   │
│   │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                 VIRTUAL ENVIRONMENT                      │   │
│   │   Python 3.10 + pandas + scikit-learn + fastapi + ...  │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                      DOCKER                              │   │
│   │   ┌─────────┐  ┌─────────┐  ┌─────────┐               │   │
│   │   │ Model   │  │ MLflow  │  │ Tests   │               │   │
│   │   │ API     │  │ Server  │  │ Runner  │               │   │
│   │   └─────────┘  └─────────┘  └─────────┘               │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                       GIT                                │   │
│   │   Local Repo ←→ GitHub Remote                           │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Lab / Demo

### Prerequisites

- Completed Lectures 2.1 and 2.2
- Administrative access to your computer

### Step-by-Step Instructions

Complete environment setup and verification:

```bash
# Step 1: Clone the course repository
git clone https://github.com/yourusername/mlops-course.git
cd mlops-course/project

# Step 2: Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR: .\venv\Scripts\activate  # Windows

# Step 3: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Run the verification script
python -c "
import sys
print(f'Python: {sys.version}')

import pandas
print(f'pandas: {pandas.__version__}')

import sklearn
print(f'scikit-learn: {sklearn.__version__}')

import fastapi
print(f'FastAPI: {fastapi.__version__}')

import yaml
print(f'PyYAML: {yaml.__version__}')

print()
print('✅ All packages installed successfully!')
"

# Step 5: Run the project tests
PYTHONPATH=src pytest tests/ -v --tb=short

# Step 6: Verify Docker
docker run hello-world
```

### Expected Output

```
$ python -c "..."
Python: 3.10.8 (main, Oct 21 2022, 22:22:30)
pandas: 2.0.3
scikit-learn: 1.3.0
FastAPI: 0.103.1
PyYAML: 6.0.1

✅ All packages installed successfully!

$ pytest tests/ -v --tb=short
============================= test session starts ==============================
collected 15 items

tests/test_data.py::TestDataLoading::test_generate_sample_data PASSED
tests/test_data.py::TestDataLoading::test_validate_data PASSED
tests/test_models.py::TestChurnModel::test_init_random_forest PASSED
...
============================= 15 passed in 2.34s ================================

$ docker run hello-world
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### Explanation

1. **Clone**: Gets all course materials on your machine
2. **Virtual env**: Isolates project dependencies
3. **Install**: Gets all required Python packages
4. **Verify imports**: Confirms packages work correctly
5. **Run tests**: Confirms the project code works
6. **Docker check**: Confirms Docker is running

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Forgetting to activate the virtual environment. Always check your prompt shows `(venv)` before running pip or python commands.

- ⚠️ **Pitfall 2**: Docker not starting on Windows. Make sure WSL2 is enabled and Docker Desktop is configured to use the WSL2 backend.

- ⚠️ **Pitfall 3**: Permission errors on Linux with Docker. Make sure you added your user to the docker group and ran `newgrp docker`.

---

## Homework / Practice

1. **Exercise 1**: Run `pip list` and count how many packages are installed. Save this to a file: `pip list > installed_packages.txt`

2. **Exercise 2**: Open the project in VS Code. Use the Python extension to run a single test file (`tests/test_data.py`).

3. **Stretch Goal**: Create a simple "hello world" Docker container that prints Python's version.

---

## Quick Quiz

1. **Why do we use virtual environments?**
   - A) They make Python faster
   - B) They isolate project dependencies from system Python
   - C) They are required by Docker
   - D) They improve security

2. **What command activates a virtual environment on macOS/Linux?**
   - A) `venv activate`
   - B) `python -m venv activate`
   - C) `source venv/bin/activate`
   - D) `./venv/activate`

3. **True or False: You need a GPU to complete this course.**

<details>
<summary>Answers</summary>

1. **B** - Virtual environments isolate dependencies, preventing conflicts between projects
2. **C** - The `source` command runs the activate script
3. **False** - Everything runs on CPU; 8GB RAM is sufficient

</details>

---

## Summary

- Install Python 3.10+, Git, Docker, and VS Code
- Use virtual environments for every Python project
- VS Code extensions significantly improve productivity
- Configure Git with your name, email, and preferences
- Test your setup by running the project tests and Docker hello-world
- If something doesn't work, check Lecture 2.8 for troubleshooting

---

## Next Steps

→ Continue to **Lecture 2.4**: Project Structure for an MLOps Course Project

---

## Additional Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html) - Official Python docs
- [Docker Get Started](https://docs.docker.com/get-started/) - Docker installation and basics
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial) - IDE setup
- [Git Configuration](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) - Git setup guide
