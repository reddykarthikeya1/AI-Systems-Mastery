# Module 06: MySQL & MariaDB Architecture, InnoDB & Replication

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 06**. In this module, you will explore the internals of **MySQL and MariaDB**, dissect the **InnoDB** storage engine's physical disk structures, and understand the mechanics of production replication topologies.

---

## 🏗️ 1. The MySQL Pluggable Storage Engine Architecture

Unlike PostgreSQL, which uses a single integrated storage engine, MySQL separates the **Server Layer** (SQL parsing, query caching, optimization, authentication) from the **Pluggable Storage Engine Layer** (disk layouts, locking, transactions).

```
                        [Client Connection Pool]
                                    │
                                    ▼
                     [MySQL Server Tier (NoSQL/SQL)]
               ├── Parser & Pre-processor
               ├── Cost-Based Query Optimizer (CBO)
               └── Binary Log (binlog) Replication Engine
                                    │
                                    ▼ (Storage Engine API)
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
  [InnoDB Engine]            [MyISAM Engine]             [Memory Engine]
 (ACID, Clustered Index,    (Table-level locks,         (Non-persistent,
  MVCC, Row-level Locks)     No transactions)            In-RAM hash tables)
```

---

## 🌳 2. InnoDB Storage Internals: The Clustered Index Reality

The single most fundamental difference between InnoDB and PostgreSQL is how data is stored on disk:
- **PostgreSQL**: Stores rows in an unordered **Heap Table**. All indexes (including the Primary Key) are secondary pointers storing physical tuple addresses `(block, offset)`.
- **InnoDB**: The table **IS** a **Clustered Index (Index-Organized Table)**. The leaf pages of the Primary Key B+ Tree contain the complete, actual row data!

```
[Clustered Index: Primary Key (id)]
                ┌─────────┐
                │ [Root]  │
                └───┬─┬───┘
          ┌─────────┘ └───┐
          ▼               ▼
      ┌───────┐       ┌───────┐
      │[Node] │       │[Node] │
      └───┬───┘       └───┬───┘
          ▼               ▼
    [Leaf Page 1]   [Leaf Page 2]
    ┌───────────────────────────┐
    │ id=10 | name="Alice" | ...│ <── Full Row Data Stored Directly in Leaf!
    │ id=20 | name="Bob"   | ...│
    └───────────────────────────┘

[Secondary Index: email]
                ┌─────────┐
                │ [Root]  │
                └───┬─┬───┘
          ┌─────────┘ └───┐
          ▼               ▼
    [Leaf Page 1]   [Leaf Page 2]
    ┌───────────────────────────┐
    │ "alice@x.com" -> id=10    │ <── Leaf node contains ONLY (Indexed Val, PK)
    │ "bob@x.com"   -> id=20    │
    └─────────────┬─────────────┘
                  │ (Requires Secondary Bookmark Lookup into Clustered Index!)
                  └─────────────────────────► [Clustered Index Root]
```

### The Bookmark Lookup & Covering Index Optimization
When querying via a secondary index:
```sql
SELECT name, age FROM users WHERE email = 'alice@example.com';
```
1. InnoDB traverses the secondary B+ Tree for `email` to find Primary Key `id=10`.
2. InnoDB must then perform a **second B+ Tree traversal** down the Clustered Index to retrieve `name` and `age` (Bookmark Lookup).

**The Covering Index Trick**: If all queried columns are present in the secondary index:
```sql
CREATE INDEX idx_user_cover ON users(email, name, age);
```
InnoDB fetches all data directly from the secondary index leaf page and **skips the Clustered Index lookup entirely**!

---

## 🛡️ 3. Crash Recovery: Doublewrite Buffer & Redo Logs

InnoDB uses **16 KB pages**, but physical OS disk sectors are typically **4 KB** (or 512 bytes). 

### The Torn Page Hazard
If the power fails while InnoDB is writing a 16KB page to disk, the operating system might have written 8KB before failing. The page is now half-new, half-old — a **torn page**. Because the page header checksum fails, Redo Logs cannot be applied!

### The Doublewrite Buffer Solution
Before writing dirty pages to their final location in data files:
1. InnoDB writes the pages contiguously to the **Doublewrite Buffer** on disk in sequential I/O.
2. Only after the doublewrite buffer is fsynced does InnoDB write the pages to the main data files.
3. If a crash occurs during step 2, InnoDB restores the intact 16KB page from the Doublewrite Buffer and applies Redo Logs safely!

---

## 🔄 4. MySQL Replication Topologies & Binlog Formats

### Binlog Formats
1. **`STATEMENT`**: Logs exact SQL text (`UPDATE users SET active = 1 WHERE ...`).
   - *Risk*: Breaks on non-deterministic functions (`NOW()`, `RAND()`, `UUID()`).
2. **`ROW`** (Default & Production Standard): Logs before-and-after row byte images.
   - *Advantage*: Completely deterministic, safe for all functions, supports CDC (Debezium).
3. **`MIXED`**: Uses statement format by default; switches to row format for non-deterministic queries.

### GTID (Global Transaction Identifiers)
Traditional replication tracked binary log filenames and byte offsets (`mysql-bin.000123`, position `45928`). If a primary died, failing over to a replica required manual binary log offset reconciliation.
- **GTID format**: `<server_uuid>:<sequence_number>` (e.g. `3E11FA47-71CA-11E1-9E33-C80AA9429562:1-50`).
- Every transaction globally has a unique sequential ID. Replicas automatically negotiate missed transactions without offset math!

---
## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/innodb_engine.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | innodb_engine.py (Clustered index & buffer pool LRU model) | mysql_live.py (mysql-connector-python, read/write split router) |
| **Verification** | `project_solution/test_innodb_engine.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. Transaction Deadlock (Error 1213): Unordered concurrent updates create wait-for graph cycles, triggering rollbacks.
2. Replication Lag: Single-threaded replica appliers lag behind write-heavy primaries, serving stale read data.
3. Buffer Pool Thrashing: Large analytical table sweeps flush frequently accessed OLTP pages from the LRU young sublist.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT use MySQL with MyISAM storage engine in modern production; always use InnoDB to guarantee ACID transaction durability and crash recovery.

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_06_MySQL_MariaDB_InnoDB_Replication -v

# Operational Diagnostics & Health Verification
mysql -u root -p -e "SHOW ENGINE INNODB STATUS\G"
mysql -u root -p -e "SHOW REPLICA STATUS\G"
mysql -u root -p -e "SELECT * FROM performance_schema.threads WHERE PROCESSLIST_COMMAND != 'Sleep';"
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_mysql_innodb.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](04_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](05_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.

