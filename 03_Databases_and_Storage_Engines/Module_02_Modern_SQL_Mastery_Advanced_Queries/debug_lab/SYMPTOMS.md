# Debug Lab: Incident Report & Symptoms

## Incident: Running Total Generates Identical Duplicate Numbers on Duplicate Dates
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 02 Modern SQL Mastery Advanced Queries

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_02_Modern_SQL_Mastery_Advanced_Queries/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_window_query.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_window_query.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
