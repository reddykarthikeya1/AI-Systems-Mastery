# Debug Lab: Forensic Analysis & Solution

## Incident: Cluster-Wide Scatter-Gather Latency Spikes on Sharded MongoDB

### 🔍 Root Cause Analysis
High-frequency operational user profile queries filter on `email` instead of the collection shard key `tenant_id`, broadcasting every query to all 10 shards.

### 🛠️ The Fix
Include the shard key in the query filter: `db.users.find({'tenant_id': tenant, 'email': email})`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
