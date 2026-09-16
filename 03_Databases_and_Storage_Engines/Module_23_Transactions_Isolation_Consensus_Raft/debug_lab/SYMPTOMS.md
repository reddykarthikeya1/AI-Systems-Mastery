# Debug Lab: Incident Report & Symptoms

## Incident: Split-Brain Dual Leader Election in Raft Cluster
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 23 Transactions Isolation Consensus Raft

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_23_Transactions_Isolation_Consensus_Raft/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_raft_vote.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_raft_vote.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
