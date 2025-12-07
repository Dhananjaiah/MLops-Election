# Lecture - Local Testing of the Model API (curl, Postman, Simple UI)

## In This Lecture You Will Learn

- [x] Testing Docker containers locally before deployment
- [x] Using curl, Postman, and Python clients
- [x] Debugging container issues (logs, exec, networking)
- [x] Integration testing with docker-compose
- [x] Performance testing ML APIs

---

## Real-World Context

> **Story**: The Model That Worked Locally But Failed in Production
>
> An e-commerce company deployed their recommendation model to production. It immediately started returning 500 errors. Turns out they never tested it in a container—it expected a local file at /Users/dev/models/ that didn't exist in the Docker filesystem. Lesson: Always test in containers before deploying.

---

## Main Content

### 1. Container testing workflow

TODO: Detailed explanation with code examples, diagrams, and best practices.

### 2. curl for quick API tests

TODO: Detailed explanation with code examples, diagrams, and best practices.

### 3. Postman for comprehensive testing

TODO: Detailed explanation with code examples, diagrams, and best practices.

### 4. Docker networking basics

TODO: Detailed explanation with code examples, diagrams, and best practices.

### 5. Debugging containers (logs, exec, inspect)

TODO: Detailed explanation with code examples, diagrams, and best practices.


---

## Lab / Demo

### Prerequisites

- Completed previous lectures in this section
- Environment set up as per Section 2

#### Step 1: Build and run your Dockerized API

```bash
# Commands here
```

#### Step 2: Test with curl (health, predict endpoints)

```bash
# Commands here
```

#### Step 3: Create Postman collection

```bash
# Commands here
```

#### Step 4: Debug a failing container

```bash
# Commands here
```

#### Step 5: Load test with locust or ab

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
