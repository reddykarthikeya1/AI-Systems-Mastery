# Debug Lab: Forensic Analysis & Solution

## Incident: ReadFailure Scanned Over 100,000 Tombstones

### 🔍 Root Cause Analysis
Application repeatedly deleted expired queue items using CQL DELETE in a high-volume polling loop, generating millions of tombstones that choked subsequent range scans.

### 🛠️ The Fix
Do not use Cassandra as a task queue; model data with TTL expiration on inserts and query using exact partition keys rather than broad range scans.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
