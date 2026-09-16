# Debug Lab: Incident Report & Symptoms

## Incident: Uncommitted Transaction Leaks into Primary Table During Power Failure
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 01 Storage Theory ACID Relational Model

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_01_Storage_Theory_ACID_Relational_Model/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_csv_engine.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_csv_engine.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
