# Lesson 11.09 — The Covariance Matrix

> **Module 11:** Joint Distributions and Covariance · Lesson 9 of 29

---

## What you will be able to do after this lesson

- [ ] Construct d x d covariance matrix Sigma = E[(x - mu)(x - mu)^T].
- [ ] Compute empirical covariance Sigma = 1/(N-1) X_c^T X_c in NumPy.

## Prerequisites

- 11.06 Covariance and 03.18 Transpose.

---

## 1. The idea

For random vector $\mathbf{x} \in \mathbb{R}^d$, the **covariance matrix** $\Sigma \in \mathbb{R}^{d \times d}$ collects all variances on the diagonal and pairwise covariances on the off-diagonals:
$$\Sigma = \mathbb{E}[(\mathbf{x} - \boldsymbol{\mu})(\mathbf{x} - \boldsymbol{\mu})^T]$$
For centered data matrix $X_c \in \mathbb{R}^{N \times d}$, the sample covariance is $\Sigma = \frac{1}{N-1}X_c^T X_c$.

---

## 2. Worked example

For 2D data with variances 4 and 9 and covariance 2: $\Sigma = \begin{bmatrix} 4 & 2 \\ 2 & 9 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
X = np.random.randn(100, 3)
cov_np = np.cov(X, rowvar=False)

# Manual centered dot product
Xc = X - np.mean(X, axis=0)
cov_manual = (Xc.T @ Xc) / (len(X) - 1)
assert np.allclose(cov_np, cov_manual)
```

---

## 4. The mistake people actually make

Setting rowvar=True in `np.cov` when columns represent features, producing an N x N matrix instead of d x d.

---

## Check yourself

1. What entries sit on the main diagonal of a covariance matrix?
2. What is the shape of the covariance matrix for a 10-dimensional random vector?

<details>
<summary>Answers</summary>

1. The variances of the individual variables: Var(X_i).
2. 10 x 10.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](10_Properties_of_the_Covariance_Matrix.md)
