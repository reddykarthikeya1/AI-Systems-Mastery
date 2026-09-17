# Lesson 11.19 — Conditionals of a Multivariate Normal

> **Module 11:** Joint Distributions and Covariance · Lesson 19 of 29

---

## What you will be able to do after this lesson

- [ ] Compute conditional distribution x_1 | x_2 ~ N(mu_1|2, Sigma_1|2) using Schur complements.
- [ ] Implement Gaussian Process regression conditional updates.

## Prerequisites

- 11.17 Multivariate Normal.

---

## 1. The idea

Conditionals of a joint Gaussian remain strictly Gaussian!
For partitioned vector $[\mathbf{x}_1, \mathbf{x}_2]^T$, $\mathbf{x}_1 \mid \mathbf{x}_2 \sim \mathcal{N}(\boldsymbol{\mu}_{1|2}, \Sigma_{1|2})$ where:
$$\boldsymbol{\mu}_{1|2} = \boldsymbol{\mu}_1 + \Sigma_{12} \Sigma_{22}^{-1}(\mathbf{x}_2 - \boldsymbol{\mu}_2)$$
$$\Sigma_{1|2} = \Sigma_{11} - \Sigma_{12} \Sigma_{22}^{-1} \Sigma_{21}$$
Notice the conditional covariance is strictly smaller than $\Sigma_{11}$ (observing $\mathbf{x}_2$ reduces uncertainty).

---

## 2. Worked example

Let $\boldsymbol{\mu} = \mathbf{0}, \Sigma = \begin{bmatrix} 1 & 0.8 \\ 0.8 & 1 \end{bmatrix}$. Given $x_2 = 2$: $\mu_{1|2} = 0 + 0.8(1)(2) = 1.6$. $\Sigma_{1|2} = 1 - 0.8^2 = 1 - 0.64 = 0.36$.

---

## 3. Verify it in code

```python
import numpy as np
mu = np.array([0.0, 0.0])
Sigma = np.array([[1.0, 0.8], [0.8, 1.0]])

# Given x2 = 2.0
x2 = 2.0
mu_cond = mu[0] + Sigma[0, 1] * (1.0 / Sigma[1, 1]) * (x2 - mu[1])
sigma_cond = Sigma[0, 0] - Sigma[0, 1] * (1.0 / Sigma[1, 1]) * Sigma[1, 0]

assert np.isclose(mu_cond, 1.6)
assert np.isclose(sigma_cond, 0.36)
```

---

## 4. The mistake people actually make

Assuming conditional variance depends on the observed value x_2. In Gaussians, Sigma_{1|2} depends only on the covariance, not on x_2.

---

## Check yourself

1. Does the conditional covariance Sigma_{1|2} of a Gaussian depend on the observed value x_2?
2. What machine learning model relies on conditional Gaussian formulas?

<details>
<summary>Answers</summary>

1. No, it depends only on the prior covariance structure.
2. Gaussian Processes (GPs).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](20_Marginals_of_a_Multivariate_Normal.md)
