# Lesson 07.06 — The Moore-Penrose Pseudoinverse

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 6 of 12

---

## What you will be able to do after this lesson

- [ ] Compute the pseudoinverse A^+ = V Sigma^+ U^T.
- [ ] Solve under- and over-determined linear systems with minimum norm.

## Prerequisites

- 07.01 SVD Statement.

---

## 1. The idea

When $A$ is non-square or rank-deficient, $A^{-1}$ does not exist. The **Moore-Penrose pseudoinverse** $A^+ = V \Sigma^+ U^T$ provides a unique generalized inverse by inverting non-zero singular values ($1/\sigma_i$) and transposing.

---

## 2. Worked example

Let $A = \begin{bmatrix} 2 & 0 \\ 0 & 0 \end{bmatrix}$. $\Sigma = \text{diag}(2, 0)$. $\Sigma^+ = \text{diag}(1/2, 0)$. Then $A^+ = \begin{bmatrix} 0.5 & 0 \\ 0 & 0 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[2.0, 0.0], [0.0, 0.0]])
A_pinv = np.linalg.pinv(A)

assert np.allclose(A_pinv, [[0.5, 0.0], [0.0, 0.0]])
# Check Moore-Penrose condition 1: A @ A_pinv @ A == A
assert np.allclose(A @ A_pinv @ A, A)
```

---

## 4. The mistake people actually make

Inverting near-zero singular values without thresholding, causing massive noise amplification.

---

## Check yourself

1. What is the value of 1/sigma_i in Sigma^+ when sigma_i = 0?
2. What solution does x = A^+ b find for overdetermined systems?

<details>
<summary>Answers</summary>

1. It is set to 0.
2. The least-squares solution that minimizes ||x||_2.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](07_Principal_Component_Analysis_via_SVD.md)
