# Lesson 11.04 — Independence in Terms of Joints

> **Module 11:** Joint Distributions and Covariance · Lesson 4 of 29

---

## What you will be able to do after this lesson

- [ ] State independence as factorization P(X=x, Y=y) = P(X=x) P(Y=y).
- [ ] Test statistical independence via outer product comparison.

## Prerequisites

- 11.02 Marginal Distributions.

---

## 1. The idea

Random variables $X$ and $Y$ are **statistically independent** ($X \perp Y$) if and only if their joint distribution factors into the outer product of their marginals for all pairs: $P(X = x, Y = y) = P(X = x) P(Y = y)$. Equivalently, $P(Y \mid X) = P(Y)$.

---

## 2. Worked example

Let $P(X) = [0.6, 0.4]$ and $P(Y) = [0.5, 0.5]$. If independent, $P(X, Y) = \begin{bmatrix} 0.3 & 0.3 \\ 0.2 & 0.2 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
p_x = np.array([0.6, 0.4])
p_y = np.array([0.5, 0.5])
joint_indep = np.outer(p_x, p_y)

assert np.allclose(joint_indep, [[0.3, 0.3], [0.2, 0.2]])
assert np.allclose(np.sum(joint_indep, axis=1), p_x)
assert np.allclose(np.sum(joint_indep, axis=0), p_y)
```

---

## 4. The mistake people actually make

Assuming variables are independent just because one cell satisfies P(x, y) = P(x)P(y). It must hold for every cell.

---

## Check yourself

1. What is the rank of an independent discrete joint probability matrix?
2. If X and Y are independent, what does P(Y | X) equal?

<details>
<summary>Answers</summary>

1. Rank 1 (it is an outer product of two vectors).
2. P(Y).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](05_Joint_Marginal_and_Conditional_Densities.md)
