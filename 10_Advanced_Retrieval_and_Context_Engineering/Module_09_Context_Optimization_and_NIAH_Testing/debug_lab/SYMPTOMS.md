# Debug Lab Incident Report: NIAH Depth-vs-Accuracy Chart Is Mislabeled Across the Board

- **Severity:** P2 Test Validity / Misleading Metrics
- **Affected Subsystem:** Module_09_Context_Optimization_and_NIAH_Testing
- **Reported Impact:** The needle-in-a-haystack benchmark reported that model
  retrieval accuracy "collapses at shallow context depths," which contradicted
  every other vendor's published NIAH results and triggered a (wrong) escalation
  about the model's near-start recall. The reported failures were actually
  happening at a completely different depth than labeled.

---

## Observable Symptoms & Logs
```text
Haystack length: 1900 chars, requested insertion depth: 10% (near the start
of the document).
Expected: the needle should land at roughly 10% of the way through the
document.
Actual measured depth after insertion: 88.1%
First 80 chars of the document: 'The library was quiet this afternoon. The library was quiet this afternoon. The '
Last 80 chars of the document:  'on. The library was quiet this afternoon. The library was quiet this afternoon. '
```
A needle requested at 10% depth (intended to land near the very start of the
document) is actually measured landing at 88.1% depth -- near the end. The
first 80 characters of the document contain no trace of the needle at all.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_09_Context_Optimization_and_NIAH_Testing/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_niah_depth.py
   ```
3. Observe that `actual_depth` is far from `requested_depth` -- specifically,
   observe the relationship between the two values as `requested_depth`
   approaches 0.0 versus 1.0.

---

## Your Objective
1. Inspect `insert_needle_at_depth()` and write out, for `depth_percent = 0.0`
   and `depth_percent = 1.0`, exactly what `insertion_index` evaluates to.
2. Compare those two extremes against what "0% depth" and "100% depth" ought
   to mean for a document.
3. Formulate a hypothesis for why the measured depth is roughly
   `1 - requested_depth`, then check `ANSWERS.md`.
