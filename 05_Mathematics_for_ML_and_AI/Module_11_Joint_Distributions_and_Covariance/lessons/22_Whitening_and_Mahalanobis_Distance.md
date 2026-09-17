# Lesson 11.22 — Whitening and Mahalanobis Distance

> **Module 11:** Joint Distributions and Covariance · Lesson 22 of 29

---

## What you will be able to do after this lesson

- [ ] Compute Mahalanobis distance d_M(x, mu) = sqrt((x - mu)^T Sigma^(-1) (x - mu)).
- [ ] Demonstrate outlier detection using Mahalanobis metric.

## Prerequisites

- 11.09 Covariance Matrix and 06.17 Whitening.

---

## 1. The idea

Euclidean distance treats all directions equally. The **Mahalanobis distance** $d_M(\mathbf{x}, \boldsymbol{\mu}) = \sqrt{(\mathbf{x} - \boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x} - \boldsymbol{\mu})}$ scales distance along the principal variance axes of the data, correctly penalizing deviations in low-variance directions.

---

## 2. Worked example

Let $\Sigma = \begin{bmatrix} 100 & 0 \\ 0 & 1 \end{bmatrix}$. A point at $(10, 0)$ has Euclidean dist 10, but Mahalanobis dist $\sqrt{10^2/100} = 1.0$ (normal point). Point at $(0, 3)$ has Euclidean dist 3, but Mahalanobis dist $\sqrt{3^2/1} = 3.0$ (severe outlier!).

---

## 3. Verify it in code

```python
import numpy as np
Sigma = np.array([[100.0, 0.0], [0.0, 1.0]])
inv_Sigma = np.linalg.inv(Sigma)

p1 = np.array([10.0, 0.0])
p2 = np.array([0.0, 3.0])

d_m1 = np.sqrt(p1 @ inv_Sigma @ p1)
d_m2 = np.sqrt(p2 @ inv_Sigma @ p2)

assert np.isclose(d_m1, 1.0)
assert np.isclose(d_m2, 3.0)
assert d_m2 > d_m1  # p2 is much more of an outlier despite smaller Euclidean distance!
```

---

## 4. The mistake people actually make

Using Euclidean distance for k-nearest neighbors on unnormalized correlated features.

---

## Check yourself

1. Why is Mahalanobis distance preferred over Euclidean distance for multivariate outlier detection?
2. What does Mahalanobis distance reduce to when Sigma = I?

<details>
<summary>Answers</summary>

1. It accounts for feature correlations and unequal variance scales.
2. Standard Euclidean distance.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](23_Copulas_Separating_Marginals_From_Dependence.md)
