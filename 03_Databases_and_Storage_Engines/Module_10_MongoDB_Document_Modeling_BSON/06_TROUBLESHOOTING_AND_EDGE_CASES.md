# Module 10 MongoDB Document Modeling BSON: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **MongoDB Document Modeling & BSON Wire Protocol**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Unbounded Array Growth (16MB Document Limit Exceeded)

### 🚨 Symptom
> Inserts crash with `BSONObjectTooLarge: Document size is larger than maximum 16777216`.

### 🔍 Root Cause Analysis
An array of orders, comments, or sensor readings was embedded directly inside a parent document without capping, eventually breaching MongoDB's 16MB document size limit.

### 🛠️ Production Fix & Mitigation Runbook
Refactor to the **Time-Series Bucket Pattern** (e.g., store 500 readings per document bucket) or switch to 1:N referencing with a foreign key in the child documents.

---

## 2. Accidental Full Collection Scan (COLLSCAN)

### 🚨 Symptom
> CPU usage spikes to 100% on MongoDB servers as traffic grows.

### 🔍 Root Cause Analysis
Queries are missing index support or use unindexed sorting fields, forcing MongoDB to load millions of documents into RAM.

### 🛠️ Production Fix & Mitigation Runbook
Run `explain('executionStats')` on slow queries to verify stage transition from `COLLSCAN` to `IXSCAN` or `FETCH` with `totalDocsExamined` matching `nReturned`.

---

## 3. Schema Validation Silent Insert Rejections

### 🚨 Symptom
> Application writes fail with `WriteError: Document failed validation`.

### 🔍 Root Cause Analysis
A collection with strict `$jsonSchema` validation was updated with mismatched data types (e.g., string instead of int for an age field).

### 🛠️ Production Fix & Mitigation Runbook
Inspect collection validation rules with `db.getCollectionInfos({name: 'coll'})` and adjust validation action to `warn` in staging before enforcing `strict`.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
