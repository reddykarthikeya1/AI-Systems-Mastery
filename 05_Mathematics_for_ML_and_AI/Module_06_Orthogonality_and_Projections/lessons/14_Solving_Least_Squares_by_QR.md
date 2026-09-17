# Lesson 06.14 — Solving Least Squares by QR

> **Module 06:** Orthogonality and Projections · Lesson 14 of 18

---

## What you will be able to do after this lesson

- [ ] Solve least squares via R x_hat = Q^T b using back-substitution.
- [ ] Explain why QR avoids squaring the condition number kappa(A^T A) = kappa(A)^2.

## Prerequisites

- 06.13 QR Decomposition and 06.09 Least Squares.

---

## 1. The idea

Normal equations $A^T A \hat{\mathbf{x}} = A^T \mathbf{b}$ square the condition number: $\kappa(A^T A) = \kappa(A)^2$, destroying numerical accuracy for ill-conditioned data. Substituting $A = QR$: $(R^T Q^T Q R)\hat{\mathbf{x}} = R^T Q^T \mathbf{b} \implies R\hat{\mathbf{x}} = Q^T \mathbf{b}$. Solved via fast, stable back-substitution with condition number $\kappa(A)$.

---

## 2. Worked example

Let $Q^T \mathbf{b} = [3, 1]^T$ and $R = \begin{bmatrix} 2 & 1 \\ 0 & 1 \end{bmatrix}$.
Back substitution:
$x_2 = 1 / 1 = 1$.
$2 x_1 + 1(1) = 3 \implies x_1 = 1$. $\hat{\mathbf{x}} = [1, 1]^T$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 0.0], [1.0, 1.0], [1.0, 2.0]])
b = np.array([1.0, 2.0, 2.0])

Q, R = np.linalg.qr(A)
# Solve R x = Q.T @ b
qty = Q.T @ b
x_qr = np.linalg.solve(R, qty)

x_lstsq = np.linalg.lstsq(A, b, rcond=None)[0]
assert np.allclose(x_qr, x_lstsq)
```

---

## 4. The mistake people actually make

Explicitly computing A^T A when solving regression on ill-conditioned data, which doubles condition number.

---

## Check yourself

1. Why is solving least squares via QR numerically superior to normal equations?
2. What algorithm solves R x = Q^T b since R is triangular?

<details>
<summary>Answers</summary>

1. Because it operates with condition number kappa(A) rather than squared condition number kappa(A)^2.
2. Back-substitution (O(n^2) operations).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](15_Orthogonal_Matrices_and_Isometries.md)
