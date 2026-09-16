# Module 17 Columnar OLAP DuckDB ClickHouse: Project Guide

## 📌 Project Overview: High-Throughput Analytics Engine on Parquet & ClickHouse

This comprehensive guide walks you step-by-step through building the project for **Columnar OLAP: DuckDB & ClickHouse Vectorized Analytics**.
You will implement both the **internal algorithmic mechanics** (Track A) and **production-grade live operations** (Track B) utilizing **Columnar storage, vectorized SIMD execution, Parquet pushdown, and ClickHouse MergeTree**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | Query local CSV and Parquet files using DuckDB SQL. |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | Build a sub-second analytical reporting engine executing complex group-by aggregations on millions of records using DuckDB and ClickHouse MergeTree engines. |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | Implement partition-pruning and min/max index skipping benchmarks demonstrating columnar speedups over row-oriented relational storage. |

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
Module_17_Columnar_OLAP_DuckDB_ClickHouse/
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
   pytest Module_17_Columnar_OLAP_DuckDB_ClickHouse -v
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

- [ ] All Track A unit tests pass: `pytest Module_17_Columnar_OLAP_DuckDB_ClickHouse/project_solution/test_*_engine.py`
- [ ] Reconciliation tests pass without warnings: `pytest Module_17_Columnar_OLAP_DuckDB_ClickHouse/project_solution/test_*_live.py`
- [ ] Code strictly follows PEP 8 styling and type annotations (`mypy` / `ruff`).
- [ ] Edge cases handled: offline services skip gracefully using `@pytest.mark.skipif`.

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Explain why columnar storage compresses better than row storage
- [ ] Predict which queries benefit from columnar and which do not
- [ ] Explain what a MergeTree does in the background
- [ ] Query a Parquet file without loading it and say why that is possible
- [ ] Choose a compression codec and justify it from measured ratios
- [ ] Explain why OLAP and OLTP want opposite physical layouts

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
