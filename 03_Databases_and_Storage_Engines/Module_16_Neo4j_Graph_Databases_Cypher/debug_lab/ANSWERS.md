# Debug Lab: Forensic Analysis & Solution

## Incident: Cartesian Product OutOfMemoryError in Cypher Path Match

### 🔍 Root Cause Analysis
Query written as `MATCH (a:Person), (b:Company) WHERE a.city = b.city` without a relationship pattern, forcing an exhaustive $N \times M$ Cartesian product in RAM.

### 🛠️ The Fix
Rewrite query to match explicit graph relationships or use an index-supported subquery.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
