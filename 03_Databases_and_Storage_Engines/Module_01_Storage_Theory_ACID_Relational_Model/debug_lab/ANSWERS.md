# Debug Lab: Forensic Analysis & Solution

## Incident: Uncommitted Transaction Leaks into Primary Table During Power Failure

### 🔍 Root Cause Analysis
The csv engine flushes uncommitted in-memory rows directly to table.csv during insert() rather than deferring until commit(). When a crash occurs before commit(), dirty data is permanently written.

### 🛠️ The Fix
Buffer all rows in self.uncommitted_rows and append to table.csv strictly inside commit() after logging the COMMIT entry to the WAL.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
