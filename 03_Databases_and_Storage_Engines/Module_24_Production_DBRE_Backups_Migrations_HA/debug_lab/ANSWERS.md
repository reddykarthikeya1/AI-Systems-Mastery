# Debug Lab: Forensic Analysis & Solution

## Incident: Exclusive Table Lock Starvation During Online Schema Migration

### 🔍 Root Cause Analysis
Migration script runs `ALTER TABLE orders ADD COLUMN status_code INT;` without a lock_timeout, blocking behind a slow query and queuing all incoming web requests.

### 🛠️ The Fix
Set strict lock timeout before running DDL: `SET lock_timeout = '2s'; ALTER TABLE ...`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
