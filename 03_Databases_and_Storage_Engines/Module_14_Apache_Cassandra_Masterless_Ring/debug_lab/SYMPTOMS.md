# Debug Lab: Incident Report & Symptoms

## Incident: ReadFailure Scanned Over 100,000 Tombstones
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 14 Apache Cassandra Masterless Ring

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_14_Apache_Cassandra_Masterless_Ring/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_cassandra_schema.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_cassandra_schema.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
