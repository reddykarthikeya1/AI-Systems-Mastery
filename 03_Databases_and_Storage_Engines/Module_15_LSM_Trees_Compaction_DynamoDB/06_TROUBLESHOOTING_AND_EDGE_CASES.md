# Module 15 LSM Trees Compaction DynamoDB: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **LSM-Trees, Compaction & Amazon DynamoDB Single-Table Design**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. DynamoDB ProvisionedThroughputExceededException (Hot Key Throttle)

### 🚨 Symptom
> API requests fail with 400 ProvisionedThroughputExceededException during flash sales.

### 🔍 Root Cause Analysis
Thousands of concurrent writes targeted the exact same partition key (e.g. `PRODUCT#WIDGET`), exceeding the 1,000 WCU / 3,000 RCU per-partition limit.

### 🛠️ Production Fix & Mitigation Runbook
Implement **Write Sharding** (suffix partition key with random salt `PRODUCT#WIDGET#1` to `PRODUCT#WIDGET#10`) or use DynamoDB Accelerator (DAX) for read caching.

---

## 2. Write Amplification in Leveled LSM Compaction

### 🚨 Symptom
> Disk I/O latency spikes dramatically on SSDs running heavy write workloads.

### 🔍 Root Cause Analysis
As SSTables advance through levels (L0 to L6), compaction repeatedly reads and rewrites data blocks multiple times (write amplification often exceeding 10x-30x).

### 🛠️ Production Fix & Mitigation Runbook
Tune compaction strategy: switch from Leveled Compaction to Size-Tiered Compaction Strategy (STCS) or Time-Window Compaction Strategy (TWCS) for append-only workloads.

---

## 3. Silent False Positive Saturation in Bloom Filters

### 🚨 Symptom
> Read operations slow down because every read hits disk SSTables despite Bloom filters being present.

### 🔍 Root Cause Analysis
The Bloom filter was initialized with an expected capacity of 10,000 items, but 1,000,000 items were inserted, driving the false-positive rate towards 100%.

### 🛠️ Production Fix & Mitigation Runbook
Always size Bloom filter bit arrays dynamically based on expected element counts: $m = -\frac{n \ln p}{(\ln 2)^2}$.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
