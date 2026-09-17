# Lesson 06.07 — Projection Onto a Subspace

> **Module 06:** Orthogonality and Projections · Lesson 7 of 18

---

## What you will be able to do after this lesson

- [ ] Derive the normal equation A^T A x_hat = A^T b for subspace projection.
- [ ] Compute projection vector p = A (A^T A)^(-1) A^T b.

## Prerequisites

- 06.06 Projection Onto a Line.

---

## 1. The idea

To project $\mathbf{b}$ onto $\text{col}(A)$, the residual $\mathbf{e} = \mathbf{b} - A\hat{\mathbf{x}}$ must be perpendicular to every column of $A$: $A^T(\mathbf{b} - A\hat{\mathbf{x}}) = \mathbf{0} \implies A^T A \hat{\mathbf{x}} = A^T \mathbf{b}$. When $A$ has independent columns, $\hat{\mathbf{x}} = (A^T A)^{-1} A^T \mathbf{b}$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0 & 0 \end{bmatrix}$ (xy-plane in $\mathbb{R}^3$) and $\mathbf{b} = [2, 3, 7]^T$. $A^T A = I_2$. $\hat{\mathbf{x}} = [2, 3]^T$, $\mathbf{p} = [2, 3, 0]^T$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])
b = np.array([2.0, 3.0, 7.0])
x_hat = np.linalg.inv(A.T @ A) @ A.T @ b
p = A @ x_hat
e = b - p
assert np.allclose(p, [2.0, 3.0, 0.0])
assert np.allclose(A.T @ e, [0.0, 0.0])
```

---

## 4. The mistake people actually make

Splitting (A^T A)^(-1) as A^(-1) (A^T)^(-1) when A is rectangular (A has no two-sided inverse).

---

## Check yourself

1. Why can't we simplify A (A^T A)^(-1) A^T to I when A is m x n with m > n?
2. What subspace is residual e orthogonal to?

<details>
<summary>Answers</summary>

1. Because A is rectangular and non-invertible; P is rank n in R^m, not the full identity.
2. The column space of A: col(A).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](08_The_Projection_Matrix_and_Its_Properties.md)
