# Debug Lab Solution & Forensic Post-Mortem

## Incident: Reported Overall Accuracy Contradicts the Raw Correct/Total Counts

---

### 🔍 Forensic Root Cause Analysis
`report_overall_accuracy()` averages the five *per-fold accuracy percentages* with equal weight, regardless of how many examples each fold contains. Because one fold has 1000 examples while the other four have only 10 each, that large, harder fold (45% accuracy) is diluted down to just one-fifth of the average instead of dominating it the way it dominates the actual example count. The correct "overall accuracy" is the total correct predictions divided by the total number of examples across all folds, i.e. a size-weighted average -- exactly what `true_overall_accuracy()` computes.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def report_overall_accuracy(results):
    total_correct = sum(correct for correct, _ in results)
    total_examples = sum(total for _, total in results)
    return total_correct / total_examples
```

With the metric weighted by fold size, the reported headline number matches the number recomputed from raw counts exactly.

---

### 🛡️ Production Prevention Invariants
1. **Weighted-Metric Review:** Whenever aggregating a metric across groups of unequal size, default to weighting by group size unless there's a documented reason not to.
2. **Cross-Check Against Raw Counts:** Always recompute headline metrics directly from raw correct/total counts as a sanity check before publishing a number.
3. **Report Fold Sizes:** Publish per-fold sample sizes alongside per-fold accuracy so reviewers can catch an unweighted average at a glance.
