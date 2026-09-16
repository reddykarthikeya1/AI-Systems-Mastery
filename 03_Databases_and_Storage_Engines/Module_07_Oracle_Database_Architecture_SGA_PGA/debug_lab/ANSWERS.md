# Debug Lab: Forensic Analysis & Solution

## Incident: ORA-04031 Shared Pool Out of Memory via Literal SQL

### 🔍 Root Cause Analysis
Application constructs SQL dynamically using f-strings (`SELECT * FROM emp WHERE id = {emp_id}`), creating 100,000 unique unsharable execution plans in the Library Cache.

### 🛠️ The Fix
Use bind variables: `cur.execute('SELECT * FROM emp WHERE id = :id', {'id': emp_id})`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
