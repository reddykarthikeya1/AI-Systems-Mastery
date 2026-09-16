# Debug Lab: Forensic Analysis & Solution

## Incident: Dual-Write Inconsistency Between Relational DB and Redis Cache

### 🔍 Root Cause Analysis
Application updates database and then updates Redis in two uncoordinated calls. Redis network glitch drops cache update, leaving stale data forever.

### 🛠️ The Fix
Implement the Transactional Outbox pattern: write update and outbox event in the same ACID transaction, relaying to Redis via CDC.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
