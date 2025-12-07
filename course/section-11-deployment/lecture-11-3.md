# Lecture 11.3 – Deploying on VM vs Managed Services vs Kubernetes

## In This Lecture You Will Learn

- [x] Compare deployment options: VMs, managed ML services, Kubernetes
- [x] Understand trade-offs: control vs convenience, cost vs capabilities
- [x] Learn how to choose the right deployment platform

---

## Real-World Context

> **Story**: A mid-size company started deploying models on VMs—full control but constant maintenance. Moved to SageMaker for simplicity but costs exploded. Finally adopted Kubernetes for the right balance: standardized deployment, reasonable costs, full control when needed. They now deploy 50+ models efficiently.

---

## Main Content

### 1. Virtual Machines

Deploy on EC2/GCE/Azure VMs. Full control, most work. Good for: simple deployments, legacy systems, cost optimization. Bad for: scale, automation, multi-model serving.

### 2. Managed ML Services

Use SageMaker, Vertex AI, Azure ML. Least work, highest cost, vendor lock-in. Good for: quick starts, small teams, proven patterns. Bad for: cost-sensitive, custom requirements, multi-cloud.

### 3. Kubernetes

Container orchestration platform. Moderate effort, portable, scales well. Good for: multiple models, cloud-agnostic, engineering teams. Bad for: small teams without K8s expertise, simple use cases.

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
