# Debug Lab: Forensic Analysis & Solution

## Incident: Audit Log Erased When Financial Transaction Fails

### 🔍 Root Cause Analysis
The security audit logging procedure was declared without `PRAGMA AUTONOMOUS_TRANSACTION`. When the parent transfer rolls back due to insufficient funds, the audit record is rolled back with it.

### 🛠️ The Fix
Add `PRAGMA AUTONOMOUS_TRANSACTION;` and an explicit `COMMIT;` inside the audit logger procedure body.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
