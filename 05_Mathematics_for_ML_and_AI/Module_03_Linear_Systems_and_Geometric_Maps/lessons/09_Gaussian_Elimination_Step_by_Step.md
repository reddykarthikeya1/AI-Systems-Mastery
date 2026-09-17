# Lesson 03.09 — Gaussian Elimination Step by Step

> **Module 03:** Linear Systems and Geometric Maps · Lesson 9 of 35

---

## What you will be able to do after this lesson

- [ ] Execute forward elimination to convert augmented matrix to upper triangular form.
- [ ] Solve triangular systems via back substitution in O(n^2) operations.

## Prerequisites

- 03.07 Row Echelon Form.

---

## 1. The idea

**Gaussian Elimination** proceeds in two phases:
1. **Forward Elimination**: eliminates sub-diagonal entries column by column using row operations, producing an upper-triangular REF ($O(\frac{2}{3}n^3)$ operations).
2. **Back Substitution**: solves for variables from bottom to top ($O(n^2)$ operations).

---

## 2. Worked example

System: $x + y = 3$ and $2x + 4y = 8$. Forward: $R_2 \leftarrow R_2 - 2R_1 \implies [0, 2 \mid 2]$. Back substitution: $2y = 2 \implies y = 1$; $x + 1 = 3 \implies x = 2$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 1.0], [2.0, 4.0]])
b = np.array([3.0, 8.0])
x = np.linalg.solve(A, b)
assert np.allclose(x, [2.0, 1.0])
assert np.allclose(A @ x, b)
```

---

## 4. The mistake people actually make

Dividing by zero when the pivot element is zero. Swapping with a non-zero row below (pivoting) is required.

---

## Check yourself

1. What is the total FLOP complexity of Gaussian elimination for an n x n system?
2. What handles a zero on the diagonal during elimination?

<details>
<summary>Answers</summary>

1. O(2/3 n^3) floating point operations.
2. Row swapping (pivoting).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](10_GaussJordan_Elimination.md)
