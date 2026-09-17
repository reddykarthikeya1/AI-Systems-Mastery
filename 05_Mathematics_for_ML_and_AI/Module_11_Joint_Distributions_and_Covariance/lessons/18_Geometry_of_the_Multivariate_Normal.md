# Lesson 11.18 — Geometry of the Multivariate Normal

> **Module 11:** Joint Distributions and Covariance · Lesson 18 of 29

---

## What you will be able to do after this lesson

- [ ] Identify contours of constant density as ellipsoids (x - mu)^T Sigma^(-1) (x - mu) = c^2.
- [ ] Connect principal axes to eigenvectors and eigenvalues of Sigma.

## Prerequisites

- 11.17 Multivariate Normal and 05.11 Spectral Theorem.

---

## 1. The idea

Equi-density surfaces of the MVN are hyper-ellipsoids centered at $\boldsymbol{\mu}$. By spectral theorem $\Sigma = Q \Lambda Q^T$, the directions of the semi-axes are given by eigenvectors $\mathbf{q}_i$, and the lengths of the semi-axes are proportional to standard deviations $\sqrt{\lambda_i}$.

---

## 2. Worked example

If $\Sigma = \begin{bmatrix} 4 & 0 \\ 0 & 1 \end{bmatrix}$, axes are aligned with coordinate axes with standard deviations $\sqrt{4}=2$ along $x$ and $\sqrt{1}=1$ along $y$.

---

## 3. Verify it in code

```python
import numpy as np
Sigma = np.array([[4.0, 0.0], [0.0, 1.0]])
vals, vecs = np.linalg.eigh(Sigma)
axis_lengths = np.sqrt(vals)
assert np.allclose(axis_lengths, [1.0, 2.0])
assert np.allclose(vecs.T @ vecs, np.eye(2))
```

---

## 4. The mistake people actually make

Believing Gaussian contours are spherical when variables are correlated. They are tilted ellipsoids.

---

## Check yourself

1. What geometric shape do equi-density contours of an MVN form?
2. What determines the orientation of the contour ellipsoids?

<details>
<summary>Answers</summary>

1. Hyper-ellipsoids.
2. The eigenvectors of the covariance matrix Sigma.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](19_Conditionals_of_a_Multivariate_Normal.md)
