# Module 24 Production DBRE Backups Migrations HA: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Production DBRE: Backups, Migrations, Monitoring & Runbooks** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is the difference between RPO (Recovery Point Objective) and RTO (Recovery Time Objective)?** What is the difference between RPO (Recovery Point Objective) and RTO (Recovery Time Objective)?
2. **Explain Point-In-Time Recovery (PITR) in relational databases.?** Explain Point-In-Time Recovery (PITR) in relational databases.
3. **What is the Expand/Contract (Parallel Run) pattern in database migrations?** What is the Expand/Contract (Parallel Run) pattern in database migrations?
4. **Why should zero-downtime migrations set strict statement_timeout and lock_timeout?** Why should zero-downtime migrations set strict statement_timeout and lock_timeout?
5. **What is the difference between a Physical Backup (pg_basebackup) and a Logical Backup (pg_dump)?** What is the difference between a Physical Backup (pg_basebackup) and a Logical Backup (pg_dump)?
6. **What is STONITH ('Shoot The Other Node In The Head') in high availability fencing?** What is STONITH ('Shoot The Other Node In The Head') in high availability fencing?
7. **What are the key RED metrics to monitor on database clusters?** What are the key RED metrics to monitor on database clusters?
8. **How does connection pool sizing impact database CPU cache efficiency?** How does connection pool sizing impact database CPU cache efficiency?
9. **What is a Split-Brain scenario during failover, and what prevents it?** What is a Split-Brain scenario during failover, and what prevents it?
10. **Why should disaster recovery runbooks be tested with automated game days?** Why should disaster recovery runbooks be tested with automated game days?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
RPO: maximum acceptable data loss measured in time; RTO: maximum acceptable downtime until service restoration.

#### Answer 2:
Restoring a base physical backup and replaying continuous Write-Ahead Logs (WAL/binlog) up to an exact specific microsecond timestamp.

#### Answer 3:
Expand: add new column/table while maintaining old; Contract: migrate application traffic to new structure, then drop old structure online.

#### Answer 4:
To abort immediately if an exclusive lock cannot be acquired within milliseconds, preventing blocking application traffic queues.

#### Answer 5:
Physical copies raw page files on disk (fast restore, exact binary); Logical exports SQL DDL/DML statements (portable, slower).

#### Answer 6:
A fencing mechanism that forcefully powers off or isolates a failed primary node to guarantee it cannot write during failover.

#### Answer 7:
Rate (queries/sec), Errors (failed connections/deadlocks), and Duration (p95/p99 query latency).

#### Answer 8:
Oversized pools cause CPU context switching thrashing; optimal pool size is roughly $(2 \times \text{cores}) + \text{effective spindles}$.

#### Answer 9:
Both primary and promoted replica accept writes simultaneously; prevented by automated fencing and odd-numbered quorum witnesses.

#### Answer 10:
Untested backups and failovers frequently fail in real emergencies due to configuration drift, permission errors, or capacity shortages.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Implement an automated zero-downtime column rename migration runner using views and triggers.

### 🚀 Challenge 2: Architect Stretch Problem
Build a health monitoring daemon that detects replica lag and exports Prometheus metrics.

---

## Verification Criteria
- [ ] Answered all 10 diagnostic questions without checking reference notes.
- [ ] Implemented Challenge 1 and validated with automated unit tests.
- [ ] Documented trade-offs and edge case behaviors for Challenge 2.

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Point-In-Time Recovery (PITR) Failure from WAL Segment Gap

```python
# Restoring production database from basebackup taken at 02:00 UTC
# Target recovery time: 14:30 UTC
# recovery.signal present in data directory:
restore_command = 'cp /mnt/wal_archive/%f %p'
recovery_target_time = '2026-09-08 14:30:00 UTC'
```

**Observed symptom:** Postgres recovery starts, replays up to 08:15 UTC, and abruptly stops with: FATAL: could not restore file '000000010000001B00000042' from archive: return code 1. Database starts in read-only recovery state at 08:15 UTC. 6 hours of business transactions are missing.

**(a)** What is a WAL segment gap, and why does missing a single 16MB WAL file abort the entire recovery chain?

**(b)** How does `archive_command` fail silently if return codes are ignored or disks fill up?

**(c)** How do modern backup tools like pgBackRest / WAL-G prevent WAL gaps and verify archive integrity?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Point-In-Time Recovery (PITR) functions as a strictly sequential log replay. Every WAL segment contains a monotonically increasing log sequence number (LSN) and references the previous segment's end LSN. If WAL file `...42` was never archived (e.g. because the network dropped during `archive_command`, or the archive script did not return non-zero on failure), there is an unbridgeable **WAL gap**. Postgres cannot skip missing WAL files because subsequent WAL changes rely on physical page states produced by the missing segment.

**Diagnostic Commands:**
1. Check WAL archive logs:
   ```bash
   SELECT * FROM pg_stat_archiver;
   -- Look for failed_count > 0 and last_failed_wal
   ```
