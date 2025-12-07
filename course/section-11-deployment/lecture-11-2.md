# Lecture 11.2 – Monolith vs Microservice Model APIs

## In This Lecture You Will Learn

- [x] Understand monolithic vs microservice architectures for ML APIs
- [x] Learn trade-offs between consolidation and separation
- [x] Know how to design scalable ML API architectures

---

## Real-World Context

> **Story**: A startup deployed 15 ML models as separate microservices—each with its own API, infrastructure, monitoring. Operations became a nightmare: 15 different failure modes, complex networking, high overhead. They consolidated to 3 services grouped by domain (user models, product models, transaction models). Ops complexity dropped 80% while maintaining logical separation.

---

## Main Content

### 1. Monolithic Model API

Single API serving all models. Pros: simple deployment, shared infrastructure, easier monitoring. Cons: all models coupled, hard to scale individually, single point of failure.

### 2. Microservice Model APIs

Each model as separate service. Pros: independent scaling, isolated failures, team autonomy. Cons: operational complexity, network overhead, service mesh needed.

### 3. Hybrid Approach

Group related models into domain services. Balance simplicity and flexibility. Use API gateway for routing and authentication.

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
