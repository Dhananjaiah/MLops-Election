# Lecture 11.5 – Model Serving Frameworks (KFServing, Seldon, BentoML)

## In This Lecture You Will Learn

- [x] Understand specialized ML serving frameworks and their benefits
- [x] Compare KFServing, Seldon Core, BentoML, and others
- [x] Learn when to use serving frameworks vs custom APIs

---

## Real-World Context

> **Story**: A team built custom FastAPI services for 10 models. Each needed custom code for metrics, logging, canary deployments, A/B testing. After adopting KFServing, they got all these features out-of-the-box with declarative configs. Development time for new models dropped from 2 weeks to 2 days.

---

## Main Content

### 1. Why Serving Frameworks

Standardize model deployment, built-in features (metrics, logging, A/B testing, canary), multi-framework support (TensorFlow, PyTorch, SKLearn), production-grade patterns.

### 2. Framework Comparison

KFServing: Kubernetes-native, standard interface. Seldon: Flexible, graph-based. BentoML: Developer-friendly, packaging focus. TorchServe: PyTorch-specific. Choose based on requirements.

### 3. When to Use

Use frameworks for: multiple models, standard patterns, rapid deployment. Use custom APIs for: unique requirements, simple cases, full control needed.

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
