# Debug Lab Solution & Forensic Post-Mortem

## Incident: Out-of-Order Message Processing Caused by Multi-Threaded Partition Consumption

---

### 🔍 Forensic Root Cause Analysis
Partition ordering is only guaranteed if a partition is consumed sequentially by a single thread. Spreading records from one partition across worker threads breaks causality.

---

### 🛠️ Production Corrective Action & Code Fix

```python
# To scale consumption while preserving per-entity order:
# 1. Ensure partition count >= consumer count.
# 2. If sub-dispatching within a consumer, hash entity_id to internal worker queues so all events
#    for user_123 are processed sequentially by the exact same worker thread.

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
