# Module 24 Production DBRE Backups Migrations HA: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Production DBRE: Backups, Migrations, Monitoring & Runbooks**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Table Rewrite Lock Stalls During ALTER TABLE ADD COLUMN DEFAULT

### 🚨 Symptom
> Executing a schema migration brings down production web services for 40 minutes.

### 🔍 Root Cause Analysis
Adding a column with a non-null default value in older database engines rewrites the entire multi-gigabyte table on disk under an exclusive table lock.

### 🛠️ Production Fix & Mitigation Runbook
In modern PostgreSQL (>= 11) and MySQL (>= 8.0), non-volatile defaults are instant metadata-only operations. In older engines, add column as nullable first, backfill in batches, then set default and NOT NULL constraints.

---

## 2. Unverified Backups Causing Disaster Recovery Failure

### 🚨 Symptom
> A ransomware event occurs, and engineers discover daily pg_dump backups have been corrupt or empty for 6 months.

### 🔍 Root Cause Analysis
Backups were created on schedule but never automatically restored and verified.

### 🛠️ Production Fix & Mitigation Runbook
Implement automated continuous disaster recovery testing: schedule an automated CI job that restores the latest backup to an isolated staging instance, verifies row counts, and runs smoke tests daily.

---

## 3. Connection Pool Exhaustion During Upstream Microservice Latency

### 🚨 Symptom
> Database connection pool spikes to 100% and crashes the application gateway.

### 🔍 Root Cause Analysis
A slow external payment API caused HTTP worker threads to hold database connections open while waiting for third-party HTTP responses.

### 🛠️ Production Fix & Mitigation Runbook
Never hold database connections across external network I/O calls. Acquire database connections only for immediate database queries and release immediately.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
