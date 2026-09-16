# Debug Lab Incident Report: Daily Storage Arithmetic Underflows by Factor of 1000 Due to Megabyte/Mebibyte Unit Confusion

- **Severity:** P1 Production Infrastructure Misconfiguration
- **Affected Subsystem:** Module_00_System_Design_Fundamentals_Interview_Playbook
- **Reported Impact:** Disks ran out of space in month 2 after provisioning based on capacity math that confused decimal GB (10^9) with binary GiB (2^30) and omitted replication factor.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in interview_capacity_calculator.
Traceback (most recent call last):
  ...
RuntimeError: Daily Storage Arithmetic Underflows by Factor of 1000 Due to Megabyte/Mebibyte Unit Confusion
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_00_System_Design_Fundamentals_Interview_Playbook/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_interview_capacity_calculator.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_interview_capacity_calculator.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
