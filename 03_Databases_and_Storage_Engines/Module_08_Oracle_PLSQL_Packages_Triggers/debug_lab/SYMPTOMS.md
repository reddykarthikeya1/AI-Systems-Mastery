# Debug Lab: Incident Report & Symptoms

## Incident: Audit Log Erased When Financial Transaction Fails
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 08 Oracle PLSQL Packages Triggers

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_08_Oracle_PLSQL_Packages_Triggers/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_plsql_audit.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_plsql_audit.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
