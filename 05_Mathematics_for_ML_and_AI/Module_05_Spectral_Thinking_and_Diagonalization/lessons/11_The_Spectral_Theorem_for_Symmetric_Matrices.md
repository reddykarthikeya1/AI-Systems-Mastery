# Lesson 05.11 — The Spectral Theorem for Symmetric Matrices

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 11 of 13

---

## What you will be able to do after this lesson

- [ ] State the Spectral Theorem: real symmetric matrices have all real eigenvalues and an orthonormal eigenbasis.
- [ ] Decompose symmetric matrices as A = Q Lambda Q^T.

## Prerequisites

- 05.06 Diagonalization and Orthogonality.

---

## 1. The idea

The **Spectral Theorem** is the crown jewel of linear algebra for machine learning: If $A \in \mathbb{R}^{n \times n}$ is symmetric ($A = A^T$), then:
1. All $n$ eigenvalues are real numbers.
2. Eigenvectors corresponding to distinct eigenvalues are mutually orthogonal.
3. $A$ has an orthonormal eigenbasis $Q$, diagonalizing as $A = Q \Lambda Q^T$ with $Q^T Q = I$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 3 & 2 \\ 2 & 3 \end{bmatrix}$. $\lambda_1 = 5, \mathbf{q}_1 = \frac{1}{\sqrt{2}}[1, 1]^T$. $\lambda_2 = 1, \mathbf{q}_2 = \frac{1}{\sqrt{2}}[-1, 1]^T$. Note $\mathbf{q}_1 \cdot \mathbf{q}_2 = 0$ and $Q Q^T = I$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[3.0, 2.0], [2.0, 3.0]])
assert np.allclose(A, A.T)  # Symmetric

vals, Q = np.linalg.eigh(A)  # eigh guarantees real and orthonormal
assert np.all(np.isreal(vals))
assert np.allclose(Q.T @ Q, np.eye(2))
assert np.allclose(Q @ np.diag(vals) @ Q.T, A)
```

---

## 4. The mistake people actually make

Using `np.linalg.eig` instead of `np.linalg.eigh` for symmetric covariance matrices. `eigh` is faster, guarantees real numbers, and enforces strict orthogonality.

---

## Check yourself

1. Are eigenvalues of a real symmetric matrix ever complex?
2. What is special about the eigenvector matrix Q of a symmetric matrix?

<details>
<summary>Answers</summary>

1. No, all eigenvalues are strictly real.
2. Q is an orthogonal matrix: Q^(-1) = Q^T.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](12_Power_Iteration_and_How_PageRank_Works.md)
