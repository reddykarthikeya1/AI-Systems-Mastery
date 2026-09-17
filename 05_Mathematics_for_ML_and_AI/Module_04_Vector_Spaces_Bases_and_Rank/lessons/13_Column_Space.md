# Lesson 04.13 — Column Space

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 13 of 21

---

## What you will be able to do after this lesson

- [ ] Define column space col(A) = span(columns of A).
- [ ] State the solvability criterion: Ax = b is solvable iff b in col(A).

## Prerequisites

- 04.06 Span of Vectors and Matrix-Vector multiplication.

---

## 1. The idea

The **column space** $\text{col}(A)$ of $A \in \mathbb{R}^{m \times n}$ is the span of its column vectors. Since $A\mathbf{x} = \sum x_i \mathbf{a}_i$, the equation $A\mathbf{x} = \mathbf{b}$ has a solution if and only if $\mathbf{b}$ lies in the column space of $A$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$. Columns are parallel. $\text{col}(A) = \text{span}([1, 2]^T)$. Target $\mathbf{b}_1 = [3, 6]^T \in \text{col}(A)$ is solvable ($x = [3, 0]^T$), but $\mathbf{b}_2 = [1, 1]^T \notin \text{col}(A)$ has no solution.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0], [2.0, 4.0]])
b_solvable = np.array([3.0, 6.0])
b_unsolvable = np.array([1.0, 1.0])

assert np.linalg.matrix_rank(A) == 1
assert np.linalg.matrix_rank(np.column_stack([A, b_solvable])) == 1
assert np.linalg.matrix_rank(np.column_stack([A, b_unsolvable])) == 2
```

---

## 4. The mistake people actually make

Thinking col(A) is a subspace of R^n. Since columns have m entries, col(A) is a subspace of R^m.

---

## Check yourself

1. In which space does col(A) live for an m x n matrix?
2. What condition on b makes Ax = b consistent?

<details>
<summary>Answers</summary>

1. In R^m (the codomain).
2. b must belong to col(A).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](14_Null_Space_and_Nullity.md)
