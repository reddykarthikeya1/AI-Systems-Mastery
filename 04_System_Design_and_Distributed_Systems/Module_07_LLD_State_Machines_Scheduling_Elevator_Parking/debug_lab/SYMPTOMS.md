# Debug Lab Incident Report: Elevator Starvation Under Upward Continuous Hall Calls

- **Severity:** P2 Starvation Anomaly
- **Affected Subsystem:** Module_07_LLD_State_Machines_Scheduling_Elevator_Parking
- **Reported Impact:** A passenger waiting on Floor 1 to go Down is ignored indefinitely because new requests on Floor 2 and 3 keep summoning the elevator Up.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in elevator_system.
Traceback (most recent call last):
  ...
RuntimeError: Elevator Starvation Under Upward Continuous Hall Calls
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_07_LLD_State_Machines_Scheduling_Elevator_Parking/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_elevator_system.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_elevator_system.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
