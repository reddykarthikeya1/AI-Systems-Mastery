# Debug Lab Incident Report: Reported Overall Accuracy Contradicts the Raw Correct/Total Counts

- **Severity:** P1 Result Reporting Integrity
- **Affected Subsystem:** Module_09_Write_Research_Paper
- **Reported Impact:** A results table aggregates per-fold test accuracy across five evaluation folds of very different sizes into a single headline number for the paper. Recomputing the same headline number directly from the raw correct/total counts gives a strikingly different answer.

---

## 🚨 Observable Symptoms & Logs
```text
Paper draft states:
  'Our model achieves 77.0% overall test accuracy.'
Recomputed directly from raw correct/total counts across all 1040 examples:
  Actual overall accuracy: 46.5%
```
The two numbers are computed from the exact same underlying `fold_results` data, yet they disagree by roughly 30 percentage points.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_09_Write_Research_Paper/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_fold_aggregation.py
   ```
3. Compare the headline percentage to the one recomputed from raw counts.

---

## 🎯 Your Objective
1. Inspect `broken_fold_aggregation.py`'s `report_overall_accuracy()` function.
2. Compare it against `true_overall_accuracy()`, which is computed from the same `fold_results` list.
3. Formulate a hypothesis for why the two disagree so much, then check `ANSWERS.md`.
