# Lesson 11.20 — Marginals of a Multivariate Normal

> **Module 11:** Joint Distributions and Covariance · Lesson 20 of 29

---

## What you will be able to do after this lesson

- [ ] Extract marginal distributions of subset variables simply by dropping irrelevant rows and columns.
- [ ] Contrast ease of Gaussian marginalization with non-Gaussian integration.

## Prerequisites

- 11.17 Multivariate Normal.

---

## 1. The idea

Marginal distributions of an MVN are trivial: to find the marginal distribution of $\mathbf{x}_1$, simply read off $\boldsymbol{\mu}_1$ and $\Sigma_{11}$ from the joint parameters. $\mathbf{x}_1 \sim \mathcal{N}(\boldsymbol{\mu}_1, \Sigma_{11})$. No integration is required!

---

## 2. Worked example

If $[\mathbf{x}_1, \mathbf{x}_2]^T \sim \mathcal{N}([3, 5]^T, \begin{bmatrix} 4 & 1 \\ 1 & 9 \end{bmatrix})$, then marginal $x_1 \sim \mathcal{N}(3, 4)$.

---

## 3. Verify it in code

```python
import numpy as np
mu_joint = np.array([3.0, 5.0])
Sigma_joint = np.array([[4.0, 1.0], [1.0, 9.0]])

mu_x1 = mu_joint[0]
sigma2_x1 = Sigma_joint[0, 0]
assert mu_x1 == 3.0
assert sigma2_x1 == 4.0
```

---

## 4. The mistake people actually make

Attempting to compute marginals of a Gaussian by integrating over conditional distributions.

---

## Check yourself

1. How are marginals obtained from a joint Gaussian covariance matrix?
2. What distribution does any linear combination of Gaussian variables follow?

<details>
<summary>Answers</summary>

1. By simply selecting the corresponding sub-block of the covariance matrix.
2. A univariate or multivariate Gaussian distribution.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](21_The_Precision_Matrix_and_Partial_Correlation.md)
