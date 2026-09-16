# Debug Lab: Forensic Analysis & Solution

## Incident: Deadlock 1213 on High Concurrency Multi-Row Updates

### 🔍 Root Cause Analysis
Application updates multiple inventory rows in arbitrary order (Thread A updates Item 10 then 20; Thread B updates Item 20 then 10), triggering cyclic lock waits.

### 🛠️ The Fix
Sort item IDs in ascending order in application code prior to issuing UPDATE statements: `for item_id in sorted(item_ids): ...`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
