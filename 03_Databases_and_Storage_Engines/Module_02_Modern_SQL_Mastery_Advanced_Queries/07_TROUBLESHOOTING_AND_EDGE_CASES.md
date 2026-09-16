# Module 02 Modern SQL Mastery Advanced Queries: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Modern SQL Mastery & Advanced Queries**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. The NULL Hazard in NOT IN Subqueries

### 🚨 Symptom
> Query with WHERE id NOT IN (SELECT foreign_id FROM ...) returns 0 rows unexpectedly.

### 🔍 Root Cause Analysis
In SQL three-valued logic, if the subquery returns even a single row with NULL, `val NOT IN (NULL, 1, 2)` evaluates to UNKNOWN for all rows, which WHERE discards.

### 🛠️ Production Fix & Mitigation Runbook
Always use `WHERE NOT EXISTS (SELECT 1 FROM ... WHERE ...)` or filter out nulls with `WHERE foreign_id IS NOT NULL`.

---

## 2. Window Function Frame Default Trap (RANGE vs ROWS)

### 🚨 Symptom
> Running sum produces identical duplicate values for rows with the same timestamp or amount.

### 🔍 Root Cause Analysis
The SQL standard default frame specification for `ORDER BY` is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which aggregates over peers with identical order values simultaneously.

### 🛠️ Production Fix & Mitigation Runbook
Explicitly define `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` when you want strict row-by-row running accumulators.

---

## 3. Cartesian Product in Multi-Join Aggregations

### 🚨 Symptom
> SUM(order_items.amount) returns wildly inflated numbers (e.g. 5x-10x actual values).

### 🔍 Root Cause Analysis
Joining a parent table with two independent 1:N child tables simultaneously creates an $N 	imes M$ Cartesian explosion of duplicate rows.

### 🛠️ Production Fix & Mitigation Runbook
Aggregate each child table in an independent CTE or subquery before joining to the parent entity.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
