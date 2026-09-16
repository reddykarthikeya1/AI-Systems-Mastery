# Module 12 Redis Data Structures Persistence: Project Guide

## 📌 Project Overview: Sliding-Window Rate Limiter & Token Bucket In-Memory Broker

This comprehensive guide walks you step-by-step through building the project for **Redis Internals: Data Structures, RDB/AOF & Sliding Windows**.
You will implement both the **internal algorithmic mechanics** (Track A) and **production-grade live operations** (Track B) utilizing **Strings, Hashes, Sets, Sorted Sets, Bitmaps, HyperLogLog, RDB, and AOF rewrite**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | Connect to Redis and set/get string keys with TTL. |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | Build a production-grade sliding-window rate limiter using Redis Sorted Sets (ZADD, ZREMRANGEBYSCORE) and an LRU cache-aside helper. |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | Implement a Redis-backed Distributed Lock using SET NX EX with Lua script safe-release verification. |

---

## 1. Architectural Blueprint & Data Flow

```text
       ┌────────────────────────────────────────────────────────┐
       │                   Application Layer                    │
       └───────────────────────────┬────────────────────────────┘
                                   │
              ┌────────────────────┴───────────────────┐
              │                                        │
     ┌────────▼──────────┐                   ┌─────────▼─────────┐
     │  Track A (Model)  │                   │  Track B (Live)   │
     │ Pure-Python Engine│                   │ Real Driver / DB  │
     │ Internal Mechanics│                   │ Production Engine │
     └────────┬──────────┘                   └─────────┬─────────┘
              │                                        │
              └────────────────────┬───────────────────┘
                                   │
                     ┌─────────────▼─────────────┐
                     │   Reconciliation Test     │
                     │  Validates Shared Semantics│
                     └───────────────────────────┘
```

---

## 2. Directory Structure & Key Files

```text
Module_12_Redis_Data_Structures_Persistence/
├── README.md                                 # Core theory, diagrams, and operational syllabus
├── PROJECT_GUIDE.md                          # This 3-tier guided project specification
├── TROUBLESHOOTING_AND_EDGE_CASES.md         # Production error signatures and debugging runbooks
├── SELF_ASSESSMENT_AND_CHALLENGES.md         # 10 diagnostic questions + coding challenges
├── starter/                                  # Skeleton code with exercises and hints
└── project_solution/                         # Reference implementations & full test suites
    ├── conftest.py                           # Pytest fixtures and isolated configuration
    ├── *_engine.py                           # Track A: In-memory reference engine
    ├── test_*_engine.py                      # Track A verification tests
    ├── *_live.py                             # Track B: Real driver & client operations
    └── test_*_live.py                        # Track B integration & reconciliation tests
```

---

## 3. Step-by-Step Implementation Roadmap

### Phase 1: Environment & Setup
1. Verify required Python packages are installed: `pip install -e .`
2. If working with live database engines, ensure local services are running via Docker:
   ```bash
   docker compose up -d
   ```
3. Run existing baseline tests to verify environment health:
   ```bash
   pytest Module_12_Redis_Data_Structures_Persistence -v
   ```

### Phase 2: Building Core Capabilities (Tier 1 & 2)
1. Complete the starter exercises in `starter/`.
2. Ensure all unit tests pass with zero assertion failures.
3. Validate operational behaviors against Track B live implementations.

### Phase 3: Architect Stretch (Tier 3)
1. Implement the advanced stretch challenge specified in Tier 3.
2. Add dedicated test cases verifying boundary conditions, concurrency limits, and failure recovery.
3. Profile execution performance and record latency/throughput improvements.

---

## 4. Verification & Self-Check Checklist

- [ ] All Track A unit tests pass: `pytest Module_12_Redis_Data_Structures_Persistence/project_solution/test_*_engine.py`
- [ ] Reconciliation tests pass without warnings: `pytest Module_12_Redis_Data_Structures_Persistence/project_solution/test_*_live.py`
- [ ] Code strictly follows PEP 8 styling and type annotations (`mypy` / `ruff`).
- [ ] Edge cases handled: offline services skip gracefully using `@pytest.mark.skipif`.

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Explain why Redis is single-threaded and why that is a feature
- [ ] Describe the SDS layout and why Redis does not use C strings
- [ ] Explain how a skip list gives O(log n) rank queries
- [ ] State the difference between RDB and AOF persistence and their failure modes
- [ ] Explain why `KEYS` is banned in production and what to use instead
- [ ] Build a correct distributed lock and name the failure mode of a naive one
- [ ] Explain each `maxmemory-policy` and pick one for a given workload
- [ ] Show, with measurement, why pipelining beats N round-trips

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
