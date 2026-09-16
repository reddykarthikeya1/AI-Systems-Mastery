# Debug Lab Solution & Forensic Post-Mortem

## Incident: Daily Storage Arithmetic Underflows by Factor of 1000 Due to Megabyte/Mebibyte Unit Confusion

---

### 🔍 Forensic Root Cause Analysis
The calculation divided by 10^6 instead of 1024^3 (GiB) or 10^9 (GB) and completely omitted multiplying by the storage replication factor (3x). This led to severe disk exhaustion in production.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def calculate_provisioned_storage(qps: int, payload_bytes: int, days: int, replication_factor: int = 3) -> float:
    daily_bytes = qps * payload_bytes * 86400 * replication_factor
    total_bytes = daily_bytes * days
    gib = total_bytes / (1024 ** 3)
    return round(gib, 2)

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