2. Check continuity of files in `/mnt/wal_archive`:
   ```bash
   ls -1 /mnt/wal_archive | sort
   ```

**Production Fix:**
1. **Never use naive `cp` or shell scripts for `archive_command`:** Naive shell commands often fail silently on disk full or permissions errors.
2. **Use Enterprise Backup Tools (`pgBackRest` or `WAL-G`):**
   - pgBackRest automatically validates WAL file checksums.
   - It performs asynchronous, multi-threaded retries with backoff.
   - It runs daily `archive-check` commands to verify that the WAL chain from the base backup to current LSN is 100% contiguous with zero gaps.

</details>

---

### D2. Connection Pool Exhaustion and 503 Cascades on Backend Spike

```python
# postgresql.conf
max_connections = 500

# 50 web server instances, each running Gunicorn with 20 worker processes
# No connection pooler (PgBouncer) between app and database.
# Each worker connects directly to Postgres via psycopg2.
```

**Observed symptom:** During a marketing campaign, web traffic doubles. Database CPU spikes to 100%. Web applications throw: FATAL: remaining connection slots are reserved for non-replication superuser connections. Latency across all APIs spikes from 15ms to 30,000ms.

**(a)** Why is running 1,000 direct connections to PostgreSQL disastrous for CPU performance?

**(b)** What is the memory footprint of an idle PostgreSQL backend process?

**(c)** How does configuring PgBouncer in transaction pooling mode resolve connection storms?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
PostgreSQL uses a process-per-connection model (`fork()`). Each backend connection consumes 5MB to 20MB of RAM just for process state, plus private catalog caches. More critically, having 1,000 concurrent active processes causes devastating **CPU context switching** and latch contention across shared memory structures (`ProcArrayLock`, buffer mapping tables). A 16-core server performs optimally with only 30 to 60 truly active query threads. When 1,000 workers contend simultaneously, the CPU spends 90% of cycles switching tasks rather than executing SQL.

**Diagnostic Commands:**
1. Check active connection states:
   ```sql
   SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
   -- Notice 850 connections in 'idle' or 'idle in transaction'.
   ```
2. Monitor context switches:
   ```bash
   vmstat 1  # Look at 'cs' (context switch) column spiking to 500,000+
   ```

**Production Fix:**
Deploy **PgBouncer** in **Transaction Pooling** mode:
```ini
# pgbouncer.ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb pool_size=50

[pgbouncer]
pool_mode = transaction
max_client_conn = 5000
default_pool_size = 50
```
5,000 application workers connect to PgBouncer. PgBouncer multiplexes their active queries into a tight, optimal pool of only 50 true Postgres connections, keeping CPU utilization focused on query execution.

</details>

---

### D3. Online DDL Table Lock Timeout from Unindexed Migration

```sql
-- Production table 'invoices' contains 80,000,000 rows
-- Application runs 2,000 queries per second on 'invoices'

-- Migration script executed during peak hours:
ALTER TABLE invoices ADD COLUMN tax_rate numeric NOT NULL DEFAULT 0.05;
```

**Observed symptom:** As soon as migration executes, all API requests freeze. Connection pool exhausts in 10 seconds. Database stops responding until the migration is manually killed.

**(a)** What table lock level does `ALTER TABLE` acquire in PostgreSQL?

**(b)** Why does an `AccessExclusiveLock` wait in queue behind existing read queries and block all subsequent reads?

**(c)** How do you safely add columns, indexes, and constraints using `lock_timeout` and zero-downtime DDL patterns?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
`ALTER TABLE` requires an `AccessExclusiveLock`, which conflicts with every other lock level, including simple `SELECT` queries (`AccessShareLock`). Even though adding a column with a constant default is metadata-only in Postgres 11+, the DDL statement cannot proceed until all active queries running on `invoices` finish. While `ALTER TABLE` waits in the lock queue for long-running queries to complete, **all subsequent incoming SELECT queries queue up behind the DDL lock**, causing total connection pool exhaustion and a cascading outage.

**Diagnostic Commands:**
1. Check lock queue in `pg_locks`:
   ```sql
   SELECT pid, granted, mode, query 
   FROM pg_locks l 
   JOIN pg_stat_activity a ON l.pid = a.pid 
   WHERE relation = 'invoices'::regclass;
   ```

**Production Fix:**
1. **Always set a strict `lock_timeout`:**
   ```sql
   SET lock_timeout = '2s';
   ALTER TABLE invoices ADD COLUMN tax_rate numeric DEFAULT 0.05;
   ```
   If the lock cannot be acquired within 2 seconds, the DDL fails immediately without backlogging user traffic.
2. **Multi-step Zero-Downtime Migration Pattern:**
   - Step 1: Add column without `NOT NULL` (instantaneous metadata change):
     ```sql
     ALTER TABLE invoices ADD COLUMN tax_rate numeric DEFAULT 0.05;
     ```
   - Step 2: Add `NOT NULL` constraint as `NOT VALID`:
     ```sql
     ALTER TABLE invoices ADD CONSTRAINT chk_tax_not_null CHECK (tax_rate IS NOT NULL) NOT VALID;
     ```
   - Step 3: Validate constraint asynchronously without locking:
     ```sql
     ALTER TABLE invoices VALIDATE CONSTRAINT chk_tax_not_null;
     ```

