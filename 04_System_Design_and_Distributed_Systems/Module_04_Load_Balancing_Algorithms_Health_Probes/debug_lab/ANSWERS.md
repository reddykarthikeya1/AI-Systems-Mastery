# Debug Lab Solution & Forensic Post-Mortem

## Incident: Load Balancer Cascading Collapse via Unhealthy Server Flapping

---

### 🔍 Forensic Root Cause Analysis
Binary instantaneous health checks without hysteresis cause healthy servers operating near capacity to be prematurely marked dead, redirecting load to remaining servers and killing the whole cluster.

---

### 🛠️ Production Corrective Action & Code Fix

```python
# Require consecutive failure threshold (hysteresis)
# Never evict more than a maximum fraction (e.g. 33%) of the pool simultaneously (outlier detection).

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
