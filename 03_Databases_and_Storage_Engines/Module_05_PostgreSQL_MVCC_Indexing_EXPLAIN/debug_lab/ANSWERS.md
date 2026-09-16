# Debug Lab: Forensic Analysis & Solution

## Incident: Dead Tuple Bloat Prevents Autovacuum Reclamation

### 🔍 Root Cause Analysis
A long-running reporting session opened a transaction with `BEGIN; SELECT ...` and remained idle in transaction for 18 hours, pinning xmin and preventing autovacuum from cleaning dead tuples.

### 🛠️ The Fix
Configure `idle_in_transaction_session_timeout = '60s'` and terminate the lagging backend using `SELECT pg_terminate_backend(pid)`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
