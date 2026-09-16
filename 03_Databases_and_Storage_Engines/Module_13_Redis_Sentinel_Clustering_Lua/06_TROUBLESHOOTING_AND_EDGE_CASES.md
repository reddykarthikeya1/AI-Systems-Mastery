# Module 13 Redis Sentinel Clustering Lua: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Redis High Availability: Sentinel, Clustering & Lua Scripting**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Lua Script Timeout & Busy Engine Errors

### 🚨 Symptom
> Redis becomes completely unresponsive, throwing `BUSY Redis is busy running a script`.

### 🔍 Root Cause Analysis
A custom Lua script contains an infinite loop, expensive table iteration, or slow operations that block the single-threaded Redis event loop.

### 🛠️ Production Fix & Mitigation Runbook
Keep Lua scripts strictly $O(1)$ or small $O(K)$, use `SCRIPT KILL` for read-only runaway scripts, or `SHUTDOWN NOSAVE` if mutations occurred.

---

## 2. Redis Cluster CROSSSLOT Keys in Request Don't Hash to the Same Slot

### 🚨 Symptom
> Multi-key operations (MGET, MSET, transactions) fail with `CROSSSLOT Keys in request don't hash to the same slot`.

### 🔍 Root Cause Analysis
In Redis Cluster, multi-key operations are only permitted if all keys hash to the exact same hash slot (0-16383).

### 🛠️ Production Fix & Mitigation Runbook
Use Redis **Hash Tags**: enclose the common partition identifier in curly braces, e.g. `{user:101}:profile` and `{user:101}:orders`.

---

## 3. Sentinel Split-Brain During Network Partition

### 🚨 Symptom
> Old master continues accepting writes while Sentinel promotes a new master, causing silent data loss upon partition healing.

### 🔍 Root Cause Analysis
Network partition separated old master from Sentinel quorum, but clients continued writing to the old master.

### 🛠️ Production Fix & Mitigation Runbook
Configure `min-replicas-to-write 1` and `min-replicas-max-lag 10` on the master to halt writes if at least one replica is not acknowledging replication.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
