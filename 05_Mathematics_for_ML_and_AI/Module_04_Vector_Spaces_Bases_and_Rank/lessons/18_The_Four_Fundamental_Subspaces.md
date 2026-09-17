# Lesson 04.18 — The Four Fundamental Subspaces

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 18 of 21

---

## What you will be able to do after this lesson

- [ ] State Gilbert Strang's Big Picture of Linear Algebra: col(A) perp null(A^T) in R^m and row(A) perp null(A) in R^n.
- [ ] Verify orthogonal complements in NumPy.

## Prerequisites

- Lessons 04.13 through 04.17.

---

## 1. The idea

Strang's Four Fundamental Subspaces:
- In Domain $\mathbb{R}^n$: $\text{row}(A)$ (dim $r$) $\perp$ $\text{null}(A)$ (dim $n-r$).
- In Codomain $\mathbb{R}^m$: $\text{col}(A)$ (dim $r$) $\perp$ $\text{null}(A^T)$ (dim $m-r$).
Every vector in the row space is orthogonal to every vector in the null space!

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 2 \end{bmatrix}$. Row space is $\text{span}([1, 2]^T)$. Null space is $\text{span}([-2, 1]^T)$. Dot product: $1(-2) + 2(1) = 0$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0]])
row_vec = A[0]
null_vec = np.array([-2.0, 1.0])
assert np.isclose(np.dot(row_vec, null_vec), 0.0)
```

---

## 4. The mistake people actually make

Believing col(A) and null(A) are orthogonal. They live in different spaces (R^m vs R^n) when m != n!

---

## Check yourself

1. Which subspace is the orthogonal complement of the null space null(A)?
2. Which subspace is the orthogonal complement of the column space col(A)?

<details>
<summary>Answers</summary>

1. The row space row(A).
2. The left null space null(A^T).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](19_What_Rank_Tells_You_About_a_Dataset.md)
