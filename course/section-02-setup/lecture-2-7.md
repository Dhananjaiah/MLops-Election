# Lecture 2.7 – Running Labs on a Normal / Corporate Laptop (No Fancy GPU Needed)

## In This Lecture You Will Learn

- [x] Understand why GPUs aren't necessary for learning MLOps
- [x] Configure your laptop for efficient ML development
- [x] Know when to scale up to cloud resources

---

## Real-World Context

> **Story**: Emma worried she couldn't take this course—her laptop was a 4-year-old ThinkPad with 8GB RAM, no GPU. She'd seen job postings requiring 'high-performance computing' and assumed MLOps needed expensive hardware. Then she learned that 90% of MLOps is about processes, not computation. Her laptop was perfect.
>
> MLOps is about systems and workflows, not just raw compute power.

Most MLOps work happens on regular laptops. The expensive hardware comes later, in production.

---

## Main Content

### 1. Why You Don't Need a GPU for This Course

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MLOPS VS DEEP LEARNING REQUIREMENTS                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  DEEP LEARNING TRAINING:                                                    │
│  ───────────────────────                                                    │
│  • Trains large neural networks                                             │
│  • Processes millions of images/text                                        │
│  • GPU essential (10-100x faster)                                           │
│  • Requires 16GB+ RAM, CUDA-enabled GPU                                     │
│  • Example: Training ResNet on ImageNet                                     │
│                                                                              │
│  THIS MLOPS COURSE:                                                         │
│  ──────────────────                                                         │
│  • Uses small datasets (10K-100K rows)                                      │
│  • Traditional ML (scikit-learn, not deep learning)                         │
│  • CPU is sufficient                                                        │
│  • Requires 8GB RAM, any modern processor                                   │
│  • Example: Logistic regression on churn data                               │
│                                                                              │
│  FOCUS IS ON:                                                               │
│  ────────────                                                               │
│  ✅ Building pipelines, not training huge models                            │
│  ✅ Docker, Git, CI/CD—all CPU tasks                                        │
│  ✅ API development and deployment                                          │
│  ✅ Monitoring and system design                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Minimum vs Recommended Specifications

| Component | Minimum | Recommended | Why |
|-----------|---------|-------------|-----|
| **CPU** | Any dual-core | Quad-core i5/Ryzen 5 | Faster builds |
| **RAM** | 8GB | 16GB | Run Docker + IDE comfortably |
| **Disk** | 20GB free | 50GB SSD | Fast builds, caching |
| **OS** | Mac/Win/Linux | Any | All tools work on all platforms |
| **GPU** | Not needed | Not needed | We use CPU-only models |

**Your laptop is probably fine if it:**
- Was made in the last 5 years
- Can run a modern web browser smoothly
- Has 8GB+ RAM

### 3. Optimizing for Limited Resources

#### **If You Have 8GB RAM:**

```bash
# Limit Docker memory
# In Docker Desktop settings: Resources → Memory → Set to 4GB

# Use slim Python images
FROM python:3.10-slim  # Not python:3.10 (half the size)

# Don't run everything at once
# Close IDE when running Docker, or vice versa

# Use pyth on in resource-efficient mode
export PYTHONOPTIMIZE=1
```

#### **If You Have Slow Internet:**

```bash
# Cache Docker layers locally
docker pull python:3.10-slim  # Pre-pull base images

# Use local package mirrors
pip install --index-url https://your-local-mirror

# Download datasets once
# Store in project/data/ and reuse
```

#### **If You Have Limited Disk Space:**

```bash
# Clean Docker regularly
docker system prune -a  # Remove unused images/containers

# Use .dockerignore to exclude unnecessary files
echo "venv/" >> .dockerignore
echo ".git/" >> .dockerignore

# Don't duplicate datasets
# Use symlinks instead of copies
```

### 4. When to Move to Cloud

You'll know it's time when:

| Sign | Solution |
|------|----------|
| Training takes > 30 minutes | Use AWS/GCP/Azure for training only |
| Need to scale to 1000+ requests/sec | Deploy to cloud, develop locally |
| Team collaboration slows | Use cloud-based dev environments |
| Corporate firewall blocks everything | Use cloud workstation |

**Key principle:** Develop locally, scale in cloud.

### 5. Corporate Laptop Challenges

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMMON CORPORATE RESTRICTIONS                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PROBLEM                  │ SOLUTION                                        │
│  ─────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  No admin rights          │ Use portable Python (Anaconda)                 │
│                           │ or request IT to install                        │
│                                                                              │
│  Firewall blocks Docker   │ Configure corporate proxy                      │
│  Hub                      │ Use internal Docker registry                    │
│                                                                              │
│  Can't install Docker     │ Use Docker playground (play-with-docker.com)   │
│                           │ or cloud-based environment                      │
│                                                                              │
│  VPN required             │ Configure Git/Docker to work with VPN          │
│                                                                              │
│  Port 8000 already used   │ Use different ports (8001, 8080, etc.)         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrams

