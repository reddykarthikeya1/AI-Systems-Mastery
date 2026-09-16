# Debug Lab: Incident Report & Symptoms

## Incident: BSONObjectTooLarge Error on Unbounded Sensor Array
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 10 MongoDB Document Modeling BSON

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_10_MongoDB_Document_Modeling_BSON/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_mongo_bucket.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_mongo_bucket.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
