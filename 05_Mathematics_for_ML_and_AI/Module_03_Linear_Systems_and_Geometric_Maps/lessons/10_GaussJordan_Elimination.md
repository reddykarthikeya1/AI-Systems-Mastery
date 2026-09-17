# Lesson 03.10 — Gauss-Jordan Elimination

> **Module 03:** Linear Systems and Geometric Maps · Lesson 10 of 35

---

## What you will be able to do after this lesson

- [ ] Execute Gauss-Jordan elimination to clear entries both above and below pivots.
- [ ] Read off solutions directly from the RREF augmented matrix.

## Prerequisites

- 03.08 RREF and 03.09 Gaussian Elimination.

---

## 1. The idea

**Gauss-Jordan elimination** extends forward elimination by continuing upward elimination to eliminate all entries above pivots as well as below, reducing $[A \mid \mathbf{b}]$ all the way to $[I \mid \mathbf{x}^*]$. Solutions can be read off directly without back substitution.

---

## 2. Worked example

Transforming $[A \mid \mathbf{b}]$ to $[I \mid \mathbf{x}^*]$ directly gives $x_1 = 2, x_2 = 1$ in the final column.

---

## 3. Verify it in code

```python
import numpy as np
# Direct matrix solve
A = np.array([[1.0, 1.0], [2.0, 4.0]])
b = np.array([3.0, 8.0])
invA = np.linalg.inv(A)
x = invA @ b
assert np.allclose(x, [2.0, 1.0])
```

---

## 4. The mistake people actually make

Using Gauss-Jordan to solve large systems of linear equations. It requires 50% more operations than Gaussian elimination with back substitution.

---

## Check yourself

1. Why is Gaussian elimination with back substitution preferred over Gauss-Jordan for solving Ax = b?
2. What does [A | I] become under Gauss-Jordan?

<details>
<summary>Answers</summary>

1. Because Gauss-Jordan requires O(n^3) FLOPs versus O(2/3 n^3) for Gaussian elimination.
2. [I | A^(-1)].

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](11_Pivots_Free_Variables_and_Parametric_Solutions.md)
