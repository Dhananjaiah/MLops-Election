# Lecture 10.6 – Blue/Green & Canary Deployments for ML Services

## In This Lecture You Will Learn

- [x] Understand blue/green deployment pattern for zero-downtime model updates
- [x] Learn canary deployment for gradual model rollout with risk mitigation
- [x] Know when to use each deployment strategy for ML services

---

## Real-World Context

> **Story**: An e-commerce company deployed a new recommendation model using blue/green deployment. The new model (green) was deployed alongside the old (blue), traffic was switched instantly, and they could roll back immediately when the new model caused a 15% drop in click-through rate. Without blue/green, the rollback would have taken 30 minutes instead of 30 seconds.

---

## Main Content

### 1. Blue/Green Deployment

Maintain two identical production environments. Deploy new model to inactive environment, test it, then switch traffic instantly. Enables immediate rollback.

### 2. Canary Deployment

Gradually roll out new model to small percentage of traffic (5%, 25%, 50%, 100%). Monitor metrics at each stage. Roll back if issues detected.

### 3. Choosing the Right Strategy

Use blue/green for instant rollback capability. Use canary for gradual validation and risk mitigation. Combine both for maximum safety.

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
