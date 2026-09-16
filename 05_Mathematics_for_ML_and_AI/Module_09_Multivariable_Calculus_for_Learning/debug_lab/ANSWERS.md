# Debug Lab 09 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - none

This is correct behaviour and it is here to set up the trap. Truncation error
falls as h falls: O(h) for the forward difference, O(h^2) for the central one.
Extrapolating that trend is precisely what leads to defect 2.

---

## Defect 2 - subtractive cancellation

**Where:** both difference functions, inherent to the method rather than to a
particular line.

Two error sources pull in opposite directions:

- **truncation error**, from the finite step: shrinks as h shrinks
- **round-off error**, from subtracting two nearly equal floats: *grows* as h
  shrinks, because the difference keeps fewer significant digits and is then
  divided by a tiny number

The total is minimised at a step size somewhere in the middle - roughly
`sqrt(machine epsilon)` for the forward difference, about 1e-8, and
`cbrt(machine epsilon)` for the central difference, about 1e-5. Below that the
answer degrades, and at 1e-17 `x + h == x` exactly, so the numerator is zero.

**The fix.** Choose h deliberately and scale it to x:

```python
h = (2.2e-16) ** (1 / 3) * max(abs(x), 1.0)      # central difference
```

Better, avoid the subtraction entirely: use automatic differentiation (what
PyTorch and JAX do) or a complex-step derivative, which has no cancellation at
all.

**The general lesson.** "More precision by taking a smaller step" is true in
analysis and false in floating point. Any limit taken numerically has a step
size at which it stops improving, and the only way to know you are near it is
to plot the error against h and look for the U.

---

## Defect 3 - divergence reported as a normal return

**Where:** `gradient_descent`, which has no convergence or divergence check.

For f(x) = x^2 the gradient is 2x, so the update is:

    x <- x - lr * 2x = x * (1 - 2 * lr)

This shrinks x only when `|1 - 2*lr| < 1`, that is `0 < lr < 1`. At lr = 1 it
oscillates forever between x and -x; above 1 it grows geometrically. In general
the bound is `lr < 2 / L`, where L is the largest curvature.

The function returns a number either way, and the caller has no way to tell the
difference without checking.

**The fix.** Make the loop report what happened:

```python
for step in range(steps):
    x_next = x - learning_rate * gradient(x)
    if not math.isfinite(x_next):
        raise FloatingPointError(f"diverged at step {step}")
    if abs(x_next - x) < tol:
        return x_next, history, "converged"
    x = x_next
return x, history, "hit the step limit"
```

**The general lesson.** An optimiser that cannot say whether it converged is
not finished. "Ran the requested number of steps" is not a result, and the
three outcomes - converged, hit the limit, diverged - need to be
distinguishable by the caller. A loss that becomes `nan` several epochs into
training is this bug with a bigger compute bill.
