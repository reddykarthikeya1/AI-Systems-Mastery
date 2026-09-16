# Module 24: Production DBRE — Backups, Point-in-Time Recovery & Zero-Downtime Migrations

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 24**. In this module, you will master **Database Reliability Engineering (DBRE)** — the mission-critical operational discipline that keeps production databases healthy, surviving catastrophic hardware failure with **Point-in-Time Recovery (PITR)**, scaling connections with **PgBouncer**, and evolving schemas with zero downtime using the **Expand/Contract Pattern**.

---

## ⏳ 1. The Core Metrics: RPO, RTO & Disaster Recovery

Every production database architecture is measured by two non-negotiable SLAs:
- **Recovery Point Objective (RPO)**: The maximum acceptable data loss in time.
  - *Example*: An RPO of 5 minutes means that in a total data center catastrophe, the business can afford to lose at most the last 5 minutes of committed transactions. (Tier-1 financial databases mandate an RPO of 0).
- **Recovery Time Objective (RTO)**: The maximum acceptable duration of downtime.
  - *Example*: An RTO of 15 minutes means services must be fully restored and accepting queries within 15 minutes of the disaster.

---

## 📼 2. Continuous WAL Archiving & Point-in-Time Recovery (PITR)

Traditional logical dumps (`pg_dump`, `mysqldump`) are inadequate for large production systems (terabytes of data):
- They lock tables or hold long-running read transactions that bloat the database.
- Restoring a multi-terabyte SQL text dump takes 12 to 24+ hours (destroying your RTO).
- Any transactions written between the dump time and the disaster are permanently lost (violating your RPO).

### The Solution: Base Backup + Continuous WAL Streaming
Modern databases combine **Physical Base Backups** with **Continuous Write-Ahead Log (WAL) Archiving** (using tools like `pgBackRest` or `WAL-G`):

```
Time ──►
[Day 1, 00:00] ──► [Full Physical Base Backup (800 GB)] ──► Saved to S3 Object Storage
                         │
                         ▼ Continuous WAL Stream (Shipped every 16MB or 60s)
                   [WAL 001] ──► [WAL 002] ──► [WAL 003] ──► [WAL 004] ──► [WAL 005]
                                                                              │
                                                     [14:32:05] Human Error: DROP TABLE customers!
                                                                              │
                                                     [14:32:00] ◄─────────────┘
                                                     Recovery Target Time!
```

### The 4-Step PITR Restoration Protocol
If an operator accidentally drops a production table at `14:32:05 UTC`:
1. **Restore Base Backup**: Download the most recent physical base backup taken prior to the incident into a fresh database directory.
2. **Configure Recovery Target**:
   Create a `recovery.signal` file and configure `postgresql.conf`:
   ```ini
   restore_command = 'pgbackrest --stanza=prod archive-get %f %p'
   recovery_target_time = '2026-09-07 14:32:00 UTC'
   recovery_target_action = 'promote'
   ```
3. **Sequential Redo Replay**: The database starts up in recovery mode. It streams and applies WAL records sequentially, replaying all row inserts, updates, and commits from the base backup up to exactly `14:32:00 UTC`.
4. **Target Stop & Promotion**: The engine halts replay 5 seconds *before* the fatal `DROP TABLE` command and promotes itself to read-write. **Zero data loss, 100% table recovery!**

---

## 🔄 3. Zero-Downtime Schema Migrations: The Expand/Contract Pattern

In high-traffic systems, running an in-place migration such as:
```sql
-- FATAL PRODUCTION ANTIPATTERN: Causes downtime!
ALTER TABLE users RENAME COLUMN phone TO mobile_number;
```
- Holds an `ACCESS EXCLUSIVE` table lock that queues all incoming queries.
- Older running application instances crash because they expect column `phone`.
- New application instances crash if deployed before the migration.

### The 5-Phase Expand/Contract Pattern
To rename or restructure a column with **zero downtime and zero lock contention**:

