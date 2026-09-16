# Debug Lab: Incident Report & Symptoms

## Incident: Deadlock in Concurrent B+ Tree Node Split
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 21 Storage Engine Internals BPlus Trees

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_21_Storage_Engine_Internals_BPlus_Trees/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_bplus_split.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_bplus_split.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
