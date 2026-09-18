# Debug Lab Incident Report: Parallel Tree Reduction Returns the Wrong Total for Non-Power-of-2 Input

- **Severity:** P1 Numerical Correctness
- **Affected Subsystem:** Module_04_Parallel_Reduction_and_Prefix_Sum
- **Reported Impact:** A classic doubling-stride tree reduction is used to sum an array in O(log n) passes. For power-of-2 sized inputs it works fine, but for an array whose length is not a power of two, the returned sum silently disagrees with the plain `sum()` of the same data.

---

## 🚨 Observable Symptoms & Logs
```text
Input array: [3, 1, 4, 1, 5, 9]
Tree-reduction result: 23
sum(data) reference:   23
```
`data` has 6 elements. The tree-reduction result and the `sum(data)` reference should be identical -- they are summing the same numbers.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_04_Parallel_Reduction_and_Prefix_Sum/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_tree_reduction.py
   ```
3. Compare the 'Tree-reduction result' line to the 'sum(data) reference' line.

---

## 🎯 Your Objective
1. Inspect `broken_tree_reduction.py`'s `tree_reduce_sum()` function.
2. Trace through the `stride`/`i` loop by hand for `n=6` and note exactly which array indices get added together at each stride.
3. Formulate a hypothesis for which element(s) never make it into the total, then check `ANSWERS.md`.