```
[Phase 1: Expand]
Add 'mobile_number' column as nullable.
App v1 still reads and writes 'phone'.

[Phase 2: Dual-Write]
Deploy App v2.
Writes to BOTH 'phone' AND 'mobile_number'.
Reads from 'phone'.

[Phase 3: Backfill]
Run background batch worker copying historical rows:
UPDATE users SET mobile_number = phone WHERE id BETWEEN ? AND ?
(Batches of 1,000 rows with 50ms sleep to prevent lock starvation).

[Phase 4: Switch Read]
Deploy App v3.
Writes to BOTH 'phone' AND 'mobile_number'.
Reads from 'mobile_number'.

[Phase 5: Contract]
Deploy App v4.
Writes ONLY to 'mobile_number'.
Drop old 'phone' column cleanly!
```

---

## 🚦 4. Connection Pooling: The Physics of PgBouncer

PostgreSQL uses a process-per-connection model. Each connected client spawns an independent OS process consuming ~10 MB of RAM:
- At 2,000 open connections, PostgreSQL consumes **20 GB of RAM purely for connection metadata**!
- More critically, hundreds of backend processes compete for CPU core time slices, resulting in massive context-switch churn and Latch contention on shared memory.

### PgBouncer Architecture
PgBouncer acts as a lightweight proxy sitting between applications and the database:

```
[5,000 App Threads / Lambda Functions]
             │
             ▼ 5,000 Lightweight Sockets
   ┌───────────────────┐
   │    PgBouncer      │ (Consumes ~2 KB per socket)
   └─────────┬─────────┘
             │ Pools into 50 Real Postgres Connections
             ▼
   ┌───────────────────┐
   │ PostgreSQL Server │ (50 Processes = Peak CPU Cache Locality & Zero Contention)
   └───────────────────┘
```

### Pooling Modes
1. **Session Pooling**: A database connection is dedicated to the client for the entire duration of its TCP connection.
2. **Transaction Pooling (Most Popular)**: A database connection is bound to the client *only for the duration of a transaction* (`BEGIN` to `COMMIT`). Once committed, the connection is returned immediately to the pool. (Allows 50 database connections to serve 10,000 active web clients!).
3. **Statement Pooling**: Connection returned after every single SQL statement (does not support multi-statement transactions).

---

## 🛠️ 5. Hands-On Lab: Building a DBRE Disaster Recovery & Migration Engine

In this lab, you will implement:
1. **Continuous WAL Archiver**: Append mutations with Log Sequence Numbers (LSN) and microsecond timestamps.
2. **Point-in-Time Recovery (PITR) Engine**: Restore an initial base snapshot and replay WAL records up to an exact target recovery timestamp, proving data recovery prior to a simulated disaster.
3. **Zero-Downtime Expand/Contract Migration**: Execute the 5-phase migration pipeline with dual-writing and batch backfilling without locking.
4. **Transaction Connection Pooler**: Implement a lightweight transaction-level connection pooler routing multiple concurrent client workers across a fixed pool of server connections.

---

## 📂 Project Structure
```
Module_24_Production_DBRE_Backups_Migrations_HA/
├── README.md
├── 01_pitr_and_zero_downtime_migration_demo.py
├── starter/
│   └── dbre_engine.py
└── project_solution/
    ├── dbre_engine.py
    └── test_dbre_engine.py
```

---

## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/dbre_engine.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | dbre_engine.py (PITR, zero-downtime migration, pool monitor) | dbre_live.py (psycopg2 pool monitoring, non-blocking migrations) |
| **Verification** | `project_solution/test_dbre_engine.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. Table Lock Starvation: Schema migrations lacking strict lock_timeout queuing behind slow queries and bringing down web traffic.
2. Untested Backups: Creating daily database dumps that fail to restore during real disasters due to corruption or permission drift.
3. Connection Pool Over-allocation: Oversized connection pools thrashing CPU caches and exhausting database memory.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT perform schema migrations directly during peak traffic hours without automated transaction timeouts and verified backward compatibility.

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_24_Production_DBRE_Backups_Migrations_HA -v

# Operational Diagnostics & Health Verification
pg_isready -h localhost -p 5432
psql -h localhost -U postgres -c "SELECT * FROM pg_stat_activity WHERE state != 'idle';"
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_production_dbre.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](04_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](05_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.

