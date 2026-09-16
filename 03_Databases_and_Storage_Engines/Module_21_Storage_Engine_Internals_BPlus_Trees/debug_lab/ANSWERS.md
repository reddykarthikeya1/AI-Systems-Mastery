# Debug Lab: Forensic Analysis & Solution

## Incident: Deadlock in Concurrent B+ Tree Node Split

### 🔍 Root Cause Analysis
Writer released parent latch before acquiring child latch during downward traversal, allowing a concurrent split to invalidate node pointers.

### 🛠️ The Fix
Enforce strict lock coupling (crabbing): do not release parent lock until child lock is acquired and confirmed safe from splitting.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
