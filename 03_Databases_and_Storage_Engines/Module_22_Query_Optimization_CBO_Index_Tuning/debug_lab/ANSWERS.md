# Debug Lab: Forensic Analysis & Solution

## Incident: Full Table Scan Caused by Function Wrapping on Indexed Timestamp

### 🔍 Root Cause Analysis
Query filters on `WHERE DATE(created_at) = '2026-01-01'`, blinding the query optimizer to the B-Tree index on `created_at`.

### 🛠️ The Fix
Rewrite as a sargable range query: `WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02'`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
