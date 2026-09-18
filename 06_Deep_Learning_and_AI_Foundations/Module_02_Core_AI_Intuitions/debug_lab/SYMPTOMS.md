# Debug Lab Incident Report: Held-Out Accuracy Is Implausibly High

- **Severity:** P2 Evaluation Integrity
- **Affected Subsystem:** Module_02_Core_AI_Intuitions
- **Reported Impact:** A trivial memorization-based model reports held-out accuracy
  far above the majority-class baseline, even though the underlying data has no
  learnable structure beyond memorizing exact values.

---

## Observable Symptoms & Logs
```text
Train set size: 160, Test set size: 40
Indices present in BOTH train and test: 37
Majority-class baseline accuracy: 52.5%
Reported held-out accuracy: 95.0%
```
An evaluation that should hover near the 51% majority-class baseline instead reports
accuracy more than 30 points higher, and a nonzero number of dataset indices are
reported as belonging to both the train and test sets simultaneously.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_02_Core_AI_Intuitions/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_train_test_leakage.py
   ```
3. Compare the "Indices present in BOTH" count to what a correct held-out split
   should report.

---

## Your Objective
1. Inspect `broken_train_test_leakage.py`'s `train_test_split` function.
2. Work out what `train_idx` and `test_idx` are supposed to represent relative to
   each other, and how they are actually constructed.
3. Formulate a hypothesis for the inflated accuracy, then check `ANSWERS.md`.
