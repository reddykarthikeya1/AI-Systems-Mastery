# Debug Lab: Forensic Analysis & Solution

## Incident: Deep Pagination Offset Crashes Elasticsearch Data Nodes

### 🔍 Root Cause Analysis
Application paginates search results using `from: 50000, size: 50`, exhausting coordinator node heap memory.

### 🛠️ The Fix
Use the `search_after` API with tie-breaker sorting or Point-In-Time (PIT) searches instead of high `from` offsets.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
