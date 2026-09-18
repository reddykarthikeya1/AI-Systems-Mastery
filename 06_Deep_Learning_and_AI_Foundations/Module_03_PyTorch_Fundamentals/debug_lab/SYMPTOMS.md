# Debug Lab Incident Report: Single-Parameter Model Oscillates Instead of Converging

- **Severity:** P2 Training Instability
- **Affected Subsystem:** Module_03_PyTorch_Fundamentals
- **Reported Impact:** A minimal "PyTorch-style" training loop fitting `y_hat = w * x`
  to the perfectly linear relationship `y = 2x` never settles near the true weight.
  It overshoots past the optimum, swings back below zero, and keeps oscillating for
  as long as training continues.

---

## Observable Symptoms & Logs
```text
Weight after each training step (should settle near 2.0):
  step 0: w = 1.4000
  step 1: w = 2.6600
  step 2: w = 3.5240
  step 3: w = 3.4736
  step 4: w = 2.5390
  step 5: w = 1.2811
  step 6: w = 0.4544
  step 7: w = 0.5552
  step 8: w = 1.5228
  step 9: w = 2.7767
Final weight: 2.7767
```
The weight overshoots 2.0 by step 1, keeps growing through step 2, then reverses and
swings past zero around step 6-7, before climbing again. It never damps toward a
stable value.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_03_PyTorch_Fundamentals/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_gradient_accumulation.py
   ```
3. Watch the weight trajectory grow and shrink instead of settling.

---

## Your Objective
1. Inspect `broken_gradient_accumulation.py`'s `train()` loop and the `Param` class.
2. Trace what happens to `p.grad` across successive calls to `backward()`.
3. Formulate a hypothesis for why the effective step size keeps changing, then check
   `ANSWERS.md`.
