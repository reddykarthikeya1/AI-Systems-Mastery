# Debug Lab: Incident Report & Symptoms

## Incident: Dead Tuple Bloat Prevents Autovacuum Reclamation
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 05 PostgreSQL MVCC Indexing EXPLAIN

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_05_PostgreSQL_MVCC_Indexing_EXPLAIN/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_mvcc_purger.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_mvcc_purger.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
