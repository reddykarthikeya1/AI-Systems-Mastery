# Lesson 06.17 — Whitening and Decorrelation

> **Module 06:** Orthogonality and Projections · Lesson 17 of 18

---

## What you will be able to do after this lesson

- [ ] Transform correlated features into spherical white noise with Cov(Z) = I.
- [ ] Implement PCA and ZCA (Mahalanobis) whitening in NumPy.

## Prerequisites

- 05.11 Spectral Theorem and Covariance.

---

## 1. The idea

**Whitening** transforms correlated data $\mathbf{x}$ (covariance $\Sigma = Q \Lambda Q^T$) into uncorrelated features $\mathbf{z}$ with identity covariance $\text{Cov}(\mathbf{z}) = I$.
- **PCA Whitening**: $\mathbf{z}_{PCA} = \Lambda^{-1/2} Q^T \mathbf{x}$.
- **ZCA Whitening**: $\mathbf{z}_{ZCA} = Q \Lambda^{-1/2} Q^T \mathbf{x}$ (minimizes distortion $\|x - z\|$).

---

## 2. Worked example

Let covariance $\Sigma = \begin{bmatrix} 4 & 0 \\ 0 & 9 \end{bmatrix}$. Eigenvalues are 4 and 9. Whitening simply divides coordinates by standard deviations $\sqrt{4}=2$ and $\sqrt{9}=3$.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
X = np.random.randn(500, 2) @ np.array([[2.0, 1.0], [0.5, 3.0]])
X_c = X - np.mean(X, axis=0)

# Covariance
Sigma = np.cov(X_c, rowvar=False)
vals, Q = np.linalg.eigh(Sigma)

# ZCA Whitening
W_zca = Q @ np.diag(1.0 / np.sqrt(vals)) @ Q.T
Z = X_c @ W_zca.T

cov_Z = np.cov(Z, rowvar=False)
assert np.allclose(cov_Z, np.eye(2), atol=1e-2)
```

---

## 4. The mistake people actually make

Whitening data without adding a small epsilon to eigenvalues, which divides by zero along near-collinear directions.

---

## Check yourself

1. What is the covariance matrix of a properly whitened dataset?
2. What is the key advantage of ZCA whitening over PCA whitening?

<details>
<summary>Answers</summary>

1. The identity matrix I.
2. ZCA whitening maintains maximum resemblance to the original raw features.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](18_Module_Project_Least_Squares_Three_Ways_Compared.md)
