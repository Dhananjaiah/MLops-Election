# Lecture 2.6 – Git Basics for MLOps (Branching, PRs, Tags)

## In This Lecture You Will Learn

- [x] Master Git workflows essential for MLOps collaboration
- [x] Understand branching strategies for ML projects
- [x] Use tags for model versioning and releases

---

## Real-World Context

> **Story**: A team of data scientists all worked on the `main` branch. One day, someone committed broken code that trained a model with the wrong data. By the time they realized it, three other people had pulled the changes and wasted hours debugging. Their manager instituted a branching strategy: "No direct commits to main. All changes via pull requests with reviews."
>
> Git isn't just for backing up code—it's essential for team collaboration and preventing disasters.

In real ML teams, proper Git workflows are as important as writing good code.

---

## Main Content

### 1. Git Basics Refresher

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ESSENTIAL GIT CONCEPTS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  WORKING DIRECTORY                                                          │
│  ─────────────────                                                          │
│  • Your actual files on disk                                                │
│  • Where you edit code                                                      │
│                                                                              │
│  STAGING AREA (INDEX)                                                       │
│  ─────────────────────                                                      │
│  • Files marked for next commit                                             │
│  • Use: git add <file>                                                      │
│                                                                              │
│  LOCAL REPOSITORY                                                           │
│  ─────────────────                                                          │
│  • Committed snapshots of your project                                      │
│  • Use: git commit -m "message"                                             │
│                                                                              │
│  REMOTE REPOSITORY                                                          │
│  ──────────────────                                                         │
│  • Shared repository on GitHub/GitLab                                       │
│  • Use: git push / git pull                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Essential Git Commands:**

```bash
# Initial Setup (one-time)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Daily Workflow
git status              # Check what's changed
git add <file>          # Stage files
git add .               # Stage all changes
git commit -m "msg"     # Commit with message
git push                # Push to remote
git pull                # Pull latest changes

# Viewing History
git log                 # View commit history
git log --oneline       # Condensed view
git show <commit>       # View specific commit
git diff                # See unstaged changes
```

### 2. Branching Strategies for MLOps

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GITFLOW FOR ML PROJECTS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  main                  →  ●────●────●────●────●  (Production)              │
│                               ↑    ↑                                        │
│                               │    │                                        │
│  staging              ●───────●────●────●  (Pre-production testing)        │
│                       │       ↑    ↑                                        │
│                       │       │    │                                        │
│  feature/churn-v2    ●───●───●    │  (New features)                       │
│                                    │                                        │
│  feature/api-update      ●────●───●  (Another feature)                     │
│                                                                              │
│  hotfix/bug-123              ●───●  (Emergency fixes)                      │
│                               ↓                                             │
│  main                  →  ●───●  (Fixed in production)                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Branch Types:**

| Branch Type | Purpose | Naming Convention | Lifetime |
|-------------|---------|------------------|----------|
| `main` | Production-ready code | `main` | Permanent |
| `develop` | Integration branch | `develop` | Permanent |
| `feature/*` | New features/experiments | `feature/churn-model-v2` | Temporary |
| `experiment/*` | ML experiments | `experiment/xgboost-tuning` | Temporary |
| `hotfix/*` | Emergency production fixes | `hotfix/memory-leak` | Temporary |
| `release/*` | Release preparation | `release/v1.2.0` | Temporary |

**For our course, we use a simplified strategy:**
- `main` branch: Always deployable
- `feature/*` branches: For new work
- No `develop` branch (keeping it simple)

### 3. Working with Branches

```bash
# Create and switch to new branch
git checkout -b feature/new-model

# List all branches
git branch -a

# Switch between branches
git checkout main
git checkout feature/new-model

# Push branch to remote
git push -u origin feature/new-model

# Delete branch (after merging)
git branch -d feature/new-model          # Local
git push origin --delete feature/new-model  # Remote

# Merge branch
git checkout main
git merge feature/new-model
```

### 4. Pull Requests (PRs) for Code Review

**Good PR Practices:**

✅ **DO:**
- Keep PRs small (< 400 lines when possible)
- Write descriptive titles and descriptions
- Reference related issues
- Include tests for new features
- Update documentation

❌ **DON'T:**
- Mix multiple unrelated changes
- Commit large binary files
- Push secrets or credentials
- Merge without review
- Leave unresolved comments

### 5. Git Tags for Model Versioning

```bash
# Create an annotated tag (preferred)
git tag -a v1.2.0 -m "Churn model with 94% accuracy"

# List tags
git tag

# Show tag details
git show v1.2.0

# Push tags to remote
git push origin v1.2.0       # Single tag
git push origin --tags       # All tags

# Checkout a specific tag
git checkout v1.2.0

# Delete a tag
git tag -d v1.2.0           # Local
```

**Semantic Versioning for ML Models:**

