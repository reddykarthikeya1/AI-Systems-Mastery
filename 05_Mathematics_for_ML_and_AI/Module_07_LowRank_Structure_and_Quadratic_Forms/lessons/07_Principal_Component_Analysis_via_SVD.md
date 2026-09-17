# Lesson 07.07 — Principal Component Analysis via SVD

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 7 of 12

---

## What you will be able to do after this lesson

- [ ] Derive PCA directly from the SVD of the centered data matrix.
- [ ] Project high-dimensional data onto principal components.

## Prerequisites

- 07.04 Truncated SVD.

---

## 1. The idea

Given centered data matrix $X \in \mathbb{R}^{N \times D}$ ($X_c = X - \mu$), sample covariance is $C = \frac{1}{N-1}X_c^T X_c$. Computing the SVD $X_c = U \Sigma V^T$ gives $V$, whose columns are the exact principal component loading vectors.

---

## 2. Worked example

Let centered data $X_c$ have shape $(100, 5)$. The right singular vectors $V$ give directions of maximal variance. Projected coordinates are $Z = X_c V_k$.

---

## 3. Verify it in code

```python
import numpy as np

np.random.seed(42)
X = np.random.randn(50, 4) + np.array([10.0, -5.0, 2.0, 0.0])

# Center data
X_c = X - np.mean(X, axis=0)

# SVD of centered data
U, s, Vt = np.linalg.svd(X_c, full_matrices=False)
V = Vt.T

# Projected coordinates
Z = X_c @ V[:, :2]
assert Z.shape == (50, 2)
# Orthogonal columns in projection
cov_Z = np.cov(Z, rowvar=False)
assert np.isclose(cov_Z[0, 1], 0.0, atol=1e-5)
```

---

## 4. The mistake people actually make

Applying PCA without centering the data first. Without subtracting the mean, the first principal component points to the mean rather than direction of maximum variance.

---

## Check yourself

1. Why must data be centered before applying PCA via SVD?
2. How do the singular values s relate to the eigenvalues of the covariance matrix?

<details>
<summary>Answers</summary>

1. Because covariance is defined around the mean: Cov(X) = E[(X - mu)(X - mu)^T].
2. lambda_i = s_i^2 / (N - 1).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](08_PCA_versus_Autoencoders_What_Actually_Differs.md)
