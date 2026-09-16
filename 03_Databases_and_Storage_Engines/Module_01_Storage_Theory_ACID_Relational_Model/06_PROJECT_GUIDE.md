# Module 01 Project Guide: Building a Transactional CSV Engine with WAL

This guide walks you step-by-step through building the **Module 01 Mini Project**: a **Transactional Flat-File Engine** in Python that implements a Write-Ahead Log (WAL) to provide real **ACID-like Atomicity, Schema Validation, and Crash Recovery**.

---

## 🎯 3-Tier Progressive Learning Paths

| Tier | Level | Who It Is For | What You Build |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🟢 **Scaffolded Beginner** | First-time developers practicing file I/O. | Implement basic table creation and append-only operations using the starter skeleton. |
| **Tier 2** | 🟡 **Standard Project** | Complete production-ready implementation. | Build the full transactional engine with `BEGIN`, `COMMIT`, `ROLLBACK`, WAL disk replay, and pass all unit tests in `test_csv_engine.py`. |
| **Tier 3** | 🔴 **Architect Stretch** | Systems engineering challenge. | Implement automated **WAL Checkpointing** (flushing WAL into main CSV and truncating the log file). |

---

## 1. Project Architecture & Objectives

You will create a Python class `TransactionalCSVEngine` that manages a named table:
1. **Schema Definition:** Enforces column names and data types (`int`, `float`, `str`).
2. **Write-Ahead Log (`table_name.wal`):** Appends every transaction intent before mutating disk.
3. **Primary Data File (`table_name.csv`):** Stores committed records.
4. **Crash Recovery Method (`recover()`):** Replays the WAL upon engine initialization to guarantee uncommitted transactions never leak into the table.

```
                  ┌───────────────────────────────┐
                  │   Transactional CSV Engine    │
                  └───────────────┬───────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
        ┌────────▼─────────┐             ┌─────────▼────────┐
        │  Write-Ahead Log │             │ Primary CSV File │
        │ (table_name.wal) │             │ (table_name.csv) │
        │  - BEGIN         │             │  - Committed     │
        │  - INSERT rows   │ ──Checkpoint──>  Table Rows    │
        │  - COMMIT        │             └──────────────────┘
        └──────────────────┘
```

---

## 2. Directory Structure

```
Module_01_Storage_Theory_ACID_Relational_Model/
├── project_solution/
│   ├── __init__.py
│   ├── csv_engine.py          # Complete transactional engine implementation
│   └── test_csv_engine.py     # Automated pytest test suite
```

---

## 5. You Have Mastered This Module When You Can…

Mastery is a capability, not a topic you have read about. Tick an item only
if you could do it right now, on a whiteboard, without notes.

- [ ] Explain what `fsync` actually guarantees, and what it does not
- [ ] Describe the exact failure window in which a crash loses a committed write
- [ ] Explain why a write-ahead log makes recovery possible, from first principles
- [ ] Name the four ACID properties and give a concrete failure for each when it is absent
- [ ] Predict what a reader sees mid-write in a non-atomic file update
- [ ] Explain why appending is safer than overwriting in place
- [ ] Recover a deliberately truncated WAL and say which records survive
- [ ] Argue when a plain file is genuinely sufficient instead of a database

If more than two are unticked, the material is not finished with you yet -
go back to the module's demos and the Track B live implementation.
