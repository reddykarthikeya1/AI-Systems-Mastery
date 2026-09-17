# Lesson 03.25 — LU Decomposition

> **Module 03:** Linear Systems and Geometric Maps · Lesson 25 of 35

---

## What you will be able to do after this lesson

- [ ] Decompose matrix A = L U into unit lower triangular L and upper triangular U.
- [ ] Solve Ax = b via forward-substitution Ly = b then back-substitution Ux = y.

## Prerequisites

- 03.09 Gaussian Elimination.

---

## 1. The idea

**LU Decomposition** records Gaussian elimination: $A = L U$, where $U$ is the upper-triangular matrix from forward elimination and $L$ is a unit lower-triangular matrix storing the row elimination multipliers. Once factored, solving $A\mathbf{x} = \mathbf{b}$ for any new $\mathbf{b}$ costs only $O(n^2)$ via forward and back substitutions.

---

## 2. Worked example

Let $A = \begin{bmatrix} 2 & 1 \\ 6 & 7 \end{bmatrix}$. Multiplier to zero out $A_{21}$ is $m = 6/2 = 3$. $R_2 \leftarrow R_2 - 3R_1$ gives $U = \begin{bmatrix} 2 & 1 \\ 0 & 4 \end{bmatrix}$. $L = \begin{bmatrix} 1 & 0 \\ 3 & 1 \end{bmatrix}$. Product $LU = A$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[2.0, 1.0], [6.0, 7.0]])
L = np.array([[1.0, 0.0], [3.0, 1.0]])
U = np.array([[2.0, 1.0], [0.0, 4.0]])
assert np.allclose(L @ U, A)

b = np.array([5.0, 23.0])
# 1. Forward substitution: L y = b
y = np.linalg.solve(L, b)
# 2. Back substitution: U x = y
x = np.linalg.solve(U, y)
assert np.allclose(A @ x, b)
assert np.allclose(x, [1.5, 2.0])
```

---

## 4. The mistake people actually make

Recomputing full Gaussian elimination for multiple right-hand side targets b instead of reusing the precomputed LU factors.

---

## Check yourself

1. What is the structure of matrix L in LU decomposition?
2. What is the cost of solving Ax = b once LU is computed?

<details>
<summary>Answers</summary>

1. Unit lower triangular (1s on diagonal, 0s above).
2. O(n^2) operations (two triangular substitutions).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](26_Partial_Pivoting_and_Numerical_Stability.md)
