# Module 02 Modern SQL Mastery Advanced Queries: Project Guide

## 📌 Project Overview: Hierarchical Organization & Financial Cohort Analysis Engine

This comprehensive guide walks you step-by-step through building the project for **Modern SQL Mastery & Advanced Analytics**.
You will implement both the **internal algorithmic mechanics** (Track A) and **production-grade live operations** (Track B) utilizing **window functions, recursive CTEs, and correlated subqueries**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | Implement basic inner/left joins and simple GROUP BY aggregates. |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | Build a multi-stage financial analytics query calculating rolling 30-day customer spend, retention cohorts, and recursive managerial hierarchy. |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | Implement custom temporal gap-and-island detection identifying contiguous subscription streaks using LEAD/LAG. |

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
Module_02_Modern_SQL_Mastery_Advanced_Queries/
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
   pytest Module_02_Modern_SQL_Mastery_Advanced_Queries -v
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

- [ ] All Track A unit tests pass: `pytest Module_02_Modern_SQL_Mastery_Advanced_Queries/project_solution/test_*_engine.py`
- [ ] Reconciliation tests pass without warnings: `pytest Module_02_Modern_SQL_Mastery_Advanced_Queries/project_solution/test_*_live.py`
- [ ] Code strictly follows PEP 8 styling and type annotations (`mypy` / `ruff`).
- [ ] Edge cases handled: offline services skip gracefully using `@pytest.mark.skipif`.

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Write a window function with the right frame clause without consulting docs
- [ ] Explain the difference between `ROW_NUMBER`, `RANK` and `DENSE_RANK` on tied values
- [ ] Rewrite a correlated subquery as a join and say which the planner prefers
- [ ] Explain when a CTE is materialised and when it is inlined
- [ ] Predict the row count of any join type before executing it
- [ ] Use `GROUPING SETS` instead of a UNION of three aggregate queries
- [ ] Spot why `WHERE` cannot filter on a window function and use `QUALIFY`/subquery instead
- [ ] Read a query you did not write and state its output shape

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
