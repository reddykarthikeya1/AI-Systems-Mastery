# Debug Lab Incident Report: TCP Head-of-Line Blocking and Socket Exhaustion Under High Concurrency

- **Severity:** P1 Gateway Starvation
- **Affected Subsystem:** Module_02_Network_Protocols_Transport_API_Paradigms
- **Reported Impact:** HTTP/2 connection over high-packet-loss mobile networks stalls all multiplexed streams when a single TCP packet is dropped.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in rpc_protocol_engine.
Traceback (most recent call last):
  ...
RuntimeError: TCP Head-of-Line Blocking and Socket Exhaustion Under High Concurrency
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_02_Network_Protocols_Transport_API_Paradigms/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_rpc_protocol_engine.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_rpc_protocol_engine.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
