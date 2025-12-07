# Lecture 10.4 – Building Docker Images & Pushing to Registry in CI

## In This Lecture You Will Learn

- [x] Learn how to build Docker images automatically in CI pipelines
- [x] Understand Docker image tagging strategies for ML models
- [x] Know how to push images to registries (Docker Hub, ECR, GCR) from CI

---

## Real-World Context

> **Story**: A fintech startup manually built Docker images for their ML models. Each deployment required an engineer to:
> 1. Build image locally (20 min)
> 2. Test it works (10 min)
> 3. Tag it correctly (2 min, often wrong)
> 4. Push to registry (5 min)
> 5. Update deployment configs (5 min)
>
> One Friday night deployment, they tagged the image `latest` instead of the version number. Two weeks later, they couldn't figure out which model version was in production. A rollback took 4 hours.
>
> After implementing automated builds in CI with semantic versioning, deployments became consistent, traceable, and took 5 minutes instead of 40.

Automating Docker builds in CI eliminates manual errors and makes deployments repeatable.

---

## Main Content

### 1. Docker Build Automation in CI

```yaml
# .github/workflows/docker-build.yml
name: Build and Push Model Docker Image

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: docker.io
  IMAGE_NAME: myorg/churn-prediction-model

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Log in to Docker Hub
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache,mode=max
      
      - name: Image scan for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          format: 'sarif'
          output: 'trivy-results.sarif'
```

**Key Features**:
1. **Triggers**: Builds on push to main/develop, tags, and PRs
2. **Metadata**: Automatically generates tags based on branch/tag/SHA
3. **Caching**: Speeds up builds by reusing layers
4. **Security**: Scans images for vulnerabilities
5. **Conditional Push**: Only pushes on non-PR events

### 2. Docker Image Tagging Strategies

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DOCKER TAGGING BEST PRACTICES                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ❌ ANTI-PATTERN: Only using 'latest'                                       │
│  ════════════════════════════════════                                       │
│  docker tag mymodel:latest                                                  │
│                                                                              │
│  Problems:                                                                   │
│  • Can't identify which version is deployed                                 │
│  • Can't rollback to previous version                                       │
│  • No traceability to git commit                                            │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  ✅ GOOD PATTERN: Multiple meaningful tags                                  │
│  ════════════════════════════════════                                       │
│  myorg/churn-model:v1.2.3            ← Semantic version (immutable)        │
│  myorg/churn-model:v1.2              ← Major.minor (rolling)               │
│  myorg/churn-model:v1                ← Major version (rolling)             │
│  myorg/churn-model:sha-abc1234       ← Git commit hash                     │
│  myorg/churn-model:main-abc1234      ← Branch + commit                     │
│  myorg/churn-model:latest            ← Latest stable (main branch)         │
│  myorg/churn-model:prod              ← Currently in production             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Tagging Strategy by Environment**:

```python
# generate_tags.py
import os
from datetime import datetime

def generate_image_tags(base_image, git_ref, git_sha):
    """Generate appropriate tags based on git context"""
    tags = []
    
    # Always add SHA-based tag (immutable, traceable)
    short_sha = git_sha[:7]
    tags.append(f"{base_image}:sha-{short_sha}")
    
    # Branch-specific tags
    if git_ref.startswith('refs/heads/'):
        branch = git_ref.split('/')[-1]
        tags.append(f"{base_image}:{branch}-{short_sha}")
        
        # Special handling for main/master
        if branch in ['main', 'master']:
            tags.append(f"{base_image}:latest")
    
    # Tag-based semantic versioning
    elif git_ref.startswith('refs/tags/'):
        version = git_ref.split('/')[-1]
        if version.startswith('v'):
            tags.append(f"{base_image}:{version}")
            
            # Add rolling tags for major.minor
            parts = version[1:].split('.')
            if len(parts) >= 2:
                tags.append(f"{base_image}:v{parts[0]}.{parts[1]}")
            if len(parts) >= 1:
                tags.append(f"{base_image}:v{parts[0]}")
    
    # PR tags
    elif git_ref.startswith('refs/pull/'):
        pr_number = git_ref.split('/')[2]
        tags.append(f"{base_image}:pr-{pr_number}")
    
    # Add timestamp for uniqueness
    timestamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    tags.append(f"{base_image}:build-{timestamp}")
    
    return tags

# Example usage
if __name__ == '__main__':
    tags = generate_image_tags(
        'myorg/model',
        git_ref=os.getenv('GITHUB_REF', 'refs/heads/main'),
        git_sha=os.getenv('GITHUB_SHA', 'unknown')
    )
    
    for tag in tags:
        print(tag)
```

