# Debug Lab Incident Report: Penny Discrepancy Leak in Three-Way Bill Split

- **Severity:** P1 Financial Ledger Discrepancy
- **Affected Subsystem:** Module_08_LLD_Financial_Engines_Splitwise_Rate_Limiting
- **Reported Impact:** Splitting a $100.00 bill three ways results in $33.33 each, leaving $0.01 unallocated and breaking double-entry zero-sum balance.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in splitwise_engine.
Traceback (most recent call last):
  ...
RuntimeError: Penny Discrepancy Leak in Three-Way Bill Split
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_08_LLD_Financial_Engines_Splitwise_Rate_Limiting/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_splitwise_engine.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_splitwise_engine.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
