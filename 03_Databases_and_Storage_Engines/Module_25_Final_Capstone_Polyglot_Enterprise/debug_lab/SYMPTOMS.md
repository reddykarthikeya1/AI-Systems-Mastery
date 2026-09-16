# Debug Lab: Incident Report & Symptoms

## Incident: Dual-Write Inconsistency Between Relational DB and Redis Cache
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 25 Final Capstone Polyglot Enterprise

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_25_Final_Capstone_Polyglot_Enterprise/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_polyglot_sync.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_polyglot_sync.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
