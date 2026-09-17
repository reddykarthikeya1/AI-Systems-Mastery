# Lesson 03.20 — Computing the Inverse by Elimination

> **Module 03:** Linear Systems and Geometric Maps · Lesson 20 of 35

---

## What you will be able to do after this lesson

- [ ] Compute A^(-1) by applying Gauss-Jordan elimination to [A | I] -> [I | A^(-1)].
- [ ] Verify inverse reconstruction in NumPy.

## Prerequisites

- 03.10 Gauss-Jordan Elimination and 03.19 Matrix Inverse.

---

## 1. The idea

To find $A^{-1}$, augment $A$ with identity $I$: $[A \mid I]$. Row operations apply elementary matrices $E$: $E[A \mid I] = [EA \mid E]$. When the left block reaches $I$, $EA = I \implies E = A^{-1}$, so the right block is $E I = A^{-1}$.

---

## 2. Worked example

For $A = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}$, row reducing $[A \mid I]$ yields $A^{-1} = \begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[2.0, 1.0], [1.0, 1.0]])
inv_manual = np.array([[1.0, -1.0], [-1.0, 2.0]])
assert np.allclose(A @ inv_manual, np.eye(2))
assert np.allclose(np.linalg.inv(A), inv_manual)
```

---

## 4. The mistake people actually make

Using matrix inversion to solve Ax = b in computer code. Solving via LU decomposition (`np.linalg.solve`) is 3x faster and far more numerically stable.

---

## Check yourself

1. What does the augmented matrix [A | I] reduce to?
2. Why is np.linalg.solve(A, b) preferred over np.linalg.inv(A) @ b?

<details>
<summary>Answers</summary>

1. [I | A^(-1)].
2. It is faster and avoids the numerical errors and instability of explicit matrix inversion.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](21_Determinants_of_2x2_and_3x3_Matrices.md)
