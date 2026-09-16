# Module 22 Query Optimization CBO Index Tuning: Project Guide

## 📌 Project Overview: Relational Query Planner & Cost-Based Optimizer

This comprehensive guide walks you step-by-step through building the project for **Query Optimization: Cost-Based Optimizer (CBO) & Index Tuning**.
You will implement both the **internal algorithmic mechanics** (Track A) and **production-grade live operations** (Track B) utilizing **Relational algebra AST, cost estimation (CPU vs I/O), join ordering (dynamic programming), and index selection**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | Parse simple SQL SELECT statements into an Abstract Syntax Tree (AST). |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | Build a cost-based query optimizer that enumerates join permutations (System R dynamic programming), evaluates table statistics (histograms), and selects optimal physical operators (Hash Join vs Nested Loop). |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | Implement genetic query optimization (GEQO) for large multi-table joins (>10 relations) avoiding exponential search space explosion. |

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
Module_22_Query_Optimization_CBO_Index_Tuning/
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
   pytest Module_22_Query_Optimization_CBO_Index_Tuning -v
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

- [ ] All Track A unit tests pass: `pytest Module_22_Query_Optimization_CBO_Index_Tuning/project_solution/test_*_engine.py`
- [ ] Reconciliation tests pass without warnings: `pytest Module_22_Query_Optimization_CBO_Index_Tuning/project_solution/test_*_live.py`
- [ ] Code strictly follows PEP 8 styling and type annotations (`mypy` / `ruff`).
- [ ] Edge cases handled: offline services skip gracefully using `@pytest.mark.skipif`.

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Read `EXPLAIN (ANALYZE)` and find where estimates diverge from actuals
- [ ] Explain how the planner uses statistics and what `ANALYZE` refreshes
- [ ] Say why a function wrapping an indexed column prevents index use, and fix it
- [ ] Predict when the planner will pick a nested loop over a hash join
- [ ] Explain what an index-only scan requires
- [ ] Diagnose a query that was fast at 10k rows and slow at 10M
- [ ] Decide against adding an index and justify it by write cost

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
