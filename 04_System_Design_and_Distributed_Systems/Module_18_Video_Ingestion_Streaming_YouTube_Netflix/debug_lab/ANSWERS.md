# Debug Lab Solution & Forensic Post-Mortem

## Incident: Transcoding Worker OOM Crash on Unbounded Video Resolution Ingestion

---

### 🔍 Forensic Root Cause Analysis
Ingesting arbitrary user uploads without strict chunk size limits and streaming piping causes memory consumption to explode.

---

### 🛠️ Production Corrective Action & Code Fix

```python
# Enforce rigid multipart upload limits (e.g. 10MB chunks).
# Stream chunks through FFmpeg UNIX pipes rather than holding complete files in memory buffers.

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
