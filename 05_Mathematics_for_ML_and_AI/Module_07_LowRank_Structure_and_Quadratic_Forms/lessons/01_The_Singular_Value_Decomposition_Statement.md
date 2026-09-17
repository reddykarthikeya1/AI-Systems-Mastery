# Lesson 07.01 — The Singular Value Decomposition: Statement

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 1 of 12

---

## What you will be able to do after this lesson

- [ ] State the SVD theorem A = U Sigma V^T for arbitrary m x n matrices.
- [ ] Verify SVD factor dimensions and reconstruction with np.linalg.svd.

## Prerequisites

- 05.11 Spectral Theorem and Orthogonal matrices.

---

## 1. The idea

Every real matrix $A \in \mathbb{R}^{m \times n}$ factors as $A = U \Sigma V^T$, where $U \in \mathbb{R}^{m \times m}$ and $V \in \mathbb{R}^{n \times n}$ are orthogonal matrices, and $\Sigma \in \mathbb{R}^{m \times n}$ is a diagonal matrix containing non-negative singular values $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 3 & 0 \\ 0 & -2 \end{bmatrix}$. $A^T A = \begin{bmatrix} 9 & 0 \\ 0 & 4 \end{bmatrix}$. Singular values are $\sigma_1 = 3, \sigma_2 = 2$. $U = I$, $V = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$, $\Sigma = \text{diag}(3, 2)$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[3.0, 0.0], [0.0, -2.0]])
U, s, Vt = np.linalg.svd(A)

assert np.allclose(s, [3.0, 2.0])
assert np.allclose(U @ np.diag(s) @ Vt, A)
assert np.allclose(U.T @ U, np.eye(2))
assert np.allclose(Vt @ Vt.T, np.eye(2))
```

---

## 4. The mistake people actually make

Confusing V with V^T. NumPy's `np.linalg.svd` returns Vt (V transposed), not V.

---

## Check yourself

1. Can a non-square matrix have an SVD?
2. Can singular values be negative?

<details>
<summary>Answers</summary>

1. Yes, SVD exists unconditionally for any rectangular matrix.
2. No, singular values are non-negative square roots of eigenvalues of A^T A.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Geometry_of_the_SVD.md)
