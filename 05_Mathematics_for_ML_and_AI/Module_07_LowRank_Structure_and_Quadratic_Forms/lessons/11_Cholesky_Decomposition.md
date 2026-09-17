# Lesson 07.11 — Cholesky Decomposition

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 11 of 12

---

## What you will be able to do after this lesson

- [ ] Decompose symmetric positive definite matrix A = L L^T.
- [ ] Sample multivariate Gaussian vectors using Cholesky factor L.

## Prerequisites

- 07.10 Positive Definiteness.

---

## 1. The idea

Every symmetric positive definite matrix $A$ has a unique decomposition $A = L L^T$, where $L$ is a lower triangular matrix with strictly positive diagonal entries. Cholesky is twice as fast as LU decomposition ($O(\frac{1}{3}n^3)$ vs $O(\frac{2}{3}n^3)$) and numerically stable.

---

## 2. Worked example

Let $A = \begin{bmatrix} 4 & 2 \\ 2 & 10 \end{bmatrix}$. $L_{11} = \sqrt{4} = 2$. $L_{21} = 2 / 2 = 1$. $L_{22} = \sqrt{10 - 1^2} = 3$. So $L = \begin{bmatrix} 2 & 0 \\ 1 & 3 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[4.0, 2.0], [2.0, 10.0]])
L = np.linalg.cholesky(A)

assert np.allclose(L, [[2.0, 0.0], [1.0, 3.0]])
assert np.allclose(L @ L.T, A)

# Sampling multivariate normal: y = mu + L @ z
z = np.array([1.0, -1.0])
sample = L @ z
assert len(sample) == 2
```

---

## 4. The mistake people actually make

Calling Cholesky on a covariance matrix with numerical zero/negative eigenvalues due to floating point roundoff. Adding jitter (eps * I) fixes it.

---

## Check yourself

1. Why is Cholesky faster than LU decomposition?
2. How is Cholesky used to sample from a Gaussian distribution with covariance Sigma?

<details>
<summary>Answers</summary>

1. Because symmetry halves the required arithmetic operations to n^3 / 3.
2. Sample standard normal z ~ N(0, I) and compute x = mu + L z where Sigma = L L^T.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](12_Module_Project_Image_Compression_and_a_Recommender_Both_by_SVD.md)
