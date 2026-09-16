# Module 11 MongoDB Aggregations Replicas Sharding: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **MongoDB Aggregation Pipelines, Replication & Sharding**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Aggregation Pipeline 100MB Memory Limit Exceeded

### 🚨 Symptom
> Complex `$sort` or `$group` aggregation crashes with `Exceeded memory limit for $sort (104857600 bytes)`.

### 🔍 Root Cause Analysis
In-memory aggregation stages exceed the 100MB RAM safety cap when sorting large datasets without an index.

### 🛠️ Production Fix & Mitigation Runbook
Place `$match` and `$limit` as early in the pipeline as possible to minimize working set size, build an index matching the sort key, or enable `{allowDiskUse: true}`.

---

## 2. Scatter-Gather Sharding Degradation

### 🚨 Symptom
> Queries take seconds to execute across a 10-shard cluster even for single-item lookups.

### 🔍 Root Cause Analysis
The query filter does not include the cluster's **Shard Key**, forcing the `mongos` router to broadcast the query to every single shard in the cluster (scatter-gather).

### 🛠️ Production Fix & Mitigation Runbook
Ensure every targeted operational query includes the shard key (e.g. `tenant_id` or `customer_id`) so mongos routes directly to a single shard.

---

## 3. Replication Read Concern 'local' Stale Reads

### 🚨 Symptom
> Reading from secondary replicas returns outdated data that does not reflect recent writes.

### 🔍 Root Cause Analysis
Default read preference `secondaryPreferred` combined with `readConcern: local` reads uncommitted or lagging oplog frames.

### 🛠️ Production Fix & Mitigation Runbook
Use `readConcern: majority` and `writeConcern: majority` for strong read-after-write consistency guarantees.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
