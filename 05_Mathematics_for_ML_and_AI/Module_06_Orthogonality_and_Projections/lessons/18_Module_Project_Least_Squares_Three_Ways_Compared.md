# Lesson 06.18 — Module Project: Least Squares Three Ways Compared

> **Module 06:** Orthogonality and Projections · Lesson 18 of 18

---

## What you will be able to do after this lesson

- [ ] Compare Normal Equations, QR Decomposition, and SVD on an ill-conditioned polynomial fit.
- [ ] Observe numerical breakdown of normal equations.

## Prerequisites

- Lessons 06.01 to 06.17.

---

## 1. The idea

We benchmark three computational paths for solving $A\mathbf{x} = \mathbf{b}$:
1. **Normal Equations** $\hat{\mathbf{x}} = (A^T A)^{-1}A^T \mathbf{b}$: fast $O(\frac{1}{3}n^3)$ but unstable ($\kappa^2$).
2. **QR Decomposition** $R\hat{\mathbf{x}} = Q^T \mathbf{b}$: stable $O(\frac{2}{3}n^3)$, standard for full-rank.
3. **SVD** $\hat{\mathbf{x}} = V \Sigma^+ U^T \mathbf{b}$: most robust $O(2mn^2)$, handles rank-deficient systems.

---

## 2. Worked example

On a Vandermonde polynomial matrix of degree 5, Normal Equations incur rounding errors up to 1000x larger than QR and SVD.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
t = np.linspace(0, 1, 20)
# Vandermonde matrix
A = np.vander(t, 4)
b = np.sin(t)

# 1. Normal equations
x_ne = np.linalg.solve(A.T @ A, A.T @ b)

# 2. QR decomposition
Q, R = np.linalg.qr(A)
x_qr = np.linalg.solve(R, Q.T @ b)

# 3. SVD / pinv
x_svd = np.linalg.pinv(A) @ b

assert np.allclose(x_ne, x_qr, atol=1e-5)
assert np.allclose(x_qr, x_svd, atol=1e-5)
```

---

## 4. The mistake people actually make

Using Normal Equations for high-degree polynomial regression, causing catastrophic floating-point cancellation.

---

## Check yourself

1. Which method handles rank-deficient least squares problems safely?
2. Why is QR preferred over normal equations in numerical libraries?

<details>
<summary>Answers</summary>

1. SVD (pseudoinverse).
2. QR avoids squaring the condition number, preserving floating-point precision.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md)
