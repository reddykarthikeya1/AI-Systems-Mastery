# Lesson 04.07 — Linear Independence

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 7 of 21

---

## What you will be able to do after this lesson

- [ ] Define linear independence: c1 v1 + ... + ck vk = 0 implies all c_i = 0.
- [ ] Verify independence using matrix determinant and rank.

## Prerequisites

- 04.06 Span of Vectors.

---

## 1. The idea

A set of vectors is **linearly independent** if no vector in the set can be written as a linear combination of the others:
$$\sum_{i=1}^k c_i \mathbf{v}_i = \mathbf{0} \implies c_1 = c_2 = \dots = c_k = 0$$
If non-trivial weights exist that produce $\mathbf{0}$, the vectors are **linearly dependent** (redundant).

---

## 2. Worked example

Let $\mathbf{v}_1 = [1, 2]^T, \mathbf{v}_2 = [2, 4]^T$. Since $\mathbf{v}_2 = 2\mathbf{v}_1$, $2\mathbf{v}_1 - \mathbf{v}_2 = \mathbf{0}$. The coefficients $(2, -1)$ are non-zero, so the vectors are linearly dependent.

---

## 3. Verify it in code

```python
import numpy as np
# Independent vectors
v1 = np.array([1.0, 0.0])
v2 = np.array([0.0, 1.0])
A_indep = np.column_stack([v1, v2])
assert np.linalg.matrix_rank(A_indep) == 2

# Dependent vectors
v3 = np.array([2.0, 0.0])
A_dep = np.column_stack([v1, v3])
assert np.linalg.matrix_rank(A_dep) == 1
```

---

## 4. The mistake people actually make

Assuming any set containing the zero vector can be independent. Any set containing 0 is automatically dependent since 1 * 0 = 0.

---

## Check yourself

1. Can a set of 4 vectors in R^3 ever be linearly independent?
2. Can a set containing the zero vector be independent?

<details>
<summary>Answers</summary>

1. No, at most 3 vectors can be linearly independent in R^3.
2. Never.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](08_Testing_Independence_by_Elimination.md)
