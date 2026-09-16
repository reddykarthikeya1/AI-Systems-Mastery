# Debug Lab Incident Report: Split-Vote Deadlock in Raft Leader Election Without Timeout Jitter

- **Severity:** P1 Cluster Unavailable
- **Affected Subsystem:** Module_24_Distributed_Consensus_Raft_Vector_Clocks
- **Reported Impact:** A 5-node Raft cluster remained leaderless for 30 minutes because all nodes had identical 150ms election timeouts and split the vote every term.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in raft_cluster_engine.
Traceback (most recent call last):
  ...
RuntimeError: Split-Vote Deadlock in Raft Leader Election Without Timeout Jitter
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_24_Distributed_Consensus_Raft_Vector_Clocks/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_raft_cluster_engine.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_raft_cluster_engine.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
