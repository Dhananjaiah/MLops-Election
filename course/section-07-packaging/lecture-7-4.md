# Lecture 7.4 – Introduction to Docker for MLOps (Images, Containers, Registries)

## In This Lecture You Will Learn

- [x] What Docker is and why it's essential for MLOps
- [x] The difference between Docker images, containers, and registries
- [x] How Docker solves the "works on my machine" problem
- [x] Basic Docker commands every MLOps engineer needs to know
- [x] Docker architecture and how it differs from virtual machines

---

## Real-World Context

> **Story**: The $500K Kubernetes Migration That Failed
>
> A healthcare startup spent 6 months migrating their ML models to Kubernetes. On launch day, nothing worked. The culprit? Their data scientists had been running models with `pip install --user` and hardcoded paths like `/Users/sarah/models/`. When Kubernetes tried to run the code, it couldn't find anything.
>
> **The lesson**: Without containerization, your code is tightly coupled to one specific environment. Docker makes code portable.

### Why Docker for ML/MLOps?

In the real world, ML teams face:
- **Environment drift**: "It worked last week" → dependencies changed
- **Onboarding nightmare**: Takes 3 days to set up a new dev laptop
- **Can't deploy**: Production uses Linux, you dev on Mac
- **Version conflicts**: sklearn 0.24 for Model A, 1.2 for Model B (can't coexist)
- **Manual setup docs**: 47-step README that's always outdated

**Docker solves this** by:
✅ Packaging code + dependencies + OS into one portable unit  
✅ Guaranteeing identical environments (dev = staging = prod)  
✅ Isolating conflicting dependencies (run 10 different Python versions simultaneously)  
✅ Enabling cloud deployment (AWS, GCP, Azure all run Docker)  
✅ Simplifying onboarding (`docker run` vs 47-step README)

---

## Main Content

### 1. Docker Mental Model: Shipping Containers for Code

**Physical shipping analogy:**

```
Before containers (1950s):          After containers (1960s):
┌──────────────────┐                ┌─────────────────────┐
│ Load bananas     │                │  Standard Container │
│ differently than │                │  ┌───────────────┐  │
│ cars, which are  │    ══════>     │  │  Any cargo    │  │
│ different than   │                │  │  fits inside  │  │
│ electronics...   │                │  └───────────────┘  │
└──────────────────┘                └─────────────────────┘
 Custom loading per item             One loading process
 Slow, error-prone                   Fast, standardized
```

**Same concept for software:**

```
Before Docker:                       After Docker:
┌──────────────────┐                ┌──────────────────────┐
│ Install Python   │                │  Docker Container    │
│ Install sklearn  │                │  ┌────────────────┐  │
│ Install pandas   │    ══════>     │  │ App + deps +   │  │
│ Configure env... │                │  │ Python + OS    │  │
│ (10-page README) │                │  └────────────────┘  │
└──────────────────┘                └──────────────────────┘
 Manual, fragile                     Automated, reliable
```

### 2. Three Core Concepts

#### Concept 1: Docker Image (The Blueprint)

**What it is:**  
A read-only template containing your app + dependencies + OS. Like a class in OOP.

**Analogy:** A recipe for baking a cake.

```
┌───────────────────────────────────┐
│       Docker Image                │
│                                   │
│  ┌─────────────────────────────┐ │
│  │ Layer 4: Your ML code       │ │  ← 50 KB
│  ├─────────────────────────────┤ │
│  │ Layer 3: Python packages    │ │  ← 500 MB (sklearn, etc.)
│  ├─────────────────────────────┤ │
│  │ Layer 2: Python 3.9         │ │  ← 200 MB
│  ├─────────────────────────────┤ │
│  │ Layer 1: Ubuntu 20.04       │ │  ← 100 MB
│  └─────────────────────────────┘ │
│                                   │
│  Total: ~850 MB (immutable)      │
└───────────────────────────────────┘
```

**Key properties:**
- **Immutable**: Once built, never changes
- **Layered**: Each step (install Python, copy code) is a layer
- **Shareable**: Push to registry, others can pull

#### Concept 2: Docker Container (The Running Instance)

**What it is:**  
A running process created from an image. Like an object instantiated from a class.

**Analogy:** A cake baked from the recipe.

```
     Docker Image                   Docker Containers
         (1)                          (Many possible)
    ┌─────────┐
    │ Recipe  │         ═════>      ┌────┐ ┌────┐ ┌────┐
    │ for ML  │                     │ C1 │ │ C2 │ │ C3 │
    │ API     │                     └────┘ └────┘ └────┘
    └─────────┘                     Port    Port   Port
     (static)                       8000    8001   8002
                                   (running, isolated)
```

**Key properties:**
- **Ephemeral**: Can be stopped/deleted/recreated instantly
- **Isolated**: Has its own filesystem, network, processes
- **Lightweight**: Shares OS kernel (not a full VM)

#### Concept 3: Docker Registry (The App Store)

**What it is:**  
A server that stores and distributes Docker images.

**Common registries:**
- **Docker Hub**: Public registry (like NPM for Docker)
- **AWS ECR**: Amazon's private registry
- **GCP Artifact Registry**: Google's private registry
- **Azure ACR**: Microsoft's private registry

```
┌────────────────────────────────────────────────────┐
│            Docker Registry (Docker Hub)            │
│                                                    │
│  python:3.9-slim ────> 1M+ downloads              │
│  postgres:14     ────> 10M+ downloads             │
│  your-company/churn-model:v1.2.3 ──> Private     │
└────────────────────────────────────────────────────┘
           ▲                       │
           │ docker push           │ docker pull
           │                       ▼
    ┌──────────────┐        ┌──────────────┐
    │  Your laptop │        │ Prod server  │
    └──────────────┘        └──────────────┘
```

### 3. Docker vs Virtual Machines

| Aspect | Virtual Machine | Docker Container |
|--------|----------------|------------------|
| **Size** | 10-50 GB | 100-500 MB |
| **Startup** | Minutes | Seconds |
| **Isolation** | Full OS per VM | Process-level |
| **Performance** | Slower (hypervisor overhead) | Near-native |
| **Density** | 5-10 VMs per host | 100+ containers per host |
| **Use Case** | Complete OS isolation | App portability |

```
Virtual Machines:                    Docker Containers:
┌──────────────────────────┐        ┌──────────────────────────┐
│   Host OS (Linux)        │        │   Host OS (Linux)        │
│  ┌────────────────────┐  │        │  ┌────────────────────┐  │
│  │   Hypervisor       │  │        │  │  Docker Engine     │  │
│  │  ┌──────┐ ┌──────┐ │  │        │  │ ┌───┐ ┌───┐ ┌───┐ │  │
│  │  │ VM 1 │ │ VM 2 │ │  │        │  │ │C1 │ │C2 │ │C3 │ │  │
│  │  │ OS   │ │ OS   │ │  │        │  │ │App│ │App│ │App│ │  │
│  │  │ App  │ │ App  │ │  │        │  │ └───┘ └───┘ └───┘ │  │
│  │  └──────┘ └──────┘ │  │        │  └────────────────────┘  │
│  └────────────────────┘  │        └──────────────────────────┘
└──────────────────────────┘        
Each VM: ~10 GB, 2-3min startup     Each container: ~500MB, <1s startup
```

**When to use which:**
- **VMs**: Need different OS (Windows + Linux), strong security isolation
- **Containers**: Same OS, fast deployment, microservices, MLOps

### 4. Essential Docker Commands

#### Installation Check

```bash
# Verify Docker is installed
docker --version
# Docker version 24.0.5, build ced0996

# Run hello-world (tests everything)
docker run hello-world
# Pulls image, runs container, prints message, exits
```

#### Working with Images

```bash
# Pull an image from Docker Hub
docker pull python:3.9-slim

# List local images
docker images
# REPOSITORY    TAG        IMAGE ID       SIZE
# python        3.9-slim   1234567890ab   122MB

# Build an image from Dockerfile
docker build -t my-ml-api:v1 .

# Remove an image
docker rmi python:3.9-slim

# Push image to registry
docker push myuser/my-ml-api:v1
```

#### Working with Containers

```bash
# Run a container (create + start)
docker run -d -p 8000:8000 --name my-api my-ml-api:v1
# -d: detached (background)
# -p: map port 8000 on host to 8000 in container
# --name: give it a friendly name

# List running containers
docker ps
# CONTAINER ID   IMAGE           STATUS       PORTS
# abc123def456   my-ml-api:v1    Up 2 mins    0.0.0.0:8000->8000/tcp

# List all containers (including stopped)
docker ps -a

# View logs
docker logs my-api
docker logs -f my-api  # Follow (tail -f)

# Execute command inside running container
docker exec -it my-api bash  # Interactive shell
docker exec my-api python --version  # One-off command

# Stop a container
docker stop my-api

# Start a stopped container
docker start my-api

# Remove a container
docker rm my-api
docker rm -f my-api  # Force remove (even if running)

# Remove all stopped containers
docker container prune
```

#### Inspecting Containers

```bash
# Get detailed info
docker inspect my-api

# Check resource usage
docker stats my-api
# CPU %   MEM USAGE / LIMIT     NET I/O
# 0.5%    250MB / 4GB           1.2kB / 0B

# View processes inside container
docker top my-api
```

### 5. Docker Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Client (CLI)                  │
│         $ docker run / build / push / pull              │
└──────────────────────┬──────────────────────────────────┘
                       │ REST API
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  Docker Daemon (dockerd)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Image Management                                 │  │
│  │  • Build images from Dockerfiles                  │  │
│  │  • Pull/push from registries                      │  │
│  │  • Cache layers                                   │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Container Management                             │  │
│  │  • Create/start/stop containers                   │  │
│  │  • Network between containers                     │  │
│  │  • Mount volumes (persistent storage)             │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Linux Kernel (containerd, runc)            │
│  • Process isolation (namespaces)                       │
│  • Resource limits (cgroups)                            │
│  • Filesystem layers (overlay2)                         │
└─────────────────────────────────────────────────────────┘
```

---

## Lab / Demo

### Prerequisites

- Docker installed ([get.docker.com](https://get.docker.com))
- Basic terminal/bash knowledge

### Step-by-Step Instructions

#### Step 1: Verify Installation

```bash
# Check Docker is running
docker --version
docker info | head -n 10

# Test with hello-world
docker run hello-world
```

**Expected output:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

#### Step 2: Run Your First Container

```bash
# Run interactive Ubuntu container
docker run -it ubuntu:20.04 bash

# You're now inside the container!
# Try these commands:
apt-get update
apt-get install -y python3
python3 --version
exit  # Leave container
```

**What just happened?**
1. Docker pulled Ubuntu 20.04 image (~30 MB)
2. Created isolated container from that image
3. Started bash shell inside
4. When you exited, container stopped (but still exists)

#### Step 3: Run a Web Server

```bash
# Run nginx web server
docker run -d -p 8080:80 --name my-nginx nginx:alpine

# Test it
curl http://localhost:8080
# Should see "Welcome to nginx!"

# Check logs
docker logs my-nginx

# Stop and remove
docker stop my-nginx
docker rm my-nginx
```

#### Step 4: Explore Container Filesystem

```bash
# Run Python container with interactive shell
docker run -it python:3.9-slim bash

# Inside container:
ls /usr/local/bin  # See Python is installed
python --version
pip list
echo "print('Hello from Docker!')" > /tmp/test.py
python /tmp/test.py
exit

# Container stopped. File is gone (ephemeral)!
```

#### Step 5: Understanding Image Layers

```bash
# Pull an image and see layers
docker pull python:3.9-slim

# Output shows layers:
# Pulling from library/python
# 01234567: Pull complete   ← Layer 1 (Base OS)
# 89abcdef: Pull complete   ← Layer 2 (System deps)
# fedcba98: Pull complete   ← Layer 3 (Python)

# View image history (layers)
docker history python:3.9-slim
```

#### Step 6: Container Persistence Problem

```bash
# Create a file in a container
docker run -it --name temp-container ubuntu:20.04 bash
echo "Important data" > /data.txt
exit

# Start the same container again
docker start temp-container
docker exec temp-container cat /data.txt
# File is still there!

# But if you remove the container...
docker rm temp-container
# Data is GONE forever

# Solution: Volumes (covered in Lecture 7.5)
```

---

## Common Pitfalls

### ❌ Pitfall 1: Forgetting `-d` Flag

```bash
# BAD: Blocks your terminal
docker run my-api
# Terminal is stuck, can't do anything else

# GOOD: Runs in background
docker run -d my-api
```

### ❌ Pitfall 2: Port Already in Use

```bash
# Start container on port 8000
docker run -d -p 8000:8000 api1

# Try to start another on same port
docker run -d -p 8000:8000 api2
# Error: port is already allocated

# FIX: Use different host port
docker run -d -p 8001:8000 api2  # Host 8001 → Container 8000
```

### ❌ Pitfall 3: Forgetting to Remove Containers

```bash
# After a while...
docker ps -a
# 47 stopped containers using disk space!

# Clean up
docker container prune  # Remove all stopped
docker system prune -a  # Remove everything unused (dangerous!)
```

### ❌ Pitfall 4: Running as Root

**Security issue:** By default, processes in containers run as root.

```bash
# BAD: Root user inside container
docker run -it python:3.9 bash
whoami  # root 😱

# GOOD: Non-root user (Dockerfile specifies)
# We'll cover this in Lecture 7.5
```

---

## Quiz

**Question 1**: What's the difference between a Docker image and a container?

a) They're the same thing  
b) Image is a running process, container is the template  
c) Image is the template, container is a running instance  
d) Image is for development, container is for production  

<details>
<summary>Answer</summary>

**c) Image is the template, container is a running instance**

Think class vs object in OOP. One image (recipe) can create many containers (cakes).
</details>

---

**Question 2**: Why are Docker containers faster to start than VMs?

a) Containers use better hardware  
b) Containers share the host OS kernel  
c) VMs are deprecated technology  
d) Containers have less features  

<details>
<summary>Answer</summary>

**b) Containers share the host OS kernel**

VMs boot an entire OS (~2 min), containers just start a process (~1 sec).
</details>

---

**Question 3**: What happens to data written inside a container when you `docker rm` it?

a) Data is backed up automatically  
b) Data is moved to the host  
c) Data is permanently deleted  
d) Data is saved to the image  

<details>
<summary>Answer</summary>

**c) Data is permanently deleted**

Containers are ephemeral. Use volumes for persistent data (next lecture).
</details>

---

## Key Takeaways

✅ **Docker packages code + dependencies + OS** into portable containers  
✅ **Images are immutable templates**, containers are running instances  
✅ **Containers are lightweight** (100s per host) vs VMs (10s per host)  
✅ **Registries (Docker Hub, ECR, etc.) distribute images** like NPM for Docker  
✅ **Master these commands:** `docker run`, `pull`, `build`, `ps`, `logs`, `exec`, `stop`, `rm`  
✅ **Containers are ephemeral** → Use volumes for persistent data  

---

## Next Lecture

In **Lecture 7.5**, we'll write a **Dockerfile** to package our FastAPI model service into a Docker image with best practices for ML workloads.

**Preview:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0"]
```

Then we'll run: `docker build -t churn-api . && docker run -p 8000:8000 churn-api` 🚀
