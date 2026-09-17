# Lesson 07.03 — Singular Values versus Eigenvalues

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 3 of 12

---

## What you will be able to do after this lesson

- [ ] Compare singular values and eigenvalues across symmetric and non-symmetric matrices.
- [ ] Identify cases where eigenvalues are zero but singular values are non-zero.

## Prerequisites

- 05.02 Eigenvalues and 07.01 SVD.

---

## 1. The idea

Eigenvalues satisfy $A\mathbf{v} = \lambda \mathbf{v}$ (same basis on input and output). Singular values satisfy $A\mathbf{v} = \sigma \mathbf{u}$ (different input and output bases). For symmetric positive semi-definite matrices, eigenvalues and singular values coincide.

---

## 2. Worked example

Let $A = \begin{bmatrix} 0 & 5 \\ 0 & 0 \end{bmatrix}$. Eigenvalues are both 0. But $A^T A = \begin{bmatrix} 0 & 0 \\ 0 & 25 \end{bmatrix}$, so singular values are 5 and 0. Singular values capture true operator norm even when eigenvalues vanish.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[0.0, 5.0], [0.0, 0.0]])
eigs = np.linalg.eigvals(A)
s = np.linalg.svd(A, compute_uv=False)

assert np.allclose(eigs, [0.0, 0.0])
assert np.allclose(s, [5.0, 0.0])
```

---

## 4. The mistake people actually make

Assuming small eigenvalues imply a matrix cannot significantly amplify any vector. Nilpotent matrices have zero eigenvalues but large singular values.

---

## Check yourself

1. When are singular values equal to absolute values of eigenvalues?
2. Can singular values be computed for non-square matrices?

<details>
<summary>Answers</summary>

1. When the matrix is normal (e.g. real symmetric).
2. Yes, singular values are defined for any m x n matrix.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](04_Truncated_SVD_and_the_EckartYoung_Theorem.md)
