# Debug Lab Solution & Forensic Post-Mortem

## Incident: Duplicate Snowflake IDs Generated During NTP Backward Time Leap

---

### 🔍 Forensic Root Cause Analysis
NTP time synchronization can jump backwards. If the generator does not refuse or wait until the clock catches up, it generates duplicate IDs.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def safe_generate_id(last_ts: int, current_ts: int, sequence: int):
    if current_ts < last_ts:
        drift = last_ts - current_ts
        if drift < 5:  # Tolerate tiny drift by busy-waiting
            import time; time.sleep(drift / 1000.0)
            current_ts = last_ts
        else:
            raise RuntimeError(f"Clock moved backwards by {drift}ms! Refusing generation.")
    return (current_ts << 22) | sequence

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
