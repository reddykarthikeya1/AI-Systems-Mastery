# Phase 5 Checkpoint Exam: Production Architecture & Performance

> **Phase Scope:** Modules 19–20 (Containerization, CI/CD, Profiling & Caching)  
> **Allocated Time:** 90 Minutes  
> **Format:** Operational readiness and low-latency cache engineering exam.

---

## 🎯 The Exam Mission: Multi-Tier Resilient Caching Microservice

Deploy an ultra-low-latency cache microservice packaged in a minimal, non-root, multi-stage Docker container with Prometheus metrics, liveness/readiness health probes, and an LRU + Redis two-tier caching engine that eliminates cache stampedes.

---

## 📋 Functional Requirements

### 1. Two-Tier Cache Engine (`cache.py`)
- L1 in-memory LRU cache with \(O(1)\) get/set/evict.
- Monotonic clock TTL calculation (`time.monotonic()`).
- Cache stampede prevention: Dogpiling / thundering herd mitigation using single-flight locking.
- Correct handling of cached `None` (negative caching) without treating it as a cache miss.

### 2. Production Telemetry & Probes
- `/healthz/live` and `/healthz/ready` endpoints.
- `/metrics` endpoint exporting Prometheus counters and latency summaries.

### 3. Multi-Stage Container Packaging (`Dockerfile`)
- Multi-stage build (builder vs runner).
- Non-root user execution (`USER 10001`).
- Listens on `0.0.0.0:8000`.

---

## 📊 Grading Rubric (100 Points Total)

| Requirement | Criteria | Points |
| :--- | :--- | :--- |
| **Cache Algorithm & Correctness** | Constant time LRU, monotonic TTL, single-flight stampede protection | 35 pts |
| **Observability & Probes** | Prometheus counters accurately reflect requests and durations | 25 pts |
| **Container Standards** | Multi-stage Dockerfile, non-root user, proper signal handling | 20 pts |
| **Benchmark Validation** | Measured latency benchmarks prove L1 is measurably faster than L2 | 20 pts |

**Passing Threshold:** 85/100 points required to advance to Phase 6.

---

## 🚦 Pre-Flight Gate

**Do not start this exam until all of the following pass.** Attempting a
checkpoint on a foundation that does not build wastes the exam — you will spend
your time debugging setup instead of demonstrating skill.

```bash
# From the course root. All must be green.
pytest Module_19_Containerization_CICD_Deployment \
      Module_20_Performance_Optimization_Profiling_Caching \
      -q

python tools/check_links.py --quiet
ruff check .
```

If any of that is red, fix it first. The exam assumes a working environment.

---

## 📏 Exam Rules

| Rule | Detail |
| :--- | :--- |
| **Time box** | Set a timer. When it ends, stop and submit what you have. |
| **No solution exists** | There is deliberately no reference implementation for this exam. The rubric is the specification. |
| **Modules are open-book** | Re-read any README, demo or troubleshooting guide. That is not cheating; it is what the job looks like. |
| **`project_solution/` is closed-book** | Do not read the module solutions during the exam. Copying them measures nothing. |
| **Write your own tests** | Untested code scores zero on the correctness criteria, however elegant it looks. |
| **Working beats complete** | A subset that runs and is tested outscores a full implementation that does not import. |

---

## 🔬 Self-Verification Harness

Produce this evidence before you score yourself. An unmeasured claim earns no
points.

```bash
# 1. It imports and runs at all
python -m your_solution            # must not traceback

# 2. Your tests pass
pytest your_tests.py -v            # paste the summary line

# 3. It is clean
ruff check .
mypy --strict your_solution.py     # advisory, but note the count

# 4. Coverage of your own code
pytest --cov=your_solution --cov-report=term-missing
```

Record the four outputs. The rubric below is scored against **evidence**, not
against intent.

---

## ⏱️ If You Run Out of Time

Score what exists and be honest about the gap. Partial credit is real:

1. **Submit the working subset.** Delete or clearly comment out anything that
   does not run — a broken import costs you every point in the file.
2. **Write down what is missing**, in one line per requirement. Naming your own
   gap accurately is itself a senior skill and earns the analysis criteria.
3. **Keep your tests.** Tests for the parts you finished are worth more than
   untested code for the parts you did not.

---

## 🔁 If You Score Below the Threshold

This is diagnostic information, not a verdict. Do exactly this:

1. Identify which **rubric row** you lost the most points on.
2. Go back to: **Module 20's profiling workflow — measure before optimising**.
3. Work that module's `debug_lab/` — it drills the failure modes this exam
   punishes.
4. Re-take the exam with a different data set or a changed requirement so you
   are re-solving rather than remembering.

Re-taking a checkpoint is normal. Advancing past one you failed is not — every
later phase assumes this one.

---

## 🎓 What This Checkpoint Actually Measures

Modules 19–20 taught you a set of tools. This exam tests **whether you can find a real bottleneck and prove you fixed it**.

That is deliberately different from the module quizzes, which test whether you
understood each piece. Here nobody tells you which tool to reach for. Choosing
correctly, under a time limit, with no solution to check against, is the whole
point — and it is the closest this course gets to the actual job.
