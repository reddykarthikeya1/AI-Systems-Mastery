# Module 19 Search Engines Elasticsearch Lucene: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Search Engines: Elasticsearch, Lucene & Inverted Indexes**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Elasticsearch Cluster Red: Unassigned Shards

### 🚨 Symptom
> Elasticsearch cluster status turns RED and queries return 503 Service Unavailable.

### 🔍 Root Cause Analysis
Primary shards cannot be allocated due to disk watermarks (`cluster.routing.allocation.disk.watermark.flood_stage` exceeded 95%) or node network partition.

### 🛠️ Production Fix & Mitigation Runbook
Free disk space on data nodes, clear read-only blocks with `PUT /*/_settings {"index.blocks.read_only_allow_delete": null}`, and check shard allocation with `GET _cluster/allocation/explain`.

---

## 2. Mapping Explosion in Dynamic Indexing

### 🚨 Symptom
> Master node CPU spikes to 100% and cluster state updates take seconds.

### 🔍 Root Cause Analysis
Dynamic indexing allowed arbitrary JSON payloads with thousands of unique keys to create separate field mappings, breaching the 1,000 fields limit.

### 🛠️ Production Fix & Mitigation Runbook
Set `"dynamic": "strict"` or `"dynamic": false` in index mappings and map unpredictable key-value pairs into nested `key`/`value` structures.

---

## 3. Deep Pagination OOM via from + size

### 🚨 Symptom
> Search query with `from: 50000, size: 50` crashes Elasticsearch data nodes.

### 🔍 Root Cause Analysis
Deep pagination requires every shard to sort and return 50,050 documents to the coordinator node, which then merges and discards 50,000 records.

### 🛠️ Production Fix & Mitigation Runbook
Use the `search_after` API with tie-breaker sorting or Point-In-Time (PIT) searches instead of high `from` offsets.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
