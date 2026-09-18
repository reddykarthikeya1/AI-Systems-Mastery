# Module 07: Oracle Database Architecture – SGA, PGA & Storage Subsystems

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 07**. In this module, you will master the foundational architecture of the **Oracle Database** — the undisputed cornerstone of global enterprise banking, telecommunications, and mission-critical ERP infrastructure.

---

## 🏛️ 1. The Oracle Instance vs. The Oracle Database

A common point of confusion for beginners is the strict Oracle distinction between an **Instance** and a **Database**:
- **The Instance (Volatile / In-Memory)**: Consists of the shared memory structures (**SGA**) and background processes running in operating system RAM. It exists only while the database is started.
- **The Database (Persistent / On-Disk)**: The set of physical operating system files (Datafiles, Control Files, Redo Log Files) residing permanently on storage.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ORACLE DATABASE INSTANCE                        │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                SYSTEM GLOBAL AREA (SGA - Shared RAM)             │  │
│  │ ┌────────────────────────┐ ┌───────────────────┐ ┌─────────────┐ │  │
│  │ │ Database Buffer Cache  │ │    Shared Pool    │ │ Redo Log    │ │  │
│  │ │ (Default, Keep, Recyc) │ │ (Library Cache,   │ │ Buffer      │ │  │
│  │ │ (Touch-Count LRU Pages)│ │  Dict Cache)      │ │ (Circular)  │ │  │
│  │ └────────────────────────┘ └───────────────────┘ └─────────────┘ │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
│                                     │                                  │
│ ┌───────────────────────────────────┼────────────────────────────────┐ │
│ │                  BACKGROUND PROCESSES (Dedicated OS Threads)       │ │
│ │   [DBWn]           [LGWR]       [CKPT]       [SMON]       [PMON]   │ │
│ │ (Dirty Blocks) (Redo to Disk) (Sync HWM)  (Instance Rec) (Cleanup) │ │
│ └─────┬────────────────┬────────────┬────────────────────────────────┘ │
└───────┼────────────────┼────────────┼──────────────────────────────────┘
        │                │            │
        ▼                ▼            ▼
 ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
 │  Datafiles  │ │ Online Redo │ │   Control   │  <── THE ORACLE DATABASE
 │  (*.dbf)    │ │ Logs (*.log)│ │ Files (*.ctl)     (Persistent Disk Files)
 └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 🧠 2. Deep-Dive into the SGA & PGA

### System Global Area (SGA)
The SGA is a single large allocated block of shared memory accessible by all Oracle server and background processes.
1. **Database Buffer Cache**: Holds copies of data blocks read from datafiles. Uses a sophisticated **touch-count augmented LRU algorithm** to prevent a single massive table scan from flushing frequently accessed reference data.
   - *Default Pool*: Standard caching.
   - *Keep Pool*: Holds tables pinned in RAM permanently (e.g. currency conversion tables).
   - *Recycle Pool*: Discards blocks immediately after use (large batch ETL staging).
2. **Shared Pool**:
   - *Library Cache*: Caches parsed executable execution plans (Cursors). If a query uses bind variables (`WHERE id = :val`), Oracle reuses the plan (**Soft Parse**, ~10µs). If literal values are hardcoded (`WHERE id = 42`), Oracle must re-parse from scratch (**Hard Parse**, ~5ms, causing library cache latch contention!).
   - *Data Dictionary Cache*: Stores table metadata, column types, and user permissions.
3. **Redo Log Buffer**: A fast circular RAM buffer holding change vectors before writing to disk.

### Program Global Area (PGA)
Unlike the SGA, the PGA is **non-shared private memory** allocated to each dedicated server process when a client connects.
- Contains the **Sort Area** (for `ORDER BY`), **Hash Area** (for Hash Joins), and cursor session state.
- Sized via `PGA_AGGREGATE_TARGET`. If a sort exceeds its private PGA budget, it spills to the `TEMP` tablespace on disk (an expensive performance cliff).

---

## 🗄️ 3. Logical to Physical Storage Hierarchy

Oracle organizes storage through five hierarchical abstraction layers:
1. **Database**: The entire collection of tablespaces.
2. **Tablespace**: A logical container (e.g., `SYSTEM`, `SYSAUX`, `USERS`, `UNDOTBS1`). Consists of one or more physical datafiles.
3. **Segment**: The storage allocated for a specific database object (e.g., a Table Segment, an Index Segment, an Undo Segment).
4. **Extent**: A contiguous set of data blocks allocated inside a datafile. As tables grow, Oracle dynamically allocates new extents.
5. **Data Block**: The smallest atomic I/O unit in Oracle (typically 8KB, ranging from 2KB to 32KB).

---

## ⚙️ 4. The Critical Background Processes

- **DBWn (Database Writer)**: Proactively writes dirty blocks from the Buffer Cache to datafiles using asynchronous I/O.
- **LGWR (Log Writer)**: Writes redo records from the Redo Log Buffer to the Online Redo Log files on disk. **Triggers immediately upon every `COMMIT`** to ensure ACID Durability.
- **CKPT (Checkpoint Process)**: Signals DBWn at scheduled intervals to write dirty blocks to disk and updates datafile and control file headers with the checkpoint SCN (System Change Number).
- **SMON (System Monitor)**: Performs automatic crash recovery on instance startup by reading online redo logs and rolling back uncommitted transactions.
- **PMON (Process Monitor)**: Detects dead client connections, releases their locks in the SGA, and frees their private PGA memory.

---
## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/oracle_sga_engine.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | oracle_sga_engine.py (Library Cache & Buffer Cache touch-count) | oracle_live.py (python-oracledb, v$sgainfo, v$sysstat) |
| **Verification** | `project_solution/test_oracle_sga_engine.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. ORA-04031 Shared Pool Exhaustion: Literal SQL without bind variables creates millions of unsharable execution plans.
2. Buffer Cache Contention: Inadequate buffer pool sizing forces synchronous DBWR writer stalls on dirty page flushes.
3. High-Water Mark Scan Penalty: Deleted records leave HWM elevated, forcing full table scans to read millions of empty blocks.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT deploy Oracle Database without configuring automated memory target parameters (ASMM/AMM) and strict bind variable enforcement across client applications.

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_07_Oracle_Database_Architecture_SGA_PGA -v

# Operational Diagnostics & Health Verification
sqlplus system/oracle@localhost:1521/FREEPDB1 <<EOF
SELECT pool, name, bytes FROM v\$sgastat WHERE bytes > 10000000;
EXIT;
EOF
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_oracle_architecture.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](04_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](05_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.
### Oracle SGA Deep-Dive: Granules and Memory Resize Operations
- **SGA Granules:** Memory is allocated in contiguous chunks (granules) ranging from 4MB (small systems) to 128MB/512MB (large systems).
- **Dynamic Sizing:** ASMM can resize the Database Buffer Cache and Shared Pool dynamically without restarting the database instance.
- **PGA Memory Areas:** Private SQL Areas, Sort Areas, and Hash Areas are allocated dynamically within PGA based on `PGA_AGGREGATE_TARGET`.
