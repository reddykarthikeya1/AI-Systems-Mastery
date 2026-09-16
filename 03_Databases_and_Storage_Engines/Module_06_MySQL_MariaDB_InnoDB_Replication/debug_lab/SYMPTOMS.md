# Debug Lab: Incident Report & Symptoms

## Incident: Deadlock 1213 on High Concurrency Multi-Row Updates
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 06 MySQL MariaDB InnoDB Replication

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_06_MySQL_MariaDB_InnoDB_Replication/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_innodb_order.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_innodb_order.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