### 3. Multi-Stage Builds for ML Models

```dockerfile
# Dockerfile with multi-stage build
# Stage 1: Build environment (heavy dependencies)
FROM python:3.9-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime environment (lightweight)
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY src/ ./src/
COPY models/ ./models/
COPY config/ ./config/

# Copy model artifacts (if not downloaded at runtime)
COPY artifacts/model.pkl ./artifacts/

# Create non-root user for security
RUN useradd -m -u 1000 modeluser && \
    chown -R modeluser:modeluser /app
USER modeluser

# Set environment variables
ENV MODEL_PATH=/app/artifacts/model.pkl
ENV PORT=8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the API server
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Why Multi-Stage Builds?**:
- **Smaller Images**: Final image doesn't include build tools (GCC, etc.)
- **Faster Deployments**: Less data to transfer
- **More Secure**: Fewer attack surfaces
- **Cost Savings**: Smaller images = lower storage/bandwidth costs

**Size Comparison**:
```
Single-stage build:   2.5 GB
Multi-stage build:    450 MB  (82% reduction!)
```

### 4. Pushing to Multiple Registries

```yaml
# Push to different registries based on environment
- name: Login to Docker Hub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_TOKEN }}

- name: Login to AWS ECR
  uses: aws-actions/amazon-ecr-login@v1

- name: Login to Google Container Registry
  uses: docker/login-action@v2
  with:
    registry: gcr.io
    username: _json_key
    password: ${{ secrets.GCR_JSON_KEY }}

- name: Build once
  run: docker build -t temp-image:${{ github.sha }} .

- name: Tag and push to Docker Hub (for development)
  run: |
    docker tag temp-image:${{ github.sha }} dockerhub/mymodel:dev
    docker push dockerhub/mymodel:dev

- name: Tag and push to ECR (for production)
  if: github.ref == 'refs/heads/main'
  run: |
    docker tag temp-image:${{ github.sha }} $ECR_REGISTRY/mymodel:${{ github.sha }}
    docker tag temp-image:${{ github.sha }} $ECR_REGISTRY/mymodel:latest
    docker push $ECR_REGISTRY/mymodel:${{ github.sha }}
    docker push $ECR_REGISTRY/mymodel:latest

- name: Tag and push to GCR (for staging)
  run: |
    docker tag temp-image:${{ github.sha }} gcr.io/project/mymodel:staging
    docker push gcr.io/project/mymodel:staging
```

---

## Lab / Demo

### Prerequisites

- Docker installed locally
- GitHub account with Actions enabled
- Docker Hub account (or AWS/GCP account for ECR/GCR)

### Step-by-Step Instructions

```bash
# Step 1: Create a simple Dockerfile for your model
cd ~/mlops-election-project
cat > Dockerfile << 'DOCKERFILE'
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY artifacts/model.pkl ./artifacts/

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
DOCKERFILE

# Step 2: Build locally to test
docker build -t mymodel:local .

# Step 3: Run and test the container
docker run -p 8000:8000 mymodel:local &
curl http://localhost:8000/health
docker stop $(docker ps -q --filter ancestor=mymodel:local)

