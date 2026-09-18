# Debug Lab Solution & Forensic Post-Mortem

## Incident: Fine-Tuning Learning Rate Spikes to Maximum on the First Step

---

### 🔍 Forensic Root Cause Analysis
`warmup_lr()` computes `fraction = warmup_steps / step`. At `step=0` this raises `ZeroDivisionError`, which is silently caught and papered over by falling back to `scale = 1.0` -- i.e. full `base_lr` on the very first optimizer step, the opposite of what a warmup schedule is for. The deeper issue is the formula itself: it should scale up as `step` increases (`step / warmup_steps`), not compute the *reciprocal* (`warmup_steps / step`) and then invert it again. Because of that inversion, `step=1` produces `scale = 1/10 = 0.1` -- lower than the erroneous step-0 fallback -- and the schedule only climbs back to `base_lr` a second time as `step` approaches `warmup_steps`. The `try/except` doesn't fix the formula; it just hides the crash that would otherwise have made the bug obvious immediately.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def warmup_lr(step, base_lr, warmup_steps):
    scale = min(1.0, (step + 1) / warmup_steps)
    return base_lr * scale
```

Scaling by `(step + 1) / warmup_steps` avoids the division by zero entirely (no `try/except` needed) and produces a smooth, monotonically increasing ramp from a small nonzero value at step 0 up to `base_lr` at step 9.

---

### 🛡️ Production Prevention Invariants
1. **No Silent Except-Pass:** Never let a bare `try/except` around a formula mask a `ZeroDivisionError` with a made-up fallback value; fix the formula so the division is never degenerate.
2. **Schedule Monotonicity Tests:** Unit test that a warmup schedule's output is non-decreasing across the warmup window.
3. **Plot the Schedule:** Always plot (or print) a learning-rate schedule end to end before launching a real training run; a spike-then-dip is obvious at a glance but easy to miss buried in logs.
