# Lesson 06.09 — Least Squares as Orthogonal Projection

> **Module 06:** Orthogonality and Projections · Lesson 9 of 18

---

## What you will be able to do after this lesson

- [ ] Formulate linear regression as least squares projection in feature space.
- [ ] Solve min ||A x - b||_2^2 via normal equations.

## Prerequisites

- 06.07 Projection Onto a Subspace.

---

## 1. The idea

When $A\mathbf{x} = \mathbf{b}$ has no exact solution ($m > n$), linear least squares finds $\hat{\mathbf{x}}$ minimizing $\|\mathbf{b} - A\mathbf{x}\|_2^2$. The fitted values $\hat{\mathbf{y}} = A\hat{\mathbf{x}}$ are the orthogonal projection of target $\mathbf{b}$ onto $\text{col}(A)$.

---

## 2. Worked example

Fit line $y = c + d t$ to points $(0, 1), (1, 2), (2, 2)$.
$A = \begin{bmatrix} 1 & 0 \\ 1 & 1 \\ 1 & 2 \end{bmatrix}, \mathbf{b} = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}$. $A^T A = \begin{bmatrix} 3 & 3 \\ 3 & 5 \end{bmatrix}, A^T \mathbf{b} = \begin{bmatrix} 5 \\ 6 \end{bmatrix}$.
Solving: $\hat{\mathbf{x}} = [7/6, 1/2]^T \approx [1.167, 0.5]^T$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 0.0], [1.0, 1.0], [1.0, 2.0]])
b = np.array([1.0, 2.0, 2.0])
x_hat = np.linalg.solve(A.T @ A, A.T @ b)
assert np.allclose(x_hat, [7.0/6.0, 0.5])
# Match NumPy lstsq
x_np, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
assert np.allclose(x_hat, x_np)
```

---

## 4. The mistake people actually make

Solving least squares by inverting A^T A when features are collinear (singular A^T A).

---

## Check yourself

1. What geometric quantity does least squares minimize?
2. What equation characterizes the least squares solution?

<details>
<summary>Answers</summary>

1. The Euclidean norm of the residual vector ||b - A x||_2.
2. The normal equations: A^T A x = A^T b.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](10_Why_Residuals_Are_Orthogonal_to_the_Fit.md)