# Step 4: Create GitHub Actions workflow
mkdir -p .github/workflows
cat > .github/workflows/docker-ci.yml << 'YAML'
name: Docker CI

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - uses: docker/build-push-action@v4
        with:
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/mymodel:${{ github.sha }}
            ${{ secrets.DOCKER_USERNAME }}/mymodel:latest
YAML

# Step 5: Add secrets to GitHub
# Go to Settings → Secrets and add:
# - DOCKER_USERNAME
# - DOCKER_PASSWORD

# Step 6: Push and watch CI build
git add .
git commit -m "Add Docker CI workflow"
git push origin main

# Step 7: Pull the built image
docker pull yourusername/mymodel:latest
docker run -p 8000:8000 yourusername/mymodel:latest
```

### Expected Output

```
GitHub Actions Log:
✓ Checkout code
✓ Set up Docker Buildx
✓ Login to Docker Hub
✓ Build and push Docker image
  - Building layer 1/8
  - Building layer 2/8
  ...
  - Successfully built abc123def456
  - Successfully tagged yourusername/mymodel:abc1234
  - Successfully tagged yourusername/mymodel:latest
  - Pushing yourusername/mymodel:abc1234
  - Pushing yourusername/mymodel:latest
  - Image pushed successfully

Local Pull:
$ docker pull yourusername/mymodel:latest
latest: Pulling from yourusername/mymodel
✓ Downloaded newer image for yourusername/mymodel:latest
```

---

## Common Pitfalls / Gotchas

- ⚠️ **Using Only 'latest' Tag**: Impossible to track which version is deployed. Always use commit SHAs or semantic versions.

- ⚠️ **Large Image Sizes**: Including build tools, test data, or cache files bloats images. Use multi-stage builds and `.dockerignore`.

- ⚠️ **Hardcoded Credentials**: Never put registry credentials in Dockerfiles or code. Use secrets management and CI/CD variables.

- ⚠️ **No Image Scanning**: Push vulnerable images to production. Use Trivy, Snyk, or registry-native scanning.

- ⚠️ **Building on Every Commit**: Wastes time and money. Use caching, build only on main/tags, or use layer caching.

---

## Homework / Practice

1. **Exercise 1**: Create a multi-stage Dockerfile
   - Builder stage with all dependencies
   - Runtime stage with only essentials
   - Compare image sizes before/after

2. **Exercise 2**: Implement automated tagging
   - Generate tags from git SHA, branch, and version
   - Push to registry with multiple tags
   - Test pulling by different tag types

3. **Stretch Goal**: Add image scanning
   - Integrate Trivy or Snyk into CI
   - Fail builds with critical vulnerabilities
   - Set up automated security alerts

---

## Quick Quiz

1. **Why use multi-stage Docker builds for ML models?**
   - A) They're required by Docker
   - B) To reduce final image size by excluding build dependencies
   - C) To make builds slower
   - D) Multi-stage builds don't help ML

   **Answer: B** - Multi-stage builds significantly reduce image size by separating build and runtime environments.

2. **What's the best practice for tagging Docker images?**
   - A) Only use 'latest'
   - B) Use multiple tags: version, SHA, branch, and latest
   - C) Never tag images
   - D) Random strings

   **Answer: B** - Multiple meaningful tags provide traceability and rollback capabilities.

3. **True or False: You should commit Docker registry credentials to your repository for CI/CD.**

   **Answer: False** - Always use secrets management (GitHub Secrets, AWS Secrets Manager, etc.).

---

## Summary

- Automate Docker builds in CI to eliminate manual errors and ensure consistency
- Use semantic versioning + git SHA tags for traceability and easy rollbacks
- Multi-stage builds dramatically reduce image size by excluding build dependencies
- Push to different registries for different environments (dev, staging, prod)
- Always scan images for vulnerabilities before deployment

---

## Next Steps

→ Continue to **Lecture 10.5**: Continuous Delivery of Models & APIs (Staging → Prod)

---

## Additional Resources

- [Docker Build Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions for Docker](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)
- [Trivy Security Scanner](https://github.com/aquasecurity/trivy)
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
