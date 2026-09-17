# Lesson 03.22 — Determinant Properties and Row Operations

> **Module 03:** Linear Systems and Geometric Maps · Lesson 22 of 35

---

## What you will be able to do after this lesson

- [ ] State determinant rules under row operations: swapping flips sign, scaling scales det, row addition preserves det.
- [ ] Verify det(AB) = det(A) det(B).

## Prerequisites

- 03.21 Determinants.

---

## 1. The idea

Determinant algebraic properties:
1. Swapping two rows multiplies $\det(A)$ by $-1$.
2. Multiplying a row by $c$ scales $\det(A)$ by $c$.
3. Adding a multiple of one row to another leaves $\det(A)$ unchanged!
4. $\det(AB) = \det(A)\det(B)$ and $\det(A^{-1}) = 1/\det(A)$.

---

## 2. Worked example

Let $\det(A) = 5, \det(B) = 3$. Then $\det(AB) = 15$ and $\det(2A)$ for $2 \times 2$ is $2^2 \det(A) = 20$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[2.0, 1.0], [1.0, 3.0]])
B = np.array([[1.0, 4.0], [2.0, 5.0]])
assert np.isclose(np.linalg.det(A @ B), np.linalg.det(A) * np.linalg.det(B))
assert np.isclose(np.linalg.det(np.linalg.inv(A)), 1.0 / np.linalg.det(A))
# Scaling n x n matrix by c scales det by c^n
assert np.isclose(np.linalg.det(2.0 * A), (2.0**2) * np.linalg.det(A))
```

---

## 4. The mistake people actually make

Claiming det(c A) = c det(A). For an n x n matrix, det(c A) = c^n det(A).

---

## Check yourself

1. What is det(c A) for an n x n matrix?
2. Does adding a multiple of row 1 to row 2 change det(A)?

<details>
<summary>Answers</summary>

1. c^n det(A).
2. No, row addition leaves the determinant completely unchanged.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](23_Determinants_Volume_and_Orientation.md)
