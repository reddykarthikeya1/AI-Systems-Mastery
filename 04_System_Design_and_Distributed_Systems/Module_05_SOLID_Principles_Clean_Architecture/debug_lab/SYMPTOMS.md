# Debug Lab Incident Report: Inventory Over-Reservation Rollback Failure on Payment Exception

- **Severity:** P1 Inventory Inconsistency
- **Affected Subsystem:** Module_05_SOLID_Principles_Clean_Architecture
- **Reported Impact:** Customers whose credit cards declined still had inventory reserved permanently, leading to false out-of-stock errors.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in clean_checkout.
Traceback (most recent call last):
  ...
RuntimeError: Inventory Over-Reservation Rollback Failure on Payment Exception
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_05_SOLID_Principles_Clean_Architecture/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_clean_checkout.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_clean_checkout.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
