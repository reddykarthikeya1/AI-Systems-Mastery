# Lesson 11.10 — Properties of the Covariance Matrix

> **Module 11:** Joint Distributions and Covariance · Lesson 10 of 29

---

## What you will be able to do after this lesson

- [ ] Prove symmetry Sigma^T = Sigma.
- [ ] Prove scaling property Cov(A x) = A Cov(x) A^T.

## Prerequisites

- 11.09 The Covariance Matrix.

---

## 1. The idea

Key algebraic properties of covariance matrices:
1. **Symmetry**: $\Sigma^T = \Sigma$ because $\text{Cov}(X_i, X_j) = \text{Cov}(X_j, X_i)$.
2. **Affine Transformation**: If $\mathbf{y} = A\mathbf{x} + \mathbf{b}$, then $\text{Cov}(\mathbf{y}) = A \Sigma_{\mathbf{x}} A^T$.
3. **Variance Non-negativity**: $\mathbf{a}^T \Sigma \mathbf{a} = \text{Var}(\mathbf{a}^T \mathbf{x}) \ge 0$.

---

## 2. Worked example

Let $\Sigma_x = I_2$ and $A = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$. $\Sigma_y = A I A^T = \begin{bmatrix} 4 & 0 \\ 0 & 9 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
Sigma_x = np.eye(2)
A = np.array([[2.0, 0.0], [0.0, 3.0]])
Sigma_y = A @ Sigma_x @ A.T
assert np.allclose(Sigma_y, [[4.0, 0.0], [0.0, 9.0]])
assert np.allclose(Sigma_y, Sigma_y.T)
```

---

## 4. The mistake people actually make

Writing Cov(A x) = A Cov(x) instead of the quadratic form A Cov(x) A^T.

---

## Check yourself

1. What is Cov(A x) in terms of Cov(x)?
2. Why is a covariance matrix always symmetric?

<details>
<summary>Answers</summary>

1. A Cov(x) A^T.
2. Because Cov(X_i, X_j) = Cov(X_j, X_i).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](11_Why_Covariance_Matrices_Are_Positive_Semidefinite.md)
