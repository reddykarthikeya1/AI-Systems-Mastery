# Debug Lab Solution & Forensic Post-Mortem

## Incident: Linear Regression Loss Explodes Instead of Converging

---

### Forensic Root Cause Analysis
`train()` updates the parameters with `w = w + lr * dw` and `b = b + lr * db`. Gradient
descent must move *against* the gradient to reduce the loss, i.e. `w = w - lr * dw`.
Adding the gradient instead of subtracting it turns every step into gradient *ascent*:
each update pushes `w` and `b` further from the values that minimize the mean-squared
error, so the loss grows every epoch instead of shrinking.

---

### Production Corrective Action & Code Fix

```python
def train(x_vals, y_vals, epochs=6, lr=0.05):
    w, b = 0.0, 0.0
    history = []
    for _ in range(epochs):
        history.append(mse_loss(x_vals, y_vals, w, b))
        dw, db = compute_gradient(x_vals, y_vals, w, b)
        w = w - lr * dw   # move against the gradient
        b = b - lr * db
    return history, w, b
```

With the sign corrected, the loss decreases monotonically each epoch and `w, b`
converge toward `2.0, 1.0`.

---

### Production Prevention Invariants
1. **Loss Monitoring:** Any training loop should assert the loss is non-increasing
   (within noise tolerance) over a short warm-up window, or flag divergence early.
2. **Unit Test the Update Rule:** Test the parameter-update function in isolation
   against a known convex problem with a closed-form optimum.
3. **Code Review Checklist:** Treat every `+=`/`-=` in an optimizer update as a
   reviewable, sign-sensitive line, not a throwaway detail.
