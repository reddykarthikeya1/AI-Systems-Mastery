# Lesson 04.16 — Rank of a Matrix

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 16 of 21

---

## What you will be able to do after this lesson

- [ ] Define rank(A) as dimension of column space.
- [ ] Prove row rank equals column rank: dim(col(A)) = dim(row(A)).

## Prerequisites

- 04.15 Row Space and Column Space.

---

## 1. The idea

The **rank** of matrix $A$ is the maximum number of linearly independent column vectors. One of the most fundamental miracles of mathematics is that **row rank always equals column rank**: $\dim(\text{col}(A)) = \dim(\text{row}(A)) = \text{rank}(A)$. Rank cannot exceed $\min(m, n)$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \end{bmatrix}$. Rows are multiples ($R_2 = 2R_1 \implies \text{row rank} = 1$). Columns are also multiples ($C_2 = 2C_1, C_3 = 3C_1 \implies \text{col rank} = 1$). Both equal 1.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]])
rank_A = np.linalg.matrix_rank(A)
rank_AT = np.linalg.matrix_rank(A.T)
assert rank_A == 1
assert rank_A == rank_AT
```

---

## 4. The mistake people actually make

Assuming an m x n matrix can have rank > min(m, n).

---

## Check yourself

1. What is the maximum possible rank of a 10 x 3 matrix?
2. Is row rank ever different from column rank?

<details>
<summary>Answers</summary>

1. At most 3.
2. Never; they are always identically equal.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](17_The_RankNullity_Theorem.md)
