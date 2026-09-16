# Module 07 Oracle Database Architecture SGA PGA: Project Guide

## 📌 Project Overview: Oracle SGA Library Cache & Buffer Cache Hit Ratio Analyzer

This comprehensive guide walks you step-by-step through building the project for **Oracle Database Architecture: SGA, PGA & Storage**.
You will implement both the **internal algorithmic mechanics** (Track A) and **production-grade live operations** (Track B) utilizing **Shared Pool, Database Buffer Cache, Redo Log Buffer, and Extent Allocator**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | Connect to Oracle Database using python-oracledb and run basic SELECT queries. |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | Implement an automated SGA diagnostics probe monitoring Shared Pool Library Cache hard vs soft parses and Buffer Cache touch-count hit ratios. |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | Design a tablespace extent allocation monitor tracking High-Water Mark (HWM) fragmentation and predicting tablespace exhaustion. |

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
Module_07_Oracle_Database_Architecture_SGA_PGA/
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
   pytest Module_07_Oracle_Database_Architecture_SGA_PGA -v
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

- [ ] All Track A unit tests pass: `pytest Module_07_Oracle_Database_Architecture_SGA_PGA/project_solution/test_*_engine.py`
- [ ] Reconciliation tests pass without warnings: `pytest Module_07_Oracle_Database_Architecture_SGA_PGA/project_solution/test_*_live.py`
- [ ] Code strictly follows PEP 8 styling and type annotations (`mypy` / `ruff`).
- [ ] Edge cases handled: offline services skip gracefully using `@pytest.mark.skipif`.

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Draw the Oracle SGA and name what lives in each pool
- [ ] Explain the difference between the buffer cache and the shared pool
- [ ] Say what PGA memory is used for and why it is per-session
- [ ] Query `V$` views to answer a real capacity question
- [ ] Explain what a checkpoint does and why it bounds recovery time
- [ ] Distinguish an instance from a database in Oracle terminology

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
