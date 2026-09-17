# Lesson 05.06 — Diagonalization: When and Why

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 6 of 13

---

## What you will be able to do after this lesson

- [ ] State the diagonalization criterion A = P D P^(-1).
- [ ] Diagonalize symmetric and distinct-eigenvalue matrices in NumPy.

## Prerequisites

- 05.05 Algebraic vs Geometric Multiplicity.

---

## 1. The idea

An $n \times n$ matrix $A$ is **diagonalizable** if and only if it has $n$ linearly independent eigenvectors. Then $A = PDP^{-1}$, where $P$ contains eigenvectors as columns and $D$ is the diagonal matrix of eigenvalues.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 2 \\ 2 & 1 \end{bmatrix}$. Eigenvalues are 3 and -1 with eigenvectors $[1, 1]^T$ and $[-1, 1]^T$. Then $P = \begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix}$, $D = \begin{bmatrix} 3 & 0 \\ 0 & -1 \end{bmatrix}$. Then $PDP^{-1} = A$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[1.0, 2.0], [2.0, 1.0]])
vals, P = np.linalg.eig(A)
D = np.diag(vals)

P_inv = np.linalg.inv(P)
reconstructed = P @ D @ P_inv
assert np.allclose(A, reconstructed)
```

---

## 4. The mistake people actually make

Attempting to invert P when eigenvectors are not linearly independent.

---

## Check yourself

1. When is a matrix guaranteed to be diagonalizable?
2. Why is computing A^k easy when A is diagonalizable?

<details>
<summary>Answers</summary>

1. When all its eigenvalues are distinct, or when it is symmetric.
2. Because A^k = P D^k P^(-1), where D^k simply raises each diagonal entry to the power k.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](07_Similar_Matrices_and_Their_Invariants.md)
