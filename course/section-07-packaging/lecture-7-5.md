# Lecture - Dockerizing the Model Service (Best Practices for Images)

## In This Lecture You Will Learn

- [x] How to write production-ready Dockerfiles for ML services
- [x] Multi-stage builds to reduce image size
- [x] Best practices: non-root users, .dockerignore, layer caching
- [x] Security considerations for ML containers
- [x] Optimizing build time and image size

---

## Real-World Context

> **Story**: The 12GB Docker Image That Broke CI/CD
>
> A fintech company's ML team built a Docker image that was 12GB. Their CI/CD pipeline timed out after 45 minutes trying to push it. The culprit? They copied their entire 8GB dataset and all development dependencies into the image. After optimization (multi-stage build, .dockerignore), they got it down to 450MB and deploys went from 45min to 3min.

---

## Main Content

### 1. Dockerfile anatomy and best practices

TODO: Detailed explanation with code examples, diagrams, and best practices.

### 2. Multi-stage builds for smaller images

TODO: Detailed explanation with code examples, diagrams, and best practices.

### 3. .dockerignore to exclude unnecessary files

TODO: Detailed explanation with code examples, diagrams, and best practices.

### 4. Layer caching strategies

TODO: Detailed explanation with code examples, diagrams, and best practices.

### 5. Security: non-root users, no secrets in images

TODO: Detailed explanation with code examples, diagrams, and best practices.


---

## Lab / Demo

### Prerequisites

- Completed previous lectures in this section
- Environment set up as per Section 2

#### Step 1: Write a basic Dockerfile for FastAPI service

```bash
# Commands here
```

#### Step 2: Add .dockerignore to exclude .git, data, models

```bash
# Commands here
```

#### Step 3: Implement multi-stage build

```bash
# Commands here
```

#### Step 4: Run security scan with docker scan

```bash
# Commands here
```

#### Step 5: Measure image size improvements

```bash
# Commands here
```


---

## Common Pitfalls

### ❌ Pitfall 1: TODO

Describe common mistake and how to avoid it.

### ❌ Pitfall 2: TODO

Describe common mistake and how to avoid it.

---

## Quiz

**Question 1**: TODO

a) Option A  
b) Option B  
c) Option C  
d) Option D  

<details>
<summary>Answer</summary>

**Answer**: Explanation

</details>

---

## Key Takeaways

✅ Key takeaway 1  
✅ Key takeaway 2  
✅ Key takeaway 3  

---

## Next Lecture

→ Continue to the next lecture in this section.
