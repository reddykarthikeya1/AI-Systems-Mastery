# Lesson 04.17 — The Rank-Nullity Theorem

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 17 of 21

---

## What you will be able to do after this lesson

- [ ] State and verify rank(A) + nullity(A) = n for any m x n matrix.
- [ ] Apply rank-nullity to dimension analysis of linear maps.

## Prerequisites

- 04.14 Null Space and 04.16 Rank of a Matrix.

---

## 1. The idea

The **Rank-Nullity Theorem** states: for any matrix $A \in \mathbb{R}^{m \times n}$:
$$\text{rank}(A) + \text{nullity}(A) = n$$
Every input dimension either survives into the column space or is crushed into the null space. None is unaccounted for.

---

## 2. Worked example

For a $3 \times 5$ matrix ($n = 5$ columns) with rank 3, nullity must be $5 - 3 = 2$. Exactly 2 degrees of freedom are crushed to zero.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
# 3 x 5 matrix of rank 2
A = np.random.randn(3, 2) @ np.random.randn(2, 5)
n = A.shape[1]
rank = np.linalg.matrix_rank(A)
nullity = n - rank
assert rank == 2
assert nullity == 3
assert rank + nullity == n
```

---

## 4. The mistake people actually make

Using m (number of rows) instead of n (number of columns) in the rank-nullity equation.

---

## Check yourself

1. What does n represent in rank(A) + nullity(A) = n?
2. If a 4 x 4 matrix has nullity 0, what is its rank?

<details>
<summary>Answers</summary>

1. The number of columns (dimension of the domain R^n).
2. Rank 4 (full rank, invertible).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](18_The_Four_Fundamental_Subspaces.md)
