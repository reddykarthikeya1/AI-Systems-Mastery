# Module 14 Apache Cassandra Masterless Ring: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Apache Cassandra & ScyllaDB: Masterless Ring & Wide-Column**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Tombstone Overload & Scanned Over 100,000 Tombstones Error

### 🚨 Symptom
> Range queries fail with `ReadFailure: Scanned over 100000 tombstones in table; query aborted`.

### 🔍 Root Cause Analysis
Frequent DELETE operations or expiring TTL data create tombstones. When querying, Cassandra scans through all tombstones to find alive rows, degrading memory and CPU.

### 🛠️ Production Fix & Mitigation Runbook
Avoid using Cassandra as a message queue; optimize partition key filtering to prevent broad range scans; lower `gc_grace_seconds` on dedicated write-heavy keyspaces and tune compaction.

---

## 2. Hot Partition Due to Low-Cardinality Partition Key

### 🚨 Symptom
> One Cassandra node runs at 95% disk and CPU while other 9 nodes in the cluster sit idle at 5%.

### 🔍 Root Cause Analysis
A partition key with low cardinality (e.g. `status` or `country`) caused millions of rows to route to a single token range on a single physical node.

### 🛠️ Production Fix & Mitigation Runbook
Create a composite partition key combining the category with a time bucket or salt: `PRIMARY KEY ((category, date_bucket), item_id)`.

---

## 3. WriteTimeoutException with ConsistencyLevel.ALL

### 🚨 Symptom
> Writes fail whenever a single node undergoes maintenance or restarts.

### 🔍 Root Cause Analysis
Using `ConsistencyLevel.ALL` requires acknowledgments from every single replica in the replication factor, completely sacrificing High Availability.

### 🛠️ Production Fix & Mitigation Runbook
Use `ConsistencyLevel.QUORUM` or `LOCAL_QUORUM` to satisfy strict consistency ($R + W > N$) while tolerating node failures.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
