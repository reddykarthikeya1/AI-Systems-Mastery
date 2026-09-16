# Module 14 Apache Cassandra Masterless Ring: Project Guide

## 📌 Project Overview: Distributed IoT Time-Series Store with Tunable Consistency

This comprehensive guide walks you step-by-step through building the project for **Apache Cassandra & ScyllaDB: Masterless Ring & Wide-Column**.
You will implement both the **internal algorithmic mechanics** (Track A) and **production-grade live operations** (Track B) utilizing **Consistent hashing token ring, wide-column keyspaces, tunable quorum, and LWT**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | Create keyspaces and simple tables using CQL and cassandra-driver. |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | Design a wide-column IoT time-series schema partitioned by (device_id, date_bucket) and ordered by timestamp, executing reads and writes with tunable QUORUM consistency. |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | Build a chaos testing simulator verifying read-repair reconciliation and tombstone compaction behavior under simulated network partition. |

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
Module_14_Apache_Cassandra_Masterless_Ring/
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
   pytest Module_14_Apache_Cassandra_Masterless_Ring -v
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

- [ ] All Track A unit tests pass: `pytest Module_14_Apache_Cassandra_Masterless_Ring/project_solution/test_*_engine.py`
- [ ] Reconciliation tests pass without warnings: `pytest Module_14_Apache_Cassandra_Masterless_Ring/project_solution/test_*_live.py`
- [ ] Code strictly follows PEP 8 styling and type annotations (`mypy` / `ruff`).
- [ ] Edge cases handled: offline services skip gracefully using `@pytest.mark.skipif`.

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Explain why Cassandra has no primary node and what that buys
- [ ] Design a partition key from a query, not from an entity
- [ ] Explain tunable consistency and compute R+W>N for a given setup
- [ ] Say what a tombstone is and why too many destroy read performance
- [ ] Explain hinted handoff and read repair
- [ ] Predict which queries a given table can and cannot serve

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
