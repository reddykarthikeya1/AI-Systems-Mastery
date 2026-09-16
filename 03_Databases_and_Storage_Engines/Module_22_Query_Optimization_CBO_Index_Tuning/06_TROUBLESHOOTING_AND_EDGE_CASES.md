# Module 22 Query Optimization CBO Index Tuning: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Query Optimization: Cost-Based Optimizer (CBO) & Index Tuning**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Exponential Join Permutation Explosion

### 🚨 Symptom
> Query compilation takes 45 seconds for an 18-table JOIN query.

### 🔍 Root Cause Analysis
Dynamic programming join ordering (System R) explores $O(3^N)$ subproblems, which explodes when joining $>12$ tables.

### 🛠️ Production Fix & Mitigation Runbook
Implement a threshold switching from exhaustive dynamic programming to Genetic Query Optimization (GEQO) or greedy heuristics for queries with $>10$ joins.

---

## 2. Missing Correlation Statistics on Interdependent Columns

### 🚨 Symptom
> Query planner estimates 1 row returned, but query actually produces 500,000 rows, selecting a catastrophic Nested Loop join.

### 🔍 Root Cause Analysis
The query filtered on `city = 'San Francisco' AND state = 'CA'`. Standard optimizer assumes column independence ($P(A \cap B) = P(A) \times P(B)$).

### 🛠️ Production Fix & Mitigation Runbook
Create extended multi-column statistics: `CREATE STATISTICS s_city_state ON city, state FROM addresses;` followed by `ANALYZE`.

---

## 3. Index Suppression via Function Wrapping in WHERE Clause

### 🚨 Symptom
> Index on `created_at` is completely ignored, causing a full table scan.

### 🔍 Root Cause Analysis
Writing `WHERE DATE(created_at) = '2026-01-01'` prevents the query planner from using the standard B-Tree index on `created_at`.

### 🛠️ Production Fix & Mitigation Runbook
Write sargable range queries: `WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02'`, or create an expression index: `CREATE INDEX idx_date ON tbl (DATE(created_at));`.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
