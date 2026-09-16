# Debug Lab: Incident Report & Symptoms

## Incident: Exclusive Table Lock Starvation During Online Schema Migration
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 24 Production DBRE Backups Migrations HA

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_24_Production_DBRE_Backups_Migrations_HA/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_migration_lock.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_migration_lock.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
