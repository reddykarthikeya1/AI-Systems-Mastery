# Module 15 LSM Trees Compaction DynamoDB: Project Guide

## 📌 Project Overview: Single-Table Enterprise SaaS Core with DynamoDB

This comprehensive guide walks you step-by-step through building the project for **LSM-Trees, Compaction & Amazon DynamoDB Single-Table Design**.
You will implement both the **internal algorithmic mechanics** (Track A) and **production-grade live operations** (Track B) utilizing **LSM-Trees (MemTable, SSTable), Bloom filters, leveled compaction, and DynamoDB single-table design**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Target Audience | Scope & Deliverables |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | Fundamentals & initial setup | Perform basic PutItem and GetItem operations using boto3. |
| **Tier 2** | 🟡 **Core Production Project** | Standard course completion | Design and implement a DynamoDB Single-Table architecture supporting Users, Organizations, and Invoices using composite PK/SK and GSI inverse lookups. |
| **Tier 3** | 🔴 **Architect Stretch Challenge** | Mastery & systems engineering | Build an in-memory LSM storage engine implementing SSTable tiered merge-compaction and Bloom filter membership queries. |

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
Module_15_LSM_Trees_Compaction_DynamoDB/
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
   pytest Module_15_LSM_Trees_Compaction_DynamoDB -v
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

- [ ] All Track A unit tests pass: `pytest Module_15_LSM_Trees_Compaction_DynamoDB/project_solution/test_*_engine.py`
- [ ] Reconciliation tests pass without warnings: `pytest Module_15_LSM_Trees_Compaction_DynamoDB/project_solution/test_*_live.py`
- [ ] Code strictly follows PEP 8 styling and type annotations (`mypy` / `ruff`).
- [ ] Edge cases handled: offline services skip gracefully using `@pytest.mark.skipif`.

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Explain the LSM write path from memtable to SSTable
- [ ] Describe why LSM trees favour writes and B+ trees favour reads
- [ ] Explain what compaction does and the space/write amplification trade-off
- [ ] Design a DynamoDB single-table schema for two access patterns
- [ ] Explain why `Scan` is almost always the wrong choice
- [ ] Compute the read/write capacity a described workload needs
- [ ] Explain how a bloom filter avoids unnecessary SSTable reads

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