</details>

---

### D4. Replication Lag Storm During Bulk Purge Deleting 10M Rows

```sql
-- Nightly cleanup script executing on Primary:
DELETE FROM audit_events WHERE created_at < NOW() - INTERVAL '90 days';
-- Deleted 12,000,000 rows in a single statement!
```

**Observed symptom:** On the primary, the query finishes in 90 seconds. On the standby replica, replication lag climbs to 4 hours. Read-traffic routed to the replica serves stale data. Standby disk I/O saturates at 100%.

**(a)** Why does a single monolithic `DELETE` cause massive replication lag on streaming replicas?

**(b)** What is `max_standby_streaming_delay` in PostgreSQL, and how does query cancellation occur on standby?

**(c)** How should large purges be batched in small chunks or handled via table partitioning (`DROP TABLE`)?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Deleting 12,000,000 rows generates gigabytes of WAL records containing tombstone records, index deletions, and vacuum prerequisites. The primary can apply changes using multiple parallel worker threads or asynchronous I/O, but the standby replica applies WAL sequentially using a single startup process thread (`Startup`). When user queries on the replica access pages being modified by the WAL replay, a conflict occurs. If `max_standby_streaming_delay` expires, the replica either cancels user queries or pauses replication, causing lag to spiral out of control.

**Diagnostic Commands:**
1. Check replication lag on replica:
   ```sql
   SELECT pg_size_pretty(pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn())) AS replay_lag;
   ```
2. Check replication conflicts:
   ```sql
   SELECT * FROM pg_stat_database_conflicts;
   ```

**Production Fix:**
1. **Batching the Purge:** Delete in small batches of 5,000 rows with a sleep interval to allow the replica startup process to keep up:
   ```python
   while True:
       deleted = db.execute("""
           WITH cte AS (
               SELECT id FROM audit_events 
               WHERE created_at < NOW() - INTERVAL '90 days'
               LIMIT 5000
           )
           DELETE FROM audit_events WHERE id IN (TABLE cte)
           RETURNING id;
       """).rowcount
       if deleted == 0:
           break
       time.sleep(0.1)  # Throttle WAL generation
   ```
2. **Declarative Partitioning:** Partition `audit_events` by month. Dropping an old month (`DROP TABLE audit_events_2025_10`) is instantaneous, produces zero WAL row tombstones, and causes 0ms replication lag.

</details>

---

### D5. Split-Brain Automated Failover from Transient Network Blip

```python
# Custom HA Failover Daemon monitoring PostgreSQL Primary
while True:
    try:
        ping_primary()
    except TimeoutError:
        promote_standby()  # pg_ctl promote on replica!
        break
    time.sleep(1)
```

**Observed symptom:** A 3-second network switch hiccup causes the failover daemon to promote the replica. The old primary never died and continues taking writes from clients on switch A. The newly promoted standby accepts writes from switch B. The database is in split-brain with diverged WAL timelines.

**(a)** What is split-brain in database high-availability, and why is timeline divergence disastrous?

**(b)** What is STONITH / Fencing, and why is a quorum consensus mandatory for automated failover?

**(c)** How do Patroni and Raft/Etcd guarantee mutual exclusion during automated leader election?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
A naive failover daemon that promotes a standby based solely on local ping timeouts without **fencing (STONITH - Shoot The Other Node In The Head)** creates a dual-primary split-brain. Once the standby is promoted, it branches onto a new PostgreSQL timeline (Timeline 2). Meanwhile, the old primary on Timeline 1 continues accepting writes from any clients still connected to it. Because both nodes accepted different writes at the same LSN positions, their physical data files permanently diverge and cannot be re-synchronized without manual hex-level data loss reconciliation.

**Diagnostic Commands:**
1. Check timeline status:
   ```bash
   pg_controldata /var/lib/postgresql/data | grep "Latest checkpoint's TimeLineID"
   ```
   If Primary shows Timeline 1 and Standby shows Timeline 2, split-brain has occurred.

**Production Fix:**
1. **Never write custom failover scripts:** Use enterprise consensus-backed HA managers such as **Patroni** (backed by etcd/Consul) or **pg_auto_failover**.
2. **DCS (Distributed Consensus Store) Leases:** In Patroni, the leader acquires a TTL lease in etcd. If the leader loses network connectivity to etcd, it demotes itself to read-only before its lease expires.
3. **Fencing (STONITH):** Ensure power management (IPMI/AWS API) forcefully terminates the old primary instance before the standby is permitted to promote.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites real storage engine behaviors, configuration directives, and production failure modes.
Open your implementation files and verify the behavior — the fix is not hypothetical, it is in the code you have built.
