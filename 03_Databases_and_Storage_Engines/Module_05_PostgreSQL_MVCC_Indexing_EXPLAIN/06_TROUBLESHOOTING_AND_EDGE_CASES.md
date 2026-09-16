# Module 05 PostgreSQL MVCC Indexing EXPLAIN: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **PostgreSQL MVCC, Vacuuming & Execution Plans**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Table Bloat & Autovacuum Starvation

### 🚨 Symptom
> Table size swells from 500MB to 50GB even though row count remains constant.

### 🔍 Root Cause Analysis
High frequency UPDATE/DELETE operations generate dead tuples that cannot be vacuumed because a long-running transaction holds an old transaction snapshot (visible in `pg_stat_activity`).

### 🛠️ Production Fix & Mitigation Runbook
Kill stale idle-in-transaction sessions using `pg_terminate_backend()`, configure aggressive autovacuum scale factors (`autovacuum_vacuum_scale_factor = 0.05`), and run `VACUUM FULL` or `pg_repack` to reclaim space.

---

## 2. Misleading EXPLAIN Cost Estimates Due to Stale Statistics

### 🚨 Symptom
> Query planner chooses slow Sequential Scan over an Index Scan, causing 100x latency degradation.

### 🔍 Root Cause Analysis
The query planner relies on `pg_statistic` histograms. If massive bulk inserts/deletes occur without triggering ANALYZE, row count estimates are off by orders of magnitude.

### 🛠️ Production Fix & Mitigation Runbook
Run `ANALYZE table_name;` manually after bulk data loading, or lower `autovacuum_analyze_scale_factor = 0.02`.

---

## 3. Deadlock on Concurrent Index Creation

### 🚨 Symptom
> Executing `CREATE INDEX` hangs indefinitely and blocks all read/write traffic across the entire table.

### 🔍 Root Cause Analysis
`CREATE INDEX` acquires an `ACCESS EXCLUSIVE` lock, preventing all reads and writes until index build completes.

### 🛠️ Production Fix & Mitigation Runbook
Always use `CREATE INDEX CONCURRENTLY`, which acquires only a weak `SHARE UPDATE EXCLUSIVE` lock allowing concurrent DML to continue.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
