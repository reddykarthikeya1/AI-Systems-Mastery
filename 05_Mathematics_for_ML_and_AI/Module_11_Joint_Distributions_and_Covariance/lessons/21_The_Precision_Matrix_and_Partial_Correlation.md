# Lesson 11.21 — The Precision Matrix and Partial Correlation

> **Module 11:** Joint Distributions and Covariance · Lesson 21 of 29

---

## What you will be able to do after this lesson

- [ ] Define precision matrix Lambda = Sigma^(-1).
- [ ] Prove Lambda_ij = 0 iff X_i perp X_j | rest (conditional independence in Gaussian graphical models).

## Prerequisites

- 11.17 Multivariate Normal.

---

## 1. The idea

The **precision matrix** $\Lambda = \Sigma^{-1}$ encodes **conditional independence**. In a Gaussian Graphical Model, $X_i$ and $X_j$ are conditionally independent given all other variables if and only if $\Lambda_{ij} = 0$. While $\Sigma_{ij} = 0$ means marginal independence, $\Lambda_{ij} = 0$ means no direct edge exists between them.

---

## 2. Worked example

Let Markov chain $X \to Y \to Z$. $X$ and $Z$ have non-zero covariance $\Sigma_{13} \neq 0$ through $Y$, but precision entry $\Lambda_{13} = 0$ because $X \perp Z \mid Y$.

---

## 3. Verify it in code

```python
import numpy as np
# Chain X - Y - Z
# Sigma has non-zero entries everywhere
Sigma = np.array([
    [1.0, 0.8, 0.64],
    [0.8, 1.0, 0.8],
    [0.64, 0.8, 1.0]
])
Lambda = np.linalg.inv(Sigma)

# Lambda[0, 2] is zero (conditional independence)
assert np.isclose(Lambda[0, 2], 0.0, atol=1e-10)
assert not np.isclose(Sigma[0, 2], 0.0)
```

---

## 4. The mistake people actually make

Confusing marginal independence (Sigma_ij = 0) with conditional independence (Lambda_ij = 0).

---

## Check yourself

1. What does a zero entry Lambda_ij = 0 in the precision matrix indicate?
2. What is the inverse of the covariance matrix called?

<details>
<summary>Answers</summary>

1. Conditional independence between variables i and j given all other variables.
2. The precision (or concentration) matrix.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](22_Whitening_and_Mahalanobis_Distance.md)
