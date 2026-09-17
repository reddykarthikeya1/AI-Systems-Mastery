# Lesson 04.06 — Span of a Set of Vectors

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 6 of 21

---

## What you will be able to do after this lesson

- [ ] Define span(S) as the set of all linear combinations of S.
- [ ] Check whether target vector b lies in span(A) via rank.

## Prerequisites

- 04.02 Linear Combinations and 04.05 Subspaces.

---

## 1. The idea

The **span** of vectors $\{\mathbf{v}_1, \dots, \mathbf{v}_k\}$ is the set of all possible linear combinations: $\text{span}(\mathbf{v}_1, \dots, \mathbf{v}_k) = \{\sum_{i=1}^k c_i \mathbf{v}_i : c_i \in \mathbb{R}\}$. The span of any set of vectors is guaranteed to be a valid subspace.

---

## 2. Worked example

In $\mathbb{R}^3$, the span of $\mathbf{v}_1 = [1, 0, 0]^T$ and $\mathbf{v}_2 = [0, 1, 0]^T$ is the entire 2D xy-plane ($z = 0$). Vector $[2, 5, 0]^T \in \text{span}$, but $[2, 5, 1]^T \notin \text{span}$.

---

## 3. Verify it in code

```python
import numpy as np
v1 = np.array([1.0, 0.0, 0.0])
v2 = np.array([0.0, 1.0, 0.0])
A = np.column_stack([v1, v2])

b_in = np.array([2.0, 5.0, 0.0])
b_out = np.array([2.0, 5.0, 1.0])

# b in span(A) iff rank([A b]) == rank(A)
assert np.linalg.matrix_rank(np.column_stack([A, b_in])) == np.linalg.matrix_rank(A)
assert np.linalg.matrix_rank(np.column_stack([A, b_out])) > np.linalg.matrix_rank(A)
```

---

## 4. The mistake people actually make

Assuming the span of 3 vectors in R^3 must be all of R^3. If vectors are coplanar, their span is only a 2D plane.

---

## Check yourself

1. What is the span of a single non-zero vector in R^3?
2. Is span(S) always a subspace?

<details>
<summary>Answers</summary>

1. A line passing through the origin.
2. Yes, the span of any set of vectors is always a subspace.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](07_Linear_Independence.md)
