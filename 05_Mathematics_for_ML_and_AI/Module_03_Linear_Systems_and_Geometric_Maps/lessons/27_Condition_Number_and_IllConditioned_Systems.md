# Lesson 03.27 — Condition Number and Ill-Conditioned Systems

> **Module 03:** Linear Systems and Geometric Maps · Lesson 27 of 35

---

## What you will be able to do after this lesson

- [ ] Define condition number kappa(A) = ||A|| ||A^(-1)|| = sigma_max / sigma_min.
- [ ] Quantify how condition number bounds relative output error: delta x / x <= kappa delta b / b.

## Prerequisites

- 03.19 Matrix Inverse and 07.01 SVD.

---

## 1. The idea

The **condition number** $\kappa(A) = \|A\| \|A^{-1}\| = \frac{\sigma_{\max}}{\sigma_{\min}} \ge 1$ measures how sensitive the solution to $A\mathbf{x} = \mathbf{b}$ is to errors in $\mathbf{b}$ or $A$. A rule of thumb: if $\kappa(A) \approx 10^k$, solving $A\mathbf{x} = \mathbf{b}$ loses approximately $k$ digits of precision in floating point arithmetic.

---

## 2. Worked example

Let $A$ have $\sigma_{\max} = 1000$ and $\sigma_{\min} = 0.01$. $\kappa(A) = 1000 / 0.01 = 10^5$. In float32 (which has $\approx 7$ decimal digits of precision), roughly 5 digits are lost, leaving only 2 reliable digits.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 1.0], [1.0, 1.0001]])
cond = np.linalg.cond(A)
assert cond > 1e4

# Small perturbation in b
b = np.array([2.0, 2.0001])
x = np.linalg.solve(A, b)
b_perturbed = np.array([2.0, 2.0002])
x_perturbed = np.linalg.solve(A, b_perturbed)

# Large change in x
rel_err_b = np.linalg.norm(b - b_perturbed) / np.linalg.norm(b)
rel_err_x = np.linalg.norm(x - x_perturbed) / np.linalg.norm(x)
assert rel_err_x > rel_err_b * 1000
```

---

## 4. The mistake people actually make

Assuming full rank implies a system is easy to solve accurately. An ill-conditioned full-rank matrix is practically singular.

---

## Check yourself

1. What is the condition number of an orthogonal matrix?
2. Roughly how many decimal digits of precision are lost if kappa(A) = 10^6?

<details>
<summary>Answers</summary>

1. Exactly 1.0.
2. Approximately 6 decimal digits.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](28_Linear_Maps_as_Geometric_Transformations.md)
