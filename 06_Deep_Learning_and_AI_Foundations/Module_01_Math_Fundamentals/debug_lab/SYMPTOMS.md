# Debug Lab Incident Report: Linear Regression Loss Explodes Instead of Converging

- **Severity:** P2 Training Instability
- **Affected Subsystem:** Module_01_Math_Fundamentals
- **Reported Impact:** A textbook gradient-descent fit of `y = w*x + b` to a perfectly
  linear, noise-free dataset never converges. Every retrain produces larger loss than
  the last, regardless of learning rate.

---

## Observable Symptoms & Logs
```text
Training a linear model y = w*x + b to fit y = 2x + 1
MSE loss per epoch: [57.0, 144.335, 365.556, 925.913, 2345.309, 5940.672]
Final parameters: w=-32.2490, b=-8.9555
Loss moved from 57.0000 to 5940.6723 over 6 epochs
```
The loss grows roughly 2-3x every epoch instead of shrinking toward zero, and the
learned parameters drift far away from the known-correct `w=2, b=1`.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_01_Math_Fundamentals/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_gradient_descent.py
   ```
3. Observe the loss column growing every epoch instead of shrinking.

---

## Your Objective
1. Inspect `broken_gradient_descent.py` and trace exactly how `w` and `b` are updated
   each epoch.
2. Compare the update rule against the standard gradient descent rule you know from
   first principles.
3. Formulate a hypothesis for why the parameters move away from the optimum instead
   of toward it, then check `ANSWERS.md`.
