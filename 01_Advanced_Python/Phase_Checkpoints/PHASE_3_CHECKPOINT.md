# Phase 3 Checkpoint Exam: Concurrency, Asyncio & Internals

> **Phase Scope:** Modules 09–12 (Threading/Multiprocessing, Asyncio, Sockets/HTTP, CPython Internals)  
> **Allocated Time:** 120 Minutes  
> **Format:** Closed-solution, high-concurrency systems programming exam.

---

## 🎯 The Exam Mission: Hybrid Async & Threaded Ingestion Daemon

Build a dual-engine telemetry collector. An asynchronous TCP socket server receives JSON telemetry packets from distributed nodes, verifies packet framing, parses messages, and pushes them into an in-memory ring buffer. A dedicated worker pool performs CPU-intensive cryptographic digest calculations across batches without blocking the async event loop.

---

## 📋 Functional Requirements

### 1. Framed Async TCP Daemon (`daemon.py`)
- Non-blocking server using `asyncio.start_server`.
- Reuses socket address with `SO_REUSEADDR`.
- Implements length-prefixed framing (4-byte big-endian integer length + JSON payload).
- Graceful shutdown upon `SIGINT`/`SIGTERM` awaiting in-flight connections.

### 2. Offloading CPU Work
- Heavy SHA-256 and checksum aggregation executed in a `concurrent.futures.ProcessPoolExecutor`.
- The asyncio loop awaits the executor without blocking socket ingress.

### 3. Memory & Bytecode Optimization
- Telemetry records defined using `__slots__` to minimize RAM consumption under 100,000 active objects.
- Introspection utility that calculates deep object size and audits AST for banned operations.

---

## 📊 Grading Rubric (100 Points Total)

| Requirement | Criteria | Points |
| :--- | :--- | :--- |
| **Async Sockets & Framing** | Handles packet fragmentation and concatenation; clean disconnection | 25 pts |
| **Event Loop Cleanliness** | Zero synchronous blocking calls on event loop; clean process pool offload | 25 pts |
| **Concurrency Safety** | Thread/process safe synchronization; zero deadlocks; graceful cancellation | 25 pts |
| **CPython Optimization** | Slotted models verified with `__slots__`; deep memory analysis accurate | 25 pts |

**Passing Threshold:** 85/100 points required to advance to Phase 4.

---

## 🚦 Pre-Flight Gate

**Do not start this exam until all of the following pass.** Attempting a
checkpoint on a foundation that does not build wastes the exam — you will spend
your time debugging setup instead of demonstrating skill.

```bash
# From the course root. All must be green.
pytest Module_09_Concurrency_Threading_Multiprocessing \
      Module_10_Concurrency_Asyncio \
      Module_11_Networking_Sockets_HTTP \
      Module_12_Python_Internals_Bytecode_Memory \
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
2. Go back to: **Module 09's GIL material and Module 10's event-loop diagnostics**.
3. Work that module's `debug_lab/` — it drills the failure modes this exam
   punishes.
4. Re-take the exam with a different data set or a changed requirement so you
   are re-solving rather than remembering.

Re-taking a checkpoint is normal. Advancing past one you failed is not — every
later phase assumes this one.

---

## 🎓 What This Checkpoint Actually Measures

Modules 09–12 taught you a set of tools. This exam tests **whether you can pick the right concurrency primitive for a workload and keep the event loop clean**.

That is deliberately different from the module quizzes, which test whether you
understood each piece. Here nobody tells you which tool to reach for. Choosing
correctly, under a time limit, with no solution to check against, is the whole
point — and it is the closest this course gets to the actual job.
