# Module 04 PostgreSQL Core Advanced Types: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **PostgreSQL Core Architecture & Advanced Types**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. psycopg2.OperationalError: FATAL: remaining connection slots are reserved for non-replication superuser connections

### 🚨 Symptom
> Application starts throwing connection refused errors during traffic spikes.

### 🔍 Root Cause Analysis
Direct client connections have exceeded PostgreSQL's `max_connections` setting. Each PostgreSQL backend process consumes ~10MB RAM, causing memory exhaustion.

### 🛠️ Production Fix & Mitigation Runbook
Deploy PgBouncer or use an in-application connection pool (`ThreadedConnectionPool`) with pool size set to `(core_count * 2) + effective_spindle_count`.

---

## 2. GIN Index Not Used for JSONB Queries

### 🚨 Symptom
> Query on a JSONB column performs a sequential scan despite a GIN index existing on the column.

### 🔍 Root Cause Analysis
The query uses the `->` or `->>` operators instead of JSONB containment operators (`@>`, `?`, `?|`), or the GIN index was created with `jsonb_ops` instead of `jsonb_path_ops`.

### 🛠️ Production Fix & Mitigation Runbook
Rewrite queries to use containment (`data @> '{"status": "active"}'`) or create expression indexes on specific extracted fields: `CREATE INDEX idx_status ON tbl ((data->>'status'));`.

---

## 3. Integer Overflow on Serial Primary Keys

### 🚨 Symptom
> Inserts fail with `ERROR: integer out of range` on high-volume tables.

### 🔍 Root Cause Analysis
Standard `SERIAL` uses 32-bit signed integers (maximum 2,147,483,647 rows). When sequence wraps around, all subsequent inserts fail.

### 🛠️ Production Fix & Mitigation Runbook
Always declare modern tables with `BIGINT GENERATED ALWAYS AS IDENTITY` which supports up to $9 	imes 10^{18}$ rows.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
