# Debug Lab: Incident Report & Symptoms

## Incident: CROSSSLOT Keys in Request Don't Hash to the Same Slot
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 13 Redis Sentinel Clustering Lua

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_13_Redis_Sentinel_Clustering_Lua/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_redis_cluster.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_redis_cluster.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
