# Debug Lab Incident Report: Tail Latency Amplification Cripples Microservice Fanout

- **Severity:** P1 Service Outage Under Fanout
- **Affected Subsystem:** Module_01_Physics_of_Scalability_Capacity_Math
- **Reported Impact:** User requests hitting a fanout aggregator take > 2 seconds even though every individual backend microservice reports p99 latency of 10ms.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in capacity_estimator.
Traceback (most recent call last):
  ...
RuntimeError: Tail Latency Amplification Cripples Microservice Fanout
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_01_Physics_of_Scalability_Capacity_Math/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_capacity_estimator.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_capacity_estimator.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
