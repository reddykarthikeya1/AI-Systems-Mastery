# Module 08 Oracle PLSQL Packages Triggers: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Oracle PL/SQL Packages, Triggers & Autonomous Transactions**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. ORA-04091: table is mutating, trigger/function may not see it

### 🚨 Symptom
> A row-level trigger fails when attempting to query or aggregate the table being updated.

### 🔍 Root Cause Analysis
A row-level trigger cannot query the table it is currently modifying because the table is in a transient, inconsistent state.

### 🛠️ Production Fix & Mitigation Runbook
Refactor into a **Compound DML Trigger** using the `BEFORE STATEMENT`, `BEFORE EACH ROW`, `AFTER EACH ROW`, and `AFTER STATEMENT` lifecycle to collect rows into an in-memory collection and aggregate in the statement phase.

---

## 2. ORA-06502: PL/SQL: numeric or value error

### 🚨 Symptom
> Stored procedure crashes with buffer overflow during string operations.

### 🔍 Root Cause Analysis
A VARCHAR2 variable in PL/SQL was declared without sufficient byte/character length (or byte vs char semantics under UTF-8).

### 🛠️ Production Fix & Mitigation Runbook
Declare string variables using explicit character semantics: `v_name VARCHAR2(100 CHAR);` or anchor to table column definitions: `v_name customers.name%TYPE;`.

---

## 3. Autonomous Transaction Deadlock

### 🚨 Symptom
> Procedure using PRAGMA AUTONOMOUS_TRANSACTION hangs permanently.

### 🔍 Root Cause Analysis
The parent transaction updated a row and held an exclusive row lock; the autonomous transaction then attempted to update the exact same row.

### 🛠️ Production Fix & Mitigation Runbook
Never update rows in an autonomous transaction that are locked by the calling parent transaction. Autonomous transactions must operate strictly on independent tables (e.g. audit logs).

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
