# Module 25 Final Capstone Polyglot Enterprise: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Enterprise Polyglot Persistence Platform Capstone**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Dual-Write Distributed Inconsistency

### 🚨 Symptom
> Database has customer order recorded, but search catalog and cache have no record of it.

### 🔍 Root Cause Analysis
Application executed two independent network writes: `db.save(order)` followed by `redis.set(order)`. The second call failed due to network timeout.

### 🛠️ Production Fix & Mitigation Runbook
Implement the **Transactional Outbox Pattern**: write the business record AND the event intent to an outbox table in the SAME relational ACID transaction, and relay events downstream asynchronously via CDC.

---

## 2. Cache Stampede (Thundering Herd) on Hot Key Expiration

### 🚨 Symptom
> Database CPU spikes to 100% and crashes the instant a high-traffic cache key expires.

### 🔍 Root Cause Analysis
Thousands of concurrent incoming requests experienced a cache miss simultaneously and all queried the primary database at the exact same millisecond.

### 🛠️ Production Fix & Mitigation Runbook
Implement **Mutex Locking** (using Redis SET NX) so only 1 worker queries the database while others wait, or use probabilistic early expiration (XFetch algorithm).

---

## 3. Stale Event Replay Overwriting Newer Data in Downstream Stores

### 🚨 Symptom
> Customer profile in Elasticsearch shows old address after updating it to a new address.

### 🔍 Root Cause Analysis
Out-of-order event delivery: Event 1 (update address to City B) was delayed by network jitter and processed after Event 2 (update address to City C).

### 🛠️ Production Fix & Mitigation Runbook
Enforce monotonic event versioning or timestamps in CDC payloads: downstream engines only apply mutations if `incoming_version > current_stored_version`.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
