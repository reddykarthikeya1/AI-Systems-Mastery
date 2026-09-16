# Debug Lab 05 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - no normalisation inside the loop

**Where:** `power_iteration`.

```python
for _ in range(iterations):
    v = matvec(matrix, v)          # never rescaled
```

Each multiplication multiplies the vector's length by roughly the dominant
eigenvalue. After 60 steps with lambda = 3 the components are around 3^60,
about 4e28. The *direction* is right, which is why normalising afterwards
recovers the correct answer and hides the problem.

**The fix.** Normalise every step:

```python
for _ in range(iterations):
    v = matvec(matrix, v)
    length = norm(v)
    if length == 0:
        break
    v = [x / length for x in v]
```

**The general lesson.** Power iteration converges in *direction*, not in
magnitude. Rescaling each step costs nothing and is the difference between a
routine that works for 1,000 iterations and one that works for 60.

---

## Defect 2 - the same defect, now fatal

Same line. With 400 iterations, 3^400 exceeds the largest representable double
(about 1.8e308) and the components become `inf`. Every later operation gives
`inf` or `nan`, and `nan` compares unequal to everything - so a convergence
test never fires and a `max` comparison silently does the wrong thing.

Nothing raises. Python's floats saturate to infinity rather than erroring.

**The general lesson.** Overflow in floating point is silent. If a quantity in
your loop grows geometrically, it will reach infinity and every result after
that is meaningless while still being a "number". Normalise, or work in logs.

---

## Defect 3 - comparing eigenvectors component-wise

**Where:** `converged`.

An eigenvector is defined only up to a scalar multiple: `v` and `-v` are the
same eigenvector. A component-wise difference sees `[1, -1]` and `[-1, 1]` as
maximally different and reports no convergence, so the loop runs forever - or
until the iteration cap - on a problem that converged at step one.

This happens whenever the dominant eigenvalue is negative, and it is the
standard failure of a naive implementation.

**The fix.** Compare directions, not components:

```python
def converged(previous, current, tol=1e-10):
    alignment = abs(sum(a * b for a, b in zip(previous, current)))
    return abs(alignment - norm(previous) * norm(current)) < tol
```

Equivalently: compare after fixing a sign convention, such as forcing the
largest-magnitude component to be positive.

**The general lesson.** Test the thing the mathematics actually determines.
Power iteration determines a direction; anything your test demands beyond that
is a requirement you invented, and it will fail on legitimate input.
