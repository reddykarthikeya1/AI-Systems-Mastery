# Lesson 11.11 — Why Covariance Matrices Are Positive Semidefinite

> **Module 11:** Joint Distributions and Covariance · Lesson 11 of 29

---

## What you will be able to do after this lesson

- [ ] Prove a^T Sigma a = Var(a^T x) >= 0.
- [ ] Verify all eigenvalues of Sigma are non-negative in NumPy.

## Prerequisites

- 11.10 Properties of Covariance and 07.10 Positive Definiteness.

---

## 1. The idea

For any non-zero vector $\mathbf{a}$, the scalar $\mathbf{a}^T \mathbf{x}$ is a linear combination of random variables. Its variance is:
$$\text{Var}(\mathbf{a}^T \mathbf{x}) = \mathbf{a}^T \Sigma \mathbf{a}$$
Because variance cannot be negative by definition ($\text{Var} \ge 0$), $\mathbf{a}^T \Sigma \mathbf{a} \ge 0$ for all $\mathbf{a}$. Therefore every covariance matrix is **positive semi-definite** ($\Sigma \succeq 0$), and all its eigenvalues are $\ge 0$.

---

## 2. Worked example

Let $\Sigma = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$. Eigenvalues are 3 and 1 (both $> 0$). For $\mathbf{a} = [1, -1]^T$, $\mathbf{a}^T \Sigma \mathbf{a} = 1(2) - 2(1) + 1(2) = 2 \ge 0$.

---

## 3. Verify it in code

```python
import numpy as np
Sigma = np.array([[2.0, 1.0], [1.0, 2.0]])
eigs = np.linalg.eigvalsh(Sigma)
assert np.all(eigs >= 0.0)

a = np.array([1.0, -1.0])
var_proj = a @ Sigma @ a
assert var_proj >= 0.0
assert np.isclose(var_proj, 2.0)
```

---

## 4. The mistake people actually make

Constructing an empirical covariance with pairwise missing data imputation that accidentally yields negative eigenvalues.

---

## Check yourself

1. Can a valid covariance matrix have negative eigenvalues?
2. What does a^T Sigma a represent physically?

<details>
<summary>Answers</summary>

1. No, all eigenvalues of a covariance matrix must be >= 0.
2. The variance of the scalar projection of the random vector along direction a.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](12_Linear_Combinations_and_Their_Variance.md)