```
Resource Usage by Activity:
═══════════════════════════

Activity                RAM Usage    CPU Usage    Disk Space
────────────────────────────────────────────────────────────
VS Code (open)          500MB        Low          -
Python venv             200MB        Low          500MB
Docker Desktop          2GB          Low          10GB
Running API             300MB        Medium       -
Training model (small)  500MB        High         100MB
────────────────────────────────────────────────────────────
TOTAL (everything)      ~4GB         Varies       ~11GB

Comfortable with 8GB RAM ✅
```

---

## Lab / Demo

### Prerequisites

- Laptop with 8GB+ RAM
- Completed previous lectures

### Step-by-Step Instructions

```bash
# Step 1: Check your system specs
# On macOS:
sysctl -n hw.memsize | awk '{print $0/1024/1024/1024 " GB"}'
sysctl -n machdep.cpu.brand_string

# On Linux:
free -h
lscpu | grep "Model name"

# On Windows:
wmic computersystem get totalphysicalmemory
wmic cpu get name

# Step 2: Check available disk space
df -h .

# Step 3: Test Docker with resource limits
docker run --memory="512m" --cpus="1.0" python:3.10-slim python -c "print('✅ Works with limited resources!')"

# Step 4: Profile your development environment
# Install psutil
pip install psutil

# Check current usage
python -c "
import psutil
print(f'RAM: {psutil.virtual_memory().percent}% used')
print(f'CPU: {psutil.cpu_percent()}% used')
print(f'Disk: {psutil.disk_usage('/').percent}% used')
"

# Step 5: Optimize if needed
docker system prune -a  # Free up disk space
```

### Expected Output

```
$ sysctl -n hw.memsize | awk '{print $0/1024/1024/1024 " GB"}'
8 GB

$ docker run --memory="512m" python:3.10-slim python -c "print('✅ Works!')"
✅ Works with limited resources!

$ python -c "import psutil; print(f'RAM: {psutil.virtual_memory().percent}%')"
RAM: 65% used
```

### Explanation

1. **Steps 1-2**: Know your hardware so you can optimize accordingly
2. **Step 3**: Docker can run with resource constraints
3. **Step 4**: Monitor usage to identify bottlenecks
4. **Step 5**: Regular cleanup keeps things running smoothly

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Thinking you need a gaming laptop. Any modern laptop with 8GB RAM works fine for MLOps learning.

- ⚠️ **Pitfall 2**: Running too many things simultaneously. Close unused apps when training models or building Docker images.

- ⚠️ **Pitfall 3**: Using full-size Docker images. Always use `-slim` or `-alpine` variants to save disk space.

---

## Homework / Practice

1. **Exercise 1**: Measure your system's resource usage with all course tools running (VS Code, Docker, API). Is it under 8GB?

2. **Exercise 2**: Find the largest files in your project directory. Can any be excluded from Git or Docker?

3. **Stretch Goal**: Set up a cloud-based development environment (GitHub Codespaces, Gitpod) as a backup option.

---

## Quick Quiz

1. **Why don't you need a GPU for this course?**
   - A) GPUs are too expensive
   - B) We use traditional ML (scikit-learn), not deep learning
   - C) Macs don't have GPUs
   - D) GPUs are only for gaming

2. **What's the minimum RAM needed?**
   - A) 4GB
   - B) 8GB
   - C) 16GB
   - D) 32GB

3. **True or False: You must move to cloud for production MLOps.**

<details>
<summary>Answers</summary>

1. **B** - Traditional ML algorithms run efficiently on CPUs
2. **B** - 8GB is minimum, 16GB is comfortable
3. **False** - You can start on-premise; cloud is one deployment option

</details>

---

## Summary

- GPUs aren't needed for MLOps—this is about systems, not just training
- 8GB RAM and any modern CPU is sufficient for this course
- Use slim Docker images and close unused apps to save resources
- Develop locally, scale to cloud only when necessary
- Corporate laptops work fine with proper configuration
- Focus on learning workflows, not buying hardware

---

## Next Steps

→ Continue to **Lecture 2.8**: Troubleshooting Common Setup Issues (Ports, Docker, Permissions, Proxies)

---

## Additional Resources

- [Docker Resource Constraints](https://docs.docker.com/config/containers/resource_constraints/) - Limit container resources
- [GitHub Codespaces](https://github.com/features/codespaces) - Cloud-based development
- [VSCode Remote Development](https://code.visualstudio.com/docs/remote/remote-overview) - Develop on remote machines
- [Lightweight Python Docker Images](https://pythonspeed.com/articles/smaller-python-docker-images/) - Optimize image size
