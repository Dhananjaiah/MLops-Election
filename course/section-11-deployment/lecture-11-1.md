# Lecture 11.1 – Online vs Offline vs Near-Real-Time Serving

## In This Lecture You Will Learn

- [x] Understand different ML serving patterns and their trade-offs
- [x] Learn when to use online, offline, or near-real-time inference
- [x] Know how to choose the right serving pattern for your use case

---

## Real-World Context

> **Story**: A retail company built a product recommendation system using online inference—generating recommendations on every page load. This was elegant but cost $50,000/month in compute. They switched to offline batch predictions for 90% of users (pre-computed overnight) and online predictions only for VIP customers. Costs dropped to $5,000/month with no noticeable impact on user experience.

---

## Main Content

### 1. Online/Real-Time Serving

Predictions generated on-demand when requested. Low latency (<100ms), high cost, handles dynamic inputs. Use for: fraud detection, real-time personalization, critical decisions.

### 2. Offline/Batch Serving

Pre-compute predictions for known entities, store in database. Very low latency (lookup only), very low cost, can't handle new inputs. Use for: email recommendations, daily reports, non-time-critical decisions.

### 3. Near-Real-Time/Streaming

Process events from stream (Kafka), generate predictions with slight delay (seconds to minutes). Balance of cost and freshness. Use for: social media feeds, monitoring dashboards, event-driven systems.

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
