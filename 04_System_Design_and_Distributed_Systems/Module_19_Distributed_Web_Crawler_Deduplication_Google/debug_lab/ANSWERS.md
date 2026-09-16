# Debug Lab Solution & Forensic Post-Mortem

## Incident: Infinite Spider Trap Exhausts Crawler Memory and Storage

---

### 🔍 Forensic Root Cause Analysis
Dynamic websites generate infinite valid URLs. Without URL normalization, path depth limits, and trap detection, crawlers get trapped.

---

### 🛠️ Production Corrective Action & Code Fix

```python
# 1. Enforce strict max path depth (e.g. max 8 slashes).
# 2. Limit maximum pages crawled per domain/host.
# 3. Detect repeating directory patterns (`/a/b/a/b/a/b`).
# 4. Strictly respect per-host Crawl-delay in robots.txt.

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
