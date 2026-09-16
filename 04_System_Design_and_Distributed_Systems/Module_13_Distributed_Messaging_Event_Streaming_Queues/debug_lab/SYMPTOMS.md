# Debug Lab Incident Report: Out-of-Order Message Processing Caused by Multi-Threaded Partition Consumption

- **Severity:** P0 State Inconsistency
- **Affected Subsystem:** Module_13_Distributed_Messaging_Event_Streaming_Queues
- **Reported Impact:** User's `ORDER_CANCELLED` event was processed before `ORDER_CREATED`, resulting in a phantom charge that was never cancelled.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in commit_log_stream.
Traceback (most recent call last):
  ...
RuntimeError: Out-of-Order Message Processing Caused by Multi-Threaded Partition Consumption
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_13_Distributed_Messaging_Event_Streaming_Queues/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_commit_log_stream.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_commit_log_stream.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
