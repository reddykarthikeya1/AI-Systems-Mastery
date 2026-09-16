# Debug Lab Incident Report: Dual-Write Inconsistency: Database Committed but Message Broker Publish Failed

- **Severity:** P1 Distributed Data Inconsistency
- **Affected Subsystem:** Module_23_Distributed_Transactions_Sagas_Outbox
- **Reported Impact:** User was billed in the relational database, but the downstream Kafka event was never published due to network timeout, leaving order pending forever.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in saga_orchestrator.
Traceback (most recent call last):
  ...
RuntimeError: Dual-Write Inconsistency: Database Committed but Message Broker Publish Failed
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_23_Distributed_Transactions_Sagas_Outbox/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_saga_orchestrator.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_saga_orchestrator.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
