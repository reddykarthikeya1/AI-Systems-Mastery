# Debug Lab Incident Report: Fused LayerNorm Under-Normalizes Off-Center Rows

- **Severity:** P1 Numerical Correctness
- **Affected Subsystem:** Module_07_Fused_Activations_and_Normalization
- **Reported Impact:** A "fused" single-pass LayerNorm kernel accumulates `sum(x)` and `sum(x*x)` in one loop (to avoid a second read of the row) and is checked against a straightforward two-pass reference LayerNorm on a 5-element row whose mean is 12, not 0. The fused kernel's normalized output barely resembles the reference output.

---

## 🚨 Observable Symptoms & Logs
```text
Input row: [10.0, 11.0, 12.0, 13.0, 14.0]
reference_layernorm: [-1.4142, -0.7071, 0.0, 0.7071, 1.4142]
fused_layernorm:     [-0.1655, -0.0828, 0.0, 0.0828, 0.1655]
Mismatched entries: 4 of 5
```
Both functions center the row on its mean before dividing (element 2, equal to the mean, comes out as `0.0` in both), but every other entry from `fused_layernorm` is roughly an order of magnitude smaller in magnitude than the reference. The two implementations are supposed to compute the exact same normalization.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_07_Fused_Activations_and_Normalization/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_fused_layernorm.py
   ```
3. Compare the `reference_layernorm` line against the `fused_layernorm` line, and check the mismatch count.

---

## 🎯 Your Objective
1. Inspect `broken_fused_layernorm.py`'s `fused_layernorm()` function, specifically how it derives `var` from the single-pass accumulators `sum_x` and `sum_x2`.
2. Work out the algebraic relationship between `E[X^2]`, `E[X]`, and `Var(X) = E[X^2] - (E[X])^2`, and what `fused_layernorm` actually computes for `var`.
3. Formulate a hypothesis for why the row's non-zero mean (12, not 0) makes the bug visible, then check `ANSWERS.md`.
