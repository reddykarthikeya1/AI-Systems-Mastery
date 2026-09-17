# Lesson 11.17 — The Multivariate Normal Distribution

> **Module 11:** Joint Distributions and Covariance · Lesson 17 of 29

---

## What you will be able to do after this lesson

- [ ] Write PDF of MVN: (2 pi)^(-d/2) det(Sigma)^(-1/2) exp(-1/2 (x - mu)^T Sigma^(-1) (x - mu)).
- [ ] Evaluate MVN log-likelihood in NumPy.

## Prerequisites

- 11.09 Covariance Matrix and 07.10 Positive Definiteness.

---

## 1. The idea

The **Multivariate Normal (MVN)** $\mathcal{N}(\boldsymbol{\mu}, \Sigma)$ in $\mathbb{R}^d$ has density:
$$f(\mathbf{x}) = \frac{1}{(2\pi)^{d/2} \det(\Sigma)^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)$$
The quadratic form $(\mathbf{x} - \boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x} - \boldsymbol{\mu})$ is the squared **Mahalanobis distance**.

---

## 2. Worked example

For 2D standard normal ($\boldsymbol{\mu}=\mathbf{0}, \Sigma = I_2$), $f(\mathbf{0}) = \frac{1}{2\pi \sqrt{1}} \exp(0) = \frac{1}{2\pi} \approx 0.159$.

---

## 3. Verify it in code

```python
import numpy as np
mu = np.zeros(2)
Sigma = np.eye(2)
d = 2
x = np.zeros(2)

norm_const = 1.0 / (((2.0 * np.pi)**(d / 2.0)) * np.sqrt(np.linalg.det(Sigma)))
pdf_val = norm_const * np.exp(-0.5 * (x - mu) @ np.linalg.inv(Sigma) @ (x - mu))
assert np.isclose(pdf_val, 1.0 / (2.0 * np.pi))
```

---

## 4. The mistake people actually make

Inverting singular covariance matrices in the MVN density formula. Regularization (adding eps * I) is required.

---

## Check yourself

1. What is the normalization prefactor of a d-dimensional Gaussian?
2. What is the exponent term in the MVN PDF?

<details>
<summary>Answers</summary>

1. 1 / ((2 pi)^(d/2) det(Sigma)^(1/2)).
2. -0.5 (x - mu)^T Sigma^(-1) (x - mu).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](18_Geometry_of_the_Multivariate_Normal.md)
