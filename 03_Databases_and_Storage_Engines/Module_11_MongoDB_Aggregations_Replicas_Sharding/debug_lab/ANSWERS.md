# Debug Lab Solution & Forensic Post-Mortem

## Incident: Cluster-Wide Scatter-Gather Latency Spikes on Sharded MongoDB

---

### 🔍 Forensic Root Cause Analysis
The collection is sharded on `tenant_id`, but `query_by_email()` filters on
`email`, which is absent from the shard key. `mongos` cannot compute which
shard(s) could possibly contain a matching document from an `email` filter
alone, so it has no choice but to broadcast the query to every shard in the
cluster (scatter-gather) and merge the results, even though at most one
document anywhere actually matches.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def query_by_email_targeted(cluster, tenant_id, email):
    """Once the caller supplies tenant_id, mongos can target a single shard."""
    target_shard = cluster.shard_for(tenant_id)
    return [d for d in cluster.docs if d["email"] == email], {target_shard}
```

The durable fix is architectural: the hot lookup path needs to know (or look
up cheaply) the `tenant_id` before querying, or the collection needs a
secondary index/lookup collection keyed by `email` that resolves to
`tenant_id` first, so the expensive scatter-gather never runs on the hot path.

---

### 🛡️ Production Prevention Invariants
1. **Every hot query path must include the shard key** in its filter; audit
   query shapes against the shard key at code review time.
2. **`explain()` in CI** for sharded-collection queries, failing the build on
   `SHARD_MERGE`/scatter-gather stages for latency-sensitive paths.
3. **Maintain a secondary lookup path** (cache or index collection) for any
   field that legitimately needs point lookups outside the shard key.
