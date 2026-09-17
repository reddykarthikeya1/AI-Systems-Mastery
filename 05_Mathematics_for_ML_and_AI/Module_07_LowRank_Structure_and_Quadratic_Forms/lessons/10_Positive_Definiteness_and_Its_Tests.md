# Lesson 07.10 — Positive Definiteness and Its Tests

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 10 of 12

---

## What you will be able to do after this lesson

- [ ] Test positive definiteness via eigenvalues (all > 0) and Sylvester's criterion (leading principal minors > 0).
- [ ] Recognize positive definite Hessians as local minima.

## Prerequisites

- 07.09 Quadratic Forms and 05.11 Spectral Theorem.

---

## 1. The idea

A symmetric matrix $A$ is **positive definite** ($A \succ 0$) if $\mathbf{x}^T A \mathbf{x} > 0$ for all $\mathbf{x} \neq \mathbf{0}$. Equivalent conditions:
1. All eigenvalues are strictly positive ($\lambda_i > 0$).
2. All leading principal minors are strictly positive (Sylvester's criterion).
3. In optimization, if the Hessian $\nabla^2 f(\mathbf{x}^*) \succ 0$, $\mathbf{x}^*$ is a strict local minimum.

---

## 2. Worked example

Let $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$. Minors: $M_1 = 2 > 0$, $M_2 = \det(A) = 4 - 1 = 3 > 0$. Eigenvalues: $\lambda = 3, 1 > 0$. Therefore $A$ is positive definite.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])
eigs = np.linalg.eigvalsh(A)
assert np.all(eigs > 0)

# Positive definite quadratic form
x = np.array([1.5, -2.0])
assert (x @ A @ x) > 0
```

---

## 4. The mistake people actually make

Assuming all positive matrix entries implies positive definiteness. A matrix can have all positive entries and still have negative eigenvalues.

---

## Check yourself

1. Can a matrix with all positive entries be indefinite?
2. What does a positive definite Hessian matrix guarantee at a critical point?

<details>
<summary>Answers</summary>

1. Yes (e.g. [[1, 2], [2, 1]] has det = -3 and eigenvalue -1).
2. It guarantees the critical point is a strict local minimum.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](11_Cholesky_Decomposition.md)
