# Module 07 Oracle Database Architecture SGA PGA: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Oracle Database Architecture: SGA, PGA & Storage**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. ORA-04031: unable to allocate bytes of shared memory

### 🚨 Symptom
> Queries fail with ORA-04031 during peak hours.

### 🔍 Root Cause Analysis
Shared Pool fragmentation caused by thousands of literal SQL statements without bind variables (`SELECT * FROM t WHERE id = 12345` instead of `:id`), exhausting chunk allocations.

### 🛠️ Production Fix & Mitigation Runbook
Convert application SQL to use bind variables, configure `CURSOR_SHARING = FORCE` as an interim mitigation, and increase Shared Pool sizing.

---

## 2. Low Buffer Cache Hit Ratio & Free Buffer Waits

### 🚨 Symptom
> Sessions hang waiting on `db file sequential read` and `free buffer waits`.

### 🔍 Root Cause Analysis
Database Buffer Cache is undersized relative to active working set, forcing LGWR and DBWR into synchronous checkpoint stalls.

### 🛠️ Production Fix & Mitigation Runbook
Inspect `v$db_cache_advice` to determine optimal cache sizing, and tune DBWR writer processes (`DB_WRITER_PROCESSES`).

---

## 3. High-Water Mark (HWM) Sequential Scan Slowdown

### 🚨 Symptom
> A table with only 10 rows takes 15 seconds to execute `SELECT * FROM t;`.

### 🔍 Root Cause Analysis
The table previously contained 100 million rows which were deleted with `DELETE` instead of `TRUNCATE`. The HWM remains at the 100M mark, forcing full table scans to read millions of empty blocks.

### 🛠️ Production Fix & Mitigation Runbook
Reclaim space and reset HWM using `ALTER TABLE t MOVE;` followed by index rebuilds, or use `TRUNCATE TABLE` when purging data.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
