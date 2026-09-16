# Debug Lab 03 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - there is none here

The 3x3 system is solved correctly, with a residual at machine precision.

Included deliberately: a lab where everything is broken trains you to find
faults that are not there. Establishing that the basic path works is the first
step of any real investigation.

One caution on the residual, though. A small residual means "this `x` nearly
satisfies these equations". It does **not** mean "this `x` is near the true
solution" - for an ill-conditioned matrix both can be true of a badly wrong
answer. Residual measures backward error, not forward error.

---

## Defect 2 - no partial pivoting

**Where:** `solve`, the pivot selection.

```python
for row in range(col, n):
    if a[row][col] != 0:        # takes the FIRST non-zero, not the largest
        pivot_row = row
        break
```

With `a[0][0] = 1e-18`, the multiplier for the second row is `1 / 1e-18 = 1e18`.
Every entry of row 1 is then scaled by 10^18 and subtracted, so the original
values of row 1 are swamped: the information they carried is lost to rounding
before back substitution ever runs.

Mathematically the elimination is exact. In floating point it is catastrophic,
and nothing signals it - the routine returns confidently.

**The fix.** Choose the pivot with the largest magnitude in the column:

```python
pivot_row = max(range(col, n), key=lambda r: abs(a[r][col]))
```

That is **partial pivoting**, and it costs one pass over a column. It is why
every production solver does it and why no textbook presentation of Gaussian
elimination is complete without it.

**The general lesson.** Exact arithmetic and floating-point arithmetic are
different algorithms with the same notation. An operation that is harmless on
paper - dividing by a very small number - can destroy every significant digit
you had. Ordering the operations to avoid that is most of what numerical linear
algebra is about.

---

## Defect 3 - testing a float for exact zero

**Where:** `is_singular`, the line `return any(a[i][i] == 0 ...)`.

After elimination, a singular matrix leaves a diagonal entry that is *nearly*
zero, not exactly zero - rounding sees to that. So `== 0` misses it. Worse,
a matrix that is singular for every practical purpose (rows differing by one
part in 10^10) passes the check, and solving it divides by that near-zero
entry and produces nonsense.

**The fix.** Compare against a tolerance scaled to the size of the numbers
involved:

```python
scale = max(abs(v) for row in matrix for v in row) or 1.0
return any(abs(a[i][i]) < 1e-12 * scale for i in range(n))
```

The scaling matters: an absolute tolerance of `1e-12` is meaningless for a
matrix whose entries are around `1e15`.

Note what the output actually shows. The near-singular solve returned the
*exactly correct* `[3, 0]` - so "did the solve succeed" would have told you
nothing. A 1e-9 nudge to `b` then swung the answer to a completely different
point. The matrix is invertible and its inverse is enormous, which is the real
hazard and the reason the question to ask is about conditioning.

Better still, use the **condition number**. `numpy.linalg.cond` tells you how
much the answer can move when the input moves, which is the question you
actually have; singular is just the limiting case of badly conditioned.

**The general lesson.** `== 0` on a float asks whether a computation landed on
one exact bit pattern out of 2^64. That is almost never the question. Ask "is
this small relative to the scale of the problem", and say what the scale is.
