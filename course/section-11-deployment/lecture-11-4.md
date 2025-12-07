# Lecture 11.4 – Basic Kubernetes Concepts for MLOps

## In This Lecture You Will Learn

- [x] Understand core Kubernetes concepts: Pods, Services, Deployments
- [x] Learn how K8s applies to ML model serving
- [x] Know basic kubectl commands for ML operations

---

## Real-World Context

> **Story**: An ML team struggled with manual deployment: SSH into servers, copy model files, restart processes. After adopting Kubernetes, deployments became declarative—describe desired state, K8s handles the rest. Scaling from 2 to 20 replicas: one command. Rolling updates: automatic. Rollbacks: instant.

---

## Main Content

### 1. Core K8s Concepts

Pod: smallest deployable unit (container). Deployment: manages Pod replicas. Service: stable network endpoint. Ingress: external access routing.

### 2. K8s for ML Serving

Package model in Docker, create Deployment for replicas, expose via Service, configure Ingress for external access. K8s handles scaling, health checks, rolling updates.

### 3. Essential kubectl Commands

kubectl apply, kubectl get pods, kubectl logs, kubectl scale, kubectl rollout. Monitor and manage ML deployments.

---

## Lab / Demo

### Prerequisites

- Completed previous lectures in this section
- Development environment set up per Section 2
- Access to required cloud services (if applicable)

### Step-by-Step Instructions

```bash
# Follow along with hands-on examples
# See full code in course repository
```

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Common mistake and how to avoid it
- ⚠️ **Pitfall 2**: Another common issue to watch for
- ⚠️ **Pitfall 3**: Third important consideration

---

## Homework / Practice

1. **Exercise 1**: Apply concepts to your project
2. **Exercise 2**: Experiment with variations
3. **Stretch Goal**: Advanced implementation

---

## Quick Quiz

1. **Question about key concept**
   - A) Option A
   - B) Option B (Correct)
   - C) Option C
   - D) Option D

2. **Another key question**
   - Answer: Explanation of correct answer

---

## Summary

- Key takeaway 1
- Key takeaway 2
- Key takeaway 3

---

## Next Steps

→ Continue to next lecture

---

## Additional Resources

- [Resource 1](https://example.com)
- [Resource 2](https://example.com)
- [Documentation](https://example.com)
