# Debug Lab Incident Report: Distributed Trace Context Dropped Across Asynchronous Thread Handoff

- **Severity:** P2 Telemetry Blindspot
- **Affected Subsystem:** Module_25_Observability_Distributed_Tracing_SRE
- **Reported Impact:** Distributed trace graphs showed disconnected orphan spans because background worker threads were dispatched without copying `traceparent` context.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in resilience_telemetry.
Traceback (most recent call last):
  ...
RuntimeError: Distributed Trace Context Dropped Across Asynchronous Thread Handoff
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_25_Observability_Distributed_Tracing_SRE/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_resilience_telemetry.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_resilience_telemetry.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
