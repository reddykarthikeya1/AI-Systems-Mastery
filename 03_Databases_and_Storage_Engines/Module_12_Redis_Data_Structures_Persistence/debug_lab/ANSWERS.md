# Debug Lab: Forensic Analysis & Solution

## Incident: Distributed Lock Race Condition Releases Another Worker's Lock

### 🔍 Root Cause Analysis
Worker acquires lock with `SET lock_key 1 EX 10`. Worker takes 12 seconds to finish. Lock expires. Worker 2 acquires lock. Worker 1 then calls `DEL lock_key`, releasing Worker 2's lock prematurely.

### 🛠️ The Fix
Store a unique UUID token as the lock value and release exclusively via an atomic Lua script verifying token ownership before deleting.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
