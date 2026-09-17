# Lesson 07.04 — Truncated SVD and the Eckart-Young Theorem

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 4 of 12

---

## What you will be able to do after this lesson

- [ ] Formulate the Eckart-Young-Mirsky optimal low-rank approximation theorem.
- [ ] Construct rank-k truncated SVD approximations.

## Prerequisites

- 07.01 SVD Statement.

---

## 1. The idea

The **Eckart-Young Theorem** states that the best rank-$k$ approximation ($k < r$) to matrix $A$ in both Frobenius and Spectral norms is the truncated SVD: $A_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^T$. The approximation error is $\|A - A_k\|_2 = \sigma_{k+1}$.

---

## 2. Worked example

Let $A$ have singular values 10, 4, 1. The best rank-1 approximation error is $\sigma_2 = 4$. The best rank-2 approximation error is $\sigma_3 = 1$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[10.0, 0.0, 0.0],
              [0.0,  4.0, 0.0],
              [0.0,  0.0, 1.0]])

U, s, Vt = np.linalg.svd(A)

# Rank-1 approximation
A1 = s[0] * np.outer(U[:, 0], Vt[0])
err_spectral = np.linalg.norm(A - A1, ord=2)
assert np.isclose(err_spectral, s[1])
assert np.isclose(err_spectral, 4.0)
```

---

## 4. The mistake people actually make

Trying to obtain low-rank approximations by zeroing arbitrary elements of A instead of truncating singular components.

---

## Check yourself

1. What is the spectral norm error of the rank-k truncated SVD?
2. What does the Eckart-Young theorem guarantee?

<details>
<summary>Answers</summary>

1. sigma_{k+1}.
2. That truncated SVD is the globally optimal rank-k approximation under both Frobenius and spectral norms.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](05_LowRank_Approximation_in_Practice.md)
