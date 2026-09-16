# Debug Lab: Incident Report & Symptoms

## Incident: ORA-04031 Shared Pool Out of Memory via Literal SQL
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 07 Oracle Database Architecture SGA PGA

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_07_Oracle_Database_Architecture_SGA_PGA/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_sga_cursor.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_sga_cursor.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
