# Debug Lab: Incident Report & Symptoms

## Incident: Sequential Scan on 5,000,000 JSONB Document Catalog
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 04 PostgreSQL Core Advanced Types

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_04_PostgreSQL_Core_Advanced_Types/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_jsonb_filter.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_jsonb_filter.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
