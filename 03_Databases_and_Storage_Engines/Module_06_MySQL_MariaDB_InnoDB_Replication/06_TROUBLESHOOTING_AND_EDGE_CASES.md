# Module 06 MySQL MariaDB InnoDB Replication: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **MySQL & InnoDB Architecture, Buffer Pool & Replication**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. MySQL Error 1213: Deadlock found when trying to get lock; try restarting transaction

### 🚨 Symptom
> High-concurrency e-commerce checkout transactions fail with deadlock errors.

### 🔍 Root Cause Analysis
Two concurrent transactions updated multiple rows in reverse order (Transaction A locked Row 1 then tried to lock Row 2; Transaction B locked Row 2 then tried to lock Row 1).

### 🛠️ Production Fix & Mitigation Runbook
Enforce strict deterministic ordering in application code (e.g. `ORDER BY id ASC` before locking rows) and implement automated transaction retries with exponential backoff.

---

## 2. Replication Lag & Stale Secondary Reads

### 🚨 Symptom
> Users create a record on the web app, refresh the page, and the record disappears.

### 🔍 Root Cause Analysis
The write went to the Primary, but the subsequent read was routed to a Read Replica that is lagging by several seconds due to single-threaded replica SQL applier bottlenecks.

### 🛠️ Production Fix & Mitigation Runbook
Enable multi-threaded replication (`replica_parallel_workers = 8`) and use read-after-write routing (route reads to Primary for 2 seconds immediately following a user write).

---

## 3. InnoDB Buffer Pool Eviction Thrashing

### 🚨 Symptom
> Disk I/O spikes to 100% and query latency degrades from 2ms to 200ms.

### 🔍 Root Cause Analysis
A full-table reporting scan swept through the buffer pool, evicting frequently accessed OLTP pages from the LRU cache.

### 🛠️ Production Fix & Mitigation Runbook
Tune `innodb_old_blocks_time = 1000` (requires pages to stay accessed for 1 second before promotion to the young sublist) preventing single-scan pollution.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
