# Lesson 04.10 — Dimension and Why It Is Well Defined

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 10 of 21

---

## What you will be able to do after this lesson

- [ ] State the Dimension Theorem: all bases of a vector space have the exact same number of elements.
- [ ] Determine the dimension of subspaces in NumPy.

## Prerequisites

- 04.09 Basis of a Vector Space.

---

## 1. The idea

The **dimension** $\dim(V)$ of a vector space $V$ is the number of vectors in any basis. While a space has infinitely many bases, the Fundamental Theorem of Linear Algebra guarantees every basis has the exact same cardinality.

---

## 2. Worked example

In $\mathbb{R}^3$, the xy-plane has basis $\{[1, 0, 0]^T, [0, 1, 0]^T\}$ (size 2). Another basis is $\{[1, 1, 0]^T, [1, -1, 0]^T\}$ (size 2). Both have 2 vectors, so the dimension is 2.

---

## 3. Verify it in code

```python
import numpy as np
# Basis 1
B1 = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])
# Basis 2
B2 = np.array([[1.0, 1.0], [1.0, -1.0], [0.0, 0.0]])

dim1 = np.linalg.matrix_rank(B1)
dim2 = np.linalg.matrix_rank(B2)
assert dim1 == 2
assert dim2 == 2
```

---

## 4. The mistake people actually make

Confusing the number of elements in a vector (its ambient coordinate length) with the dimension of the subspace.

---

## Check yourself

1. Can a 2D subspace of R^5 have a basis with 3 vectors?
2. What is the dimension of the zero subspace {0}?

<details>
<summary>Answers</summary>

1. No, any basis of a 2D space must contain exactly 2 vectors.
2. Zero.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](11_Coordinates_Relative_to_a_Basis.md)
