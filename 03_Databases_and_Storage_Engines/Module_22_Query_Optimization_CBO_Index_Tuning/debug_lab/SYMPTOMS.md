# Debug Lab: Incident Report & Symptoms

## Incident: Full Table Scan Caused by Function Wrapping on Indexed Timestamp
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 22 Query Optimization CBO Index Tuning

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_22_Query_Optimization_CBO_Index_Tuning/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_query_index.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_query_index.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
