# Module 03 Embedded Databases SQLite WAL: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Embedded Databases: SQLite & WAL Architecture**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. sqlite3.OperationalError: database is locked

### 🚨 Symptom
> Concurrent threads or processes crash with 'database is locked' during write operations.

### 🔍 Root Cause Analysis
SQLite allows multiple concurrent readers in WAL mode, but only ONE writer at any instant. If a writer attempts to acquire the exclusive write lock while another transaction holds it and busy_timeout is 0, it fails immediately.

### 🛠️ Production Fix & Mitigation Runbook
Configure `PRAGMA busy_timeout = 5000;` (wait up to 5 seconds for lock release) and ensure transactions are kept short.

---

## 2. Runaway -wal File Growth

### 🚨 Symptom
> The database WAL file (`app.db-wal`) grows to tens of gigabytes without shrinking.

### 🔍 Root Cause Analysis
A long-running active reader transaction is holding open an old read transaction snapshot, preventing the WAL checkpoint from advancing past that frame.

### 🛠️ Production Fix & Mitigation Runbook
Terminate idle in-transaction connections and configure automatic periodic checkpointing using `PRAGMA wal_autocheckpoint = 1000;` or invoke `PRAGMA wal_checkpoint(TRUNCATE);` during maintenance windows.

---

## 3. Silent Corruption via PRAGMA synchronous = OFF

### 🚨 Symptom
> System crashes result in database corruption with `SQLITE_CORRUPT` upon reboot.

### 🔍 Root Cause Analysis
With `synchronous = OFF`, SQLite hands data to the OS cache without calling `fsync()`. A sudden power outage results in torn pages or missing header updates on disk.

### 🛠️ Production Fix & Mitigation Runbook
In production WAL mode, always use `PRAGMA synchronous = NORMAL;`. It provides full ACID durability with minimal performance penalty.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
