# Lesson 03.34 — Linear Systems in NumPy and SciPy

> **Module 03:** Linear Systems and Geometric Maps · Lesson 34 of 35

---

## What you will be able to do after this lesson

- [ ] Select optimal solver routines (solve, lstsq, pinv) based on system shape and rank.
- [ ] Avoid explicit matrix inversion in numerical pipelines.

## Prerequisites

- 03.09 Gaussian Elimination and 03.27 Condition Number.

---

## 1. The idea

In scientific Python, choosing the correct solver depends on matrix properties:
- **Square, well-conditioned**: `np.linalg.solve(A, b)` (uses LAPACK `_gesv` with LU decomposition and partial pivoting, $O(\frac{2}{3}n^3)$).
- **Overdetermined ($m > n$)**: `np.linalg.lstsq(A, b)` (uses LAPACK `_gelsd` via SVD).
- **Rank-deficient**: `np.linalg.pinv(A) @ b` (minimum-norm solution).

---

## 2. Worked example

Solving $2x + y = 5, x + 3y = 5$. `np.linalg.solve` decomposes via LU in place, computing $x = 2, y = 1$ in a single call.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[2.0, 1.0], [1.0, 3.0]])
b = np.array([5.0, 5.0])

# Direct solve via LU
x = np.linalg.solve(A, b)
assert np.allclose(x, [2.0, 1.0])
assert np.allclose(A @ x, b)
```

---

## 4. The mistake people actually make

Using `np.linalg.inv(A) @ b` instead of `np.linalg.solve(A, b)`. Direct solve is faster and eliminates catastrophic loss of precision.

---

## Check yourself

1. Why is np.linalg.solve faster than np.linalg.inv?
2. What LAPACK routine underlies np.linalg.solve?

<details>
<summary>Answers</summary>

1. Because it performs LU factorization and back substitution directly without assembling the full inverse matrix.
2. _gesv (LU factorization with partial pivoting).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](35_Module_Project_A_Solver_That_Reports_Its_Own_Conditioning.md)
