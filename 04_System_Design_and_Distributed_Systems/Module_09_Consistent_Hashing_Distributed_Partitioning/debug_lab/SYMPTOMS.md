# Debug Lab Incident Report: Hot Partition Cascade Triggered by Inadequate Virtual Node Density

- **Severity:** P1 Storage Node Failure
- **Affected Subsystem:** Module_09_Consistent_Hashing_Distributed_Partitioning
- **Reported Impact:** Node 3 receives 72% of all cache writes in a 5-node cluster, causing OOM crashes, while Node 1 sits at 4% utilization.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in consistent_hash_ring.
Traceback (most recent call last):
  ...
RuntimeError: Hot Partition Cascade Triggered by Inadequate Virtual Node Density
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_09_Consistent_Hashing_Distributed_Partitioning/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_consistent_hash_ring.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_consistent_hash_ring.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
