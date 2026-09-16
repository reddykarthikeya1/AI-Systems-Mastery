# Debug Lab 04 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - none

Exact integer-valued entries eliminate to exact zeros, so counting non-zero
rows works. That is the only case in which it works.

---

## Defect 2 - counting non-zero rows with an exact comparison

**Where:** `rank`, the test `any(v != 0 for v in row)`.

`0.1` and `0.2` are not exactly representable in binary. Eliminating a row that
is mathematically a perfect multiple leaves residue around 1e-17 rather than
zero, so the row counts as non-zero and the rank comes out one too high.

A rank that is too high is the dangerous direction: it says "these features are
independent, go ahead and invert" for a matrix that is effectively singular.

**The fix.** Compare against a tolerance scaled to the matrix:

```python
def rank(matrix, tol=None):
    a = row_echelon(matrix)
    scale = max((abs(v) for row in matrix for v in row), default=1.0)
    tol = tol if tol is not None else 1e-12 * scale
    return sum(1 for row in a if any(abs(v) > tol for v in row))
```

In practice, use the SVD: count singular values above a tolerance. It is what
`numpy.linalg.matrix_rank` does, and it is far more reliable than elimination
because it does not depend on pivot order.

**The general lesson.** Rank is not a property you can read off floating-point
data without choosing a threshold. Any routine that reports a rank without
letting you set a tolerance is hiding a decision it made for you.

---

## Defect 3 - rank-nullity applied to rows instead of columns

**Where:** `nullity`, which returns `len(matrix) - rank(matrix)`.

`len(matrix)` is the number of **rows**. The rank-nullity theorem is about the
domain of the map, so it is the number of **columns**:

    rank(A) + nullity(A) = number of columns of A

**The fix.**

```python
return len(matrix[0]) - rank(matrix)
```

**The general lesson.** For a square matrix rows and columns are the same
number, so this bug is invisible in every square test case - and every textbook
example is square. It appears the moment a real feature matrix arrives with
more columns than rows, which is exactly when the null space starts to matter.
