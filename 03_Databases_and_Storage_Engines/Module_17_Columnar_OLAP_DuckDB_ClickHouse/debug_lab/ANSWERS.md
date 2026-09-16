# Debug Lab: Forensic Analysis & Solution

## Incident: DB::Exception: Too Many Parts in Table in ClickHouse

### 🔍 Root Cause Analysis
Microservice sends 5,000 single-row HTTP INSERT requests per second to ClickHouse MergeTree, exhausting background merge worker capacity.

### 🛠️ The Fix
Batch inserts into chunks of at least 10,000 rows before sending to ClickHouse, or insert into a Buffer engine table.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
