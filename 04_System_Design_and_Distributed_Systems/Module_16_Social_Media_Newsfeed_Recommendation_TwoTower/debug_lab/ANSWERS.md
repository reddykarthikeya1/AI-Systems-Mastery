# Debug Lab Solution & Forensic Post-Mortem

## Incident: Write Amplification Catastrophe on Celebrity Fan-Out

---

### 🔍 Forensic Root Cause Analysis
Pure Push (Fan-out-on-Write) works well for normal users, but scales linearly with follower count. For celebrities, $50M$ writes for 1 post saturates storage and queues.

---

### 🛠️ Production Corrective Action & Code Fix

```python
# Implement Hybrid Fan-Out:
# - Normal users (< 25,000 followers): Fan-out-on-Write (Push to follower timelines).
# - Celebrities (>= 25,000 followers): Do NOT push!
#   Merge celebrity posts at READ time when the follower opens their feed (Fan-out-on-Read).

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
