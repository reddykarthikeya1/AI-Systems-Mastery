# Module 09 Oracle RAC DataGuard GoldenGate: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Oracle RAC, Active Data Guard & Real-Time Replication**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. RAC Interconnect Congestion & gc buffer busy acquire

### 🚨 Symptom
> Query latency spikes across all RAC cluster nodes with high `gc cr request` waits.

### 🔍 Root Cause Analysis
Cache Fusion pinging: multiple nodes are concurrently writing to the same data blocks, causing the Global Cache Service (GCS) to constantly transfer dirty blocks back and forth over the private interconnect.

### 🛠️ Production Fix & Mitigation Runbook
Partition workload at the application tier using Oracle Services so specific business domains execute on dedicated instances, avoiding cross-instance block contention.

---

## 2. Data Guard Transport Lag & Standby Desynchronization

### 🚨 Symptom
> Active Data Guard standby lags behind primary by hours, risking data loss (RPO breach).

### 🔍 Root Cause Analysis
Network throughput between primary and standby data centers is saturated or redo transport service is misconfigured.

### 🛠️ Production Fix & Mitigation Runbook
Tune `redo_transport_user`, configure multiple archiver processes (`LOG_ARCHIVE_MAX_PROCESSES`), and set protection mode to `MAXIMUM AVAILABILITY` with synchronous standby redo logs (SRLs).

---

## 3. Split-Brain Scenario During RAC Node Eviction

### 🚨 Symptom
> A node is evicted from the RAC cluster, but continues attempting to write to shared storage.

### 🔍 Root Cause Analysis
Network heartbeat was lost over interconnect, but storage fencing (STONITH / CSS voting disks) failed to isolate the node.

### 🛠️ Production Fix & Mitigation Runbook
Ensure dedicated, redundant physical network switches for RAC private interconnects and verify voting disk quorum configurations.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
