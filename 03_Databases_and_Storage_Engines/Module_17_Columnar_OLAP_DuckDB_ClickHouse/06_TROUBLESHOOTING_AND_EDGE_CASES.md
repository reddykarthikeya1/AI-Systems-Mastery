# Module 17 Columnar OLAP DuckDB ClickHouse: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Columnar OLAP: DuckDB & ClickHouse Vectorized Analytics**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Too Many Parts Exception in ClickHouse MergeTree

### 🚨 Symptom
> ClickHouse throws `DB::Exception: Too many parts in table. Merges are processing significantly slower than inserts`.

### 🔍 Root Cause Analysis
Application executed thousands of small single-row inserts per second instead of batching.

### 🛠️ Production Fix & Mitigation Runbook
Always batch writes in ClickHouse (insert batches of 10,000 to 100,000 rows at a time) or insert into a `Buffer` engine table.

---

## 2. DuckDB Out-of-Memory on Enormous Parquet Joins

### 🚨 Symptom
> DuckDB query process is killed by OS OOM killer when aggregating multi-terabyte datasets.

### 🔍 Root Cause Analysis
DuckDB attempted to hold massive hash join tables in memory without disk spilling configured.

### 🛠️ Production Fix & Mitigation Runbook
Configure `PRAGMA max_memory = '16GB';` and specify `PRAGMA temp_directory = '/path/to/fast_disk';` to enable graceful disk-spilling joins.

---

## 3. Sub-Optimal Parquet Row-Group Sizing

### 🚨 Symptom
> Analytical query execution is 10x slower than expected when reading Parquet files.

### 🔍 Root Cause Analysis
Parquet files were saved with tiny row groups (e.g. 500 rows per group), destroying columnar vectorization benefits and increasing metadata parsing overhead.

### 🛠️ Production Fix & Mitigation Runbook
Size Parquet row groups between 100,000 and 1,000,000 rows (approx 128MB-512MB per row group).

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
