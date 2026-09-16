# Module 21 Storage Engine Internals BPlus Trees: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Storage Engine Internals: Disk Pages & B+ Trees**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Off-By-One Key Search in Slotted Pages

### 🚨 Symptom
> Point lookups fail to find newly inserted keys or return adjacent incorrect records.

### 🔍 Root Cause Analysis
Binary search on slotted page key offsets failed to account for upper-bound vs lower-bound binary search semantics when keys match.

### 🛠️ Production Fix & Mitigation Runbook
Implement `bisect_right` or strict equality comparison and verify boundary conditions with property-based testing (Hypothesis).

---

## 2. Deadlocks During Concurrent Node Splitting

### 🚨 Symptom
> Multi-threaded B+ Tree threads hang permanently under heavy write load.

### 🔍 Root Cause Analysis
Lock crabbing (coupling) acquired child locks without maintaining strict top-down root-to-leaf hierarchy, causing cyclic lock wait states.

### 🛠️ Production Fix & Mitigation Runbook
Enforce strict lock coupling: acquire child lock before releasing parent lock, and release parent only when child is guaranteed not to split.

---

## 3. Buffer Pool Dirty Page Eviction Without WAL Flush

### 🚨 Symptom
> Database crashes cause unrecoverable corruption and violates ACID Durability.

### 🔍 Root Cause Analysis
The buffer pool evicted a dirty data frame to disk before the corresponding WAL log record was flushed (violating the Write-Ahead Logging invariant).

### 🛠️ Production Fix & Mitigation Runbook
Strictly enforce WAL rule: `page.page_lsn <= flushed_to_disk_lsn` before allowing buffer pool manager to write any frame to disk.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
