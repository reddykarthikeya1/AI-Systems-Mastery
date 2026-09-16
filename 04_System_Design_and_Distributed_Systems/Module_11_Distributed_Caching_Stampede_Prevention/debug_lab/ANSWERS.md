# Debug Lab Solution & Forensic Post-Mortem

## Incident: Cache Stampede Crashes Primary Database on Hot Key Expiration

---

### 🔍 Forensic Root Cause Analysis
Cache-aside without request coalescing allows all concurrent callers to experience a cache miss at the exact same millisecond and hammer the backend.

---

### 🛠️ Production Corrective Action & Code Fix

```python
# Use SingleFlight / Mutex Request Coalescing:
# In-flight calls for key 'k' share a single future/promise;
# exactly 1 request hits the database while the other 4,999 await its result.

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
