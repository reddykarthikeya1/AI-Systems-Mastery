# Debug Lab: Incident Report & Symptoms

## Incident: ProvisionedThroughputExceededException on Single Partition Key
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 15 LSM Trees Compaction DynamoDB

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_15_LSM_Trees_Compaction_DynamoDB/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_dynamo_hotkey.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_dynamo_hotkey.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
