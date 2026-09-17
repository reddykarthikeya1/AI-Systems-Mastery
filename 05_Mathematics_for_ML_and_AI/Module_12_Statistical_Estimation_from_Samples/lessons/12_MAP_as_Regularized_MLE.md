# Lesson 12.12 — MAP as Regularized MLE

> **Module 12:** Statistical Estimation from Samples · Lesson 12 of 22

---

## What you will be able to do after this lesson

- [ ] Prove Gaussian prior on weights corresponds to L2 Ridge regularization.
- [ ] Prove Laplace prior on weights corresponds to L1 Lasso regularization.

## Prerequisites

- 12.11 MAP Estimation.

---

## 1. The idea

A profound equivalence connects Bayesian priors and machine learning regularization:
- **Gaussian Prior** $p(\mathbf{w}) \propto \exp(-\frac{\|\mathbf{w}\|_2^2}{2\sigma_0^2}) \implies$ objective adds $-\lambda \|\mathbf{w}\|_2^2$ (**L2 Ridge**).
- **Laplace Prior** $p(\mathbf{w}) \propto \exp(-\frac{\|\mathbf{w}\|_1}{b}) \implies$ objective adds $-\lambda \|\mathbf{w}\|_1$ (**L1 Lasso**).

---

## 2. Worked example

In linear regression with noise variance $\sigma^2 = 1$ and prior variance $\sigma_0^2 = 1/\lambda$: $\log p(y \mid X, w) + \log p(w) = -\frac{1}{2}\|y - Xw\|^2 - \frac{\lambda}{2}\|w\|^2$. Maximizing this is identical to Ridge regression.

---

## 3. Verify it in code

```python
import numpy as np
# Ridge regression normal equation: w = (X^T X + lambda I)^(-1) X^T y
X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
y = np.array([1.0, 2.0, 3.0])
lam = 0.5

# OLS vs Ridge
w_ols = np.linalg.lstsq(X, y, rcond=None)[0]
w_ridge = np.linalg.inv(X.T @ X + lam * np.eye(2)) @ X.T @ y

assert np.linalg.norm(w_ridge) < np.linalg.norm(w_ols)
```

---

## 4. The mistake people actually make

Viewing L1 and L2 penalties as arbitrary heuristic tricks rather than explicit probabilistic priors on parameter distributions.

---

## Check yourself

1. Which prior distribution produces L2 weight decay?
2. Which prior distribution produces L1 sparse regularization?

<details>
<summary>Answers</summary>

1. A zero-mean Gaussian prior.
2. A zero-mean Laplace prior.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](13_Conjugate_Priors.md)
