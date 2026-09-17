# Lesson 06.13 — QR Decomposition

> **Module 06:** Orthogonality and Projections · Lesson 13 of 18

---

## What you will be able to do after this lesson

- [ ] Decompose matrix A = Q R into orthogonal Q and upper triangular R.
- [ ] Compute QR decomposition via np.linalg.qr.

## Prerequisites

- 06.11 Gram-Schmidt.

---

## 1. The idea

Every $m \times n$ matrix $A$ factors as $A = Q R$, where $Q \in \mathbb{R}^{m \times n}$ has orthonormal columns ($Q^T Q = I$) and $R \in \mathbb{R}^{n \times n}$ is upper triangular. $R_{ij} = \mathbf{q}_i^T \mathbf{a}_j$ records the projection coefficients.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix}$. $\mathbf{q}_1 = \frac{1}{\sqrt{2}}[1, 1]^T$. $R_{11} = \|\mathbf{a}_1\| = \sqrt{2}$. $R_{12} = \mathbf{q}_1^T \mathbf{a}_2 = 3/\sqrt{2}$. $R_{22} = \|\mathbf{a}_2 - R_{12}\mathbf{q}_1\| = 1/\sqrt{2}$. $A = QR$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 1.0], [1.0, 2.0]])
Q, R = np.linalg.qr(A)
assert np.allclose(Q.T @ Q, np.eye(2))
assert np.allclose(np.triu(R), R)  # Upper triangular
assert np.allclose(Q @ R, A)
```

---

## 4. The mistake people actually make

Assuming Q is square when A is rectangular (m > n). In reduced QR, Q is m x n.

---

## Check yourself

1. What algebraic structure does R have in QR decomposition?
2. What property does Q possess?

<details>
<summary>Answers</summary>

1. R is upper triangular.
2. Q has orthonormal columns: Q^T Q = I.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](14_Solving_Least_Squares_by_QR.md)
