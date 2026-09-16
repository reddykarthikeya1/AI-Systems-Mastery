# Debug Lab: Incident Report & Symptoms

## Incident: Interconnect Saturation Due to Unpartitioned Workload
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 09 Oracle RAC DataGuard GoldenGate

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_09_Oracle_RAC_DataGuard_GoldenGate/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_rac_router.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_rac_router.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
