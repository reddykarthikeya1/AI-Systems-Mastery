# Debug Lab Solution & Forensic Post-Mortem

## Incident: Overselling Limited Stock Under High Concurrency Race Condition

---

### 🔍 Forensic Root Cause Analysis
Multiple threads checked `stock > 0` simultaneously before any thread decremented, allowing overselling.

---

### 🛠️ Production Corrective Action & Code Fix

```python
# Use atomic Redis DECR or SQL conditional update:
# UPDATE inventory SET stock = stock - 1 WHERE item_id = :id AND stock > 0;
# If rows_affected == 0, item is out of stock!

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
