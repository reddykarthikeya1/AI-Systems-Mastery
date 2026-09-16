# Module 20 AI Vector Databases pgvector Qdrant: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **AI Vector Databases: pgvector & Qdrant HNSW Similarity**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Un-Normalized Vectors Breaking Cosine Similarity

### 🚨 Symptom
> Vector search returns nonsensical nearest neighbors with incorrect similarity ranking.

### 🔍 Root Cause Analysis
Cosine distance calculations assume vectors are unit normalized or use dot product instead of true cosine distance.

### 🛠️ Production Fix & Mitigation Runbook
Normalize vector embeddings to unit length ($L_2$ norm = 1.0) before insertion or explicitly configure `Distance.COSINE` in index parameters.

---

## 2. HNSW Graph Disconnection Causing Catastrophic Recall Drop

### 🚨 Symptom
> Approximate Nearest Neighbor (ANN) search recall drops from 98% to 45%.

### 🔍 Root Cause Analysis
The HNSW parameter `ef_construction` or `m` was set too low during bulk insertion, causing disconnected graph clusters.

### 🛠️ Production Fix & Mitigation Runbook
Set `m = 16` or `32` and `ef_construction = 128` to `200` during index creation, and tune query-time `ef_search` for desired latency vs recall trade-offs.

---

## 3. pgvector IVFFlat Index Degradation After Data Growth

### 🚨 Symptom
> Query latency on pgvector increases 20x after inserting 500,000 new vectors.

### 🔍 Root Cause Analysis
An IVFFlat index partitions vectors into clusters based on centroids calculated *at index creation time*. Adding 10x more vectors invalidates centroid distributions.

### 🛠️ Production Fix & Mitigation Runbook
Rebuild the IVFFlat index (`REINDEX INDEX`) with `lists = sqrt(total_rows)` or switch to HNSW indexing (`CREATE INDEX USING hnsw`).

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
