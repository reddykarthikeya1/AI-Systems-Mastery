# Debug Lab: Incident Report & Symptoms

## Incident: Database is Locked Exception on High Concurrent Ingestion
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 03 Embedded Databases SQLite WAL

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_03_Embedded_Databases_SQLite_WAL/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_wal_buffer.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_wal_buffer.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
