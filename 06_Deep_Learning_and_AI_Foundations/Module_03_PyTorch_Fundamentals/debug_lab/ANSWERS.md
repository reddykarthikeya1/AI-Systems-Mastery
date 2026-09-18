# Debug Lab Solution & Forensic Post-Mortem

## Incident: Single-Parameter Model Oscillates Instead of Converging

---

### Forensic Root Cause Analysis
`train()` calls `backward(params, xs, ys)` every step but never calls a
`zero_grad(params)` equivalent beforehand. `Param.grad` is only ever incremented
(`p.grad += 2 * error * x`), never reset, so gradients from every previous step keep
accumulating into the current step's gradient. The effective step size therefore
grows every iteration (it is proportional to the sum of all past steps' gradients,
not just the current one), which is exactly the "forgot `optimizer.zero_grad()`"
mistake that produces runaway, oscillating updates in real PyTorch training loops.

---

### Production Corrective Action & Code Fix

```python
def train(xs, ys, epochs=10, lr=0.01):
    params = [Param(0.5)]
    history = []
    for _ in range(epochs):
        zero_grad(params)          # reset accumulated gradients first
        backward(params, xs, ys)
        optimizer_step(params, lr)
        history.append(params[0].value)
    return history
```

With gradients reset every step, `w` converges smoothly and monotonically toward
`2.0` instead of oscillating.

---

### Production Prevention Invariants
1. **Zero-Grad Discipline:** Every training loop must reset gradients before each
   `backward()` call; lint or template the loop so this can't be omitted silently.
2. **Trajectory Assertions:** Monitor parameter trajectories for monotonic movement
   toward a validation-loss minimum; flag oscillation as an early-warning signal.
3. **Gradient Norm Logging:** Log the gradient norm every step -- an accumulation bug
   shows up immediately as a norm that grows without bound.
