# Lesson 03.33 — Least Squares via the Normal Equations

> **Module 03:** Linear Systems and Geometric Maps · Lesson 33 of 35

---

## What you will be able to do after this lesson

- [ ] Derive the normal equations A^T A x = A^T b by setting the gradient of ||Ax - b||^2 to zero.
- [ ] Compute least-squares parameters in NumPy.

## Prerequisites

- 03.04 Matrices as Compact Notation and 06.09 Least Squares.

---

## 1. The idea

To minimize the sum of squared errors $L(\mathbf{x}) = \|A\mathbf{x} - \mathbf{b}\|_2^2 = (A\mathbf{x} - \mathbf{b})^T(A\mathbf{x} - \mathbf{b})$, differentiate with respect to $\mathbf{x}$:
$$\nabla_{\mathbf{x}} L(\mathbf{x}) = 2 A^T(A\mathbf{x} - \mathbf{b}) = \mathbf{0} \implies A^T A \mathbf{x} = A^T \mathbf{b}$$
When $A$ has linearly independent columns, $A^T A$ is strictly invertible, yielding the closed-form ordinary least squares (OLS) solution $\hat{\mathbf{x}} = (A^T A)^{-1}A^T \mathbf{b}$.

---

## 2. Worked example

Given points $(1, 1), (2, 2), (3, 2)$. Model $y = w x$. $A = [1, 2, 3]^T, \mathbf{b} = [1, 2, 2]^T$. $A^T A = 1 + 4 + 9 = 14$. $A^T \mathbf{b} = 1(1) + 2(2) + 3(2) = 11$. $w = 11/14 \approx 0.786$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0], [2.0], [3.0]])
b = np.array([1.0, 2.0, 2.0])
w = (A.T @ b) / (A.T @ A)
assert np.isclose(w[0], 11.0 / 14.0)
w_lstsq, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
assert np.isclose(w[0], w_lstsq[0])
```

---

## 4. The mistake people actually make

Using normal equations when features are collinear, which makes A^T A non-invertible.

---

## Check yourself

1. What is the dimension of A^T A for an m x n matrix A?
2. What matrix equation defines the least squares solution?

<details>
<summary>Answers</summary>

1. n x n.
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

[Module README](../README.md) · [Next →](34_Linear_Systems_in_NumPy_and_SciPy.md)
