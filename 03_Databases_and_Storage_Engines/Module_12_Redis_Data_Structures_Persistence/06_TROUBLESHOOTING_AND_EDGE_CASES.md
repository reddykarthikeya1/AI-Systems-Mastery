# Module 12 Redis Data Structures Persistence: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Redis Internals: Data Structures, RDB/AOF & Sliding Windows**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. OOM Command Not Allowed (MaxMemory Reached)

### 🚨 Symptom
> Redis commands start failing with `OOM command not allowed when used memory > 'maxmemory'`.

### 🔍 Root Cause Analysis
Redis memory reached `maxmemory` threshold and the eviction policy was set to `noeviction`.

### 🛠️ Production Fix & Mitigation Runbook
Configure an appropriate eviction policy such as `volatile-lru` or `allkeys-lru`, ensure all transient keys have explicit TTLs, and monitor memory fragmentation ratio with `INFO memory`.

---

## 2. RDB Fork Hang & System Memory Exhaustion

### 🚨 Symptom
> Redis latency spikes by hundreds of milliseconds every 15 minutes during background snapshots.

### 🔍 Root Cause Analysis
`BGSAVE` calls `fork()`, which duplicates page tables. If the Linux kernel has `vm.overcommit_memory = 0`, the fork fails or triggers massive copy-on-write page swapping.

### 🛠️ Production Fix & Mitigation Runbook
Set `sysctl vm.overcommit_memory = 1` in `/etc/sysctl.conf` and disable transparent huge pages (`transparent_hugepage = never`).

---

## 3. Hot Key CPU Core Saturation

### 🚨 Symptom
> Single Redis CPU core is pinned at 100% while all other cores are idle.

### 🔍 Root Cause Analysis
A single hot key (e.g., a massive celebrity follower set or global counter) receives 100,000 requests/sec, bottlenecking the single-threaded Redis event loop.

### 🛠️ Production Fix & Mitigation Runbook
Implement local in-memory caching (e.g., Python `cachetools`) with 1-second TTL, or shard the hot key across multiple keys (`counter:1`, `counter:2`, etc.).

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