```
v MAJOR . MINOR . PATCH

v1.2.3
 │ │ │
 │ │ └─ PATCH: Bug fixes, hotfixes (no model change)
 │ └─── MINOR: Model retraining, feature updates
 └───── MAJOR: Complete model architecture change
```

### 6. .gitignore for ML Projects

```gitignore
# Python
__pycache__/
*.py[cod]
venv/
env/

# Jupyter
.ipynb_checkpoints

# ML Specific
data/               # Large datasets
*.csv
models/*.pkl       # Trained models
mlruns/            # MLflow tracking

# OS
.DS_Store

# Secrets
.env
*.key
```

---

## Diagrams

```
Git Workflow for MLOps:
═══════════════════════

Developer              GitHub                   Production
    │                     │                          │
    ├─ feature/v2         │                          │
    │  ├─ commit          │                          │
    │  └─ push ──────────▶│                          │
    │                     │                          │
    │      ◀── PR review ─┤                          │
    │                     │                          │
    │      ── approve ───▶│                          │
    │                     │                          │
    │                  merge to main                 │
    │                     ├─ tag v1.1.0              │
    │                     │                          │
    │                     └─ CI/CD ────────────────▶ Deploy
```

---

## Lab / Demo

### Prerequisites

- Completed Lecture 2.5
- Git installed and configured
- GitHub account

### Step-by-Step Instructions

```bash
# Step 1: Clone the course repository
git clone https://github.com/yourusername/mlops-course.git
cd mlops-course

# Step 2: Create a new feature branch
git checkout -b feature/my-first-feature

# Step 3: Make a change (edit README.md)
echo "
## My Notes" >> README.md

# Step 4: Check status
git status

# Step 5: Stage and commit
git add README.md
git commit -m "Add my notes section to README"

# Step 6: Push to remote
git push -u origin feature/my-first-feature

# Step 7: Create tag
git tag -a v0.1.0 -m "My first tagged version"
git push origin v0.1.0

# Step 8: Switch back to main
git checkout main

# Step 9: View your branch
git branch -a
```

### Expected Output

```
$ git checkout -b feature/my-first-feature
Switched to a new branch 'feature/my-first-feature'

$ git status
On branch feature/my-first-feature
Changes not staged for commit:
  modified:   README.md

$ git commit -m "Add my notes section to README"
[feature/my-first-feature abc1234] Add my notes section to README
 1 file changed, 2 insertions(+)

$ git push -u origin feature/my-first-feature
To https://github.com/yourusername/mlops-course.git
 * [new branch]      feature/my-first-feature -> feature/my-first-feature
```

### Explanation

1. **Steps 1-2**: Create an isolated branch for your changes
2. **Steps 3-5**: Make changes, stage, and commit them
3. **Step 6**: Push your branch to GitHub (enables PR creation)
4. **Steps 7**: Tag important versions for easy reference
5. **Steps 8-9**: Switch between branches to work on different tasks

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Committing directly to `main`. Always work on feature branches and use PRs for main.

- ⚠️ **Pitfall 2**: Forgetting to pull before starting work. Always `git pull` to get latest changes.

- ⚠️ **Pitfall 3**: Committing large model files. Use Git LFS or DVC for large binary files.

---

## Homework / Practice

1. **Exercise 1**: Create a branch, make 3 commits, push it, then merge it back to main using GitHub PR interface.

2. **Exercise 2**: Practice merge conflicts: Create two branches that modify the same line, then try to merge them.

3. **Stretch Goal**: Set up a pre-commit hook that runs `black` formatter before every commit.

---

## Quick Quiz

1. **What's the purpose of feature branches?**
   - A) To backup your code
   - B) To isolate new work from production code
   - C) To make Git faster
   - D) They're optional

2. **What does semantic versioning v2.1.3 mean?**
   - A) 2nd major version, 1st minor update, 3rd patch
   - B) Released on 2021-03
   - C) 2 features, 1 bug fix, 3 tests
   - D) Random numbers

3. **True or False: You should commit the venv folder to Git.**

<details>
<summary>Answers</summary>

1. **B** - Feature branches keep experimental work separate from stable code
2. **A** - Semantic versioning: MAJOR.MINOR.PATCH
3. **False** - venv folders are environment-specific and shouldn't be versioned

</details>

---

## Summary

- Git enables team collaboration and version control for ML projects
- Use feature branches for all new work, never commit directly to main
- Pull Requests enable code review before merging
- Tags mark important versions (model releases)
- .gitignore prevents committing large files and secrets
- Semantic versioning helps track model evolution

---

## Next Steps

→ Continue to **Lecture 2.7**: Running Labs on a Normal / Corporate Laptop (No Fancy GPU Needed)

---

## Additional Resources

- [Git Documentation](https://git-scm.com/doc) - Official Git reference
- [GitHub Flow](https://guides.github.com/introduction/flow/) - Simple branching strategy
- [Semantic Versioning](https://semver.org/) - Version numbering spec
- [Oh Shit, Git!?!](https://ohshitgit.com/) - Common Git problems and solutions
