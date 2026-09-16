# Debug Lab Incident Report: Bloom Filter False Positive Rate Explodes Beyond Expected Bounds

- **Severity:** P2 Performance Degradation
- **Affected Subsystem:** Module_12_Probabilistic_Data_Structures
- **Reported Impact:** Cache bypass rate increased from 1% to 45% because the Bloom Filter was sized for 100,000 items but was fed 2,000,000 items.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in probabilistic_structures.
Traceback (most recent call last):
  ...
RuntimeError: Bloom Filter False Positive Rate Explodes Beyond Expected Bounds
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_12_Probabilistic_Data_Structures/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_probabilistic_structures.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_probabilistic_structures.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
