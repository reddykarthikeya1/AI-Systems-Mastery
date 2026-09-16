# Debug Lab: Forensic Analysis & Solution

## Incident: Split-Brain Dual Leader Election in Raft Cluster

### 🔍 Root Cause Analysis
Candidate node transitions to Leader after receiving 2 votes in a 5-node cluster, violating majority quorum ($N/2 + 1 = 3$).

### 🛠️ The Fix
Require strict majority: `if votes_received >= (len(self.nodes) // 2) + 1: self.become_leader()`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
