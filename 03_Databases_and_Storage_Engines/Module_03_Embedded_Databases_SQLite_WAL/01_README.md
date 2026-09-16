# Module 03: Embedded Databases – SQLite Architecture & Write-Ahead Logging (WAL)

> **Brand new to this topic?** Start with [`00_W3_BEGINNER_PLAYGROUND.md`](00_W3_BEGINNER_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 03**! SQLite is the most widely deployed database engine on planet Earth (present inside every smartphone, browser, airplane, and operating system). In this module, we explore **Embedded Architecture**, **Write-Ahead Logging (WAL)**, registering **Custom Python Functions into SQLite**, and **Async SQLite with `aiosqlite`**.

---

## 🗺️ Recommended Step-by-Step Learning Path

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[README.md](01_README.md)** *(Current File)* | Read the theory, Rollback Journal vs WAL, and SQLite B-Tree file format. |
| **2** | **[01_sqlite_wal_benchmarking_demo.py](03_sqlite_wal_benchmarking_demo.py)** | Run in terminal (`python 01_sqlite_wal_benchmarking_demo.py`) to benchmark standard Rollback Journal vs WAL mode. |
| **3** | **[02_custom_python_sql_functions_demo.py](04_custom_python_sql_functions_demo.py)** | Run in terminal to see how Python regex and hashing algorithms can be executed directly inside SQL queries. |
| **4** | **[TROUBLESHOOTING_AND_EDGE_CASES.md](07_TROUBLESHOOTING_AND_EDGE_CASES.md)** | Review SQLite concurrency traps: `database is locked`, busy timeouts, and multi-thread limits. |
| **5** | **[SELF_ASSESSMENT_AND_CHALLENGES.md](06_SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test yourself with the 10-question quiz and solve the 2 hands-on coding challenges. |
| **6** | **[PROJECT_GUIDE.md](05_PROJECT_GUIDE.md)** | Build the **High-Concurrency WAL Engine with Custom SQL** in **[project_solution/](project_solution)**! |

---

## 1. What is an Embedded Database?

In client-server databases (like PostgreSQL or Oracle), your application sends network packets over TCP/IP to an external database server process.

In **SQLite**, there is no server process, no network socket, and no port. The entire database engine is a compact C library compiled directly into your application. When you execute a query, your application reads and writes directly to a single disk file!

---

## 2. Rollback Journal vs. Write-Ahead Logging (WAL)

By default, SQLite uses a **Rollback Journal**:
1. When writing, SQLite copies original unchanged database pages to a `.journal` file.
2. It writes changes directly into the main `.db` file.
3. **The Concurrency Problem:** While a write is in progress, **readers are completely blocked**! Only one reader or one writer can touch the database at any moment.

### The Breakthrough: WAL Mode (`PRAGMA journal_mode=WAL;`)
In **WAL mode**, SQLite reverses the process:
1. The main `.db` file is left untouched.
2. New changes are appended sequentially to a separate `-wal` file.
3. **The Superpower:** **Readers do not block writers, and writers do not block readers!** Readers read committed pages from the main `.db` and the `-wal`, while a writer appends to the `-wal` concurrently.
4. **Checkpointing:** Periodically, SQLite copies WAL changes back into the main `.db` and truncates the WAL file.

```
       Write-Ahead Logging (WAL) Mode
┌────────────────┐          ┌────────────────┐
│ Active Reader  │ ───────> │  app.db file   │ (Original committed data)
└────────────────┘          └───────▲────────┘
                                    │ Checkpoint sync
┌────────────────┐          ┌───────┴────────┐
│ Active Writer  │ ───────> │  app.db-wal    │ (Append-only write stream)
└────────────────┘          └────────────────┘
```

---

## 3. Registering Custom Python Functions in SQL

Python's `sqlite3` driver allows you to register pure Python functions directly into the SQL engine:

```python
import sqlite3
import re

conn = sqlite3.connect(":memory:")

# Register custom regex function (Name, ArgCount, Function)
conn.create_function("regexp", 2, lambda expr, item: 1 if re.search(expr, item) else 0)

# Now you can use REGEXP syntax in SQL!
cursor = conn.execute("SELECT * FROM users WHERE email REGEXP '^[a-z0-9]+@company\\.com$'")
```

---

## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/sqlite_wal_engine.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | sqlite_wal_engine.py (WAL concurrency model) | sqlite3 (WAL mode, busy_timeout, custom UDFs) |
| **Verification** | `project_solution/test_sqlite_wal_engine.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. Database Locked: Concurrent writers without busy_timeout immediately throw SQLITE_BUSY.
2. Runaway WAL Growth: Long-running active readers holding open old read snapshots prevent WAL checkpoint truncation.
3. Silent Corruption: Running with PRAGMA synchronous = OFF risks torn pages on sudden power cut.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](07_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT use SQLite across network-attached storage (NFS, SMB) or for applications requiring dozens of simultaneous high-throughput concurrent writers.

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_03_Embedded_Databases_SQLite_WAL -v

# Operational Diagnostics & Health Verification
sqlite3 app.db "PRAGMA journal_mode = WAL;"
sqlite3 app.db "PRAGMA wal_checkpoint(TRUNCATE);"
sqlite3 app.db "PRAGMA integrity_check;"
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_sqlite_wal.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](05_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](07_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](06_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.
### SQLite Deep-Dive: The Shm Index & Frame Checksumming
The SQLite WAL architecture relies on an auxiliary shared-memory (`.shm`) file:
- **Fast Frame Mapping:** Readers map WAL frame offsets directly into 32KB shared-memory hash tables, bypassing file seeks.
- **Frame Headers:** Each 24-byte WAL frame header records a 32-bit page number, commit marker flag, and rolling cumulative checksum.
- **Zero Reader Interference:** Readers snapshot the current WAL salt and max committed frame upon starting, ensuring read isolation is never disrupted by background checkpointing.
### Production WAL Checkpointing Strategies: PASSIVE vs RESTART vs TRUNCATE
In mission-critical embedded deployments, choosing the proper checkpointing pragma is critical:
- **`PRAGMA wal_checkpoint(PASSIVE);`**: Checkpoints as many frames as possible without blocking active readers or writers. If a reader is open on an older frame, it pauses at that frame.
- **`PRAGMA wal_checkpoint(FULL);`**: Blocks subsequent writers until all active readers complete, flushing all frames to the main database file.
- **`PRAGMA wal_checkpoint(RESTART);`**: Similar to FULL, but ensures subsequent writers begin writing at frame 1 of the WAL file.
- **`PRAGMA wal_checkpoint(TRUNCATE);`**: Flushes all frames and truncates the `-wal` file to zero bytes on disk, reclaiming operating system storage.
### Architectural Summary
- Concurrency Model: 1 exclusive writer, N concurrent readers without blocking.
- Checkpoint Modes: PASSIVE, FULL, RESTART, TRUNCATE.
- Recovery Mechanism: On-disk WAL frame replay with rolling cumulative checksums.
