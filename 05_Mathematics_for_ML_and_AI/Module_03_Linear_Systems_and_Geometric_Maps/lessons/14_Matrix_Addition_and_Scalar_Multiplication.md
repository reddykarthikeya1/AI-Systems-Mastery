# Lesson 03.14 — Matrix Addition and Scalar Multiplication

> **Module 03:** Linear Systems and Geometric Maps · Lesson 14 of 35

---

## What you will be able to do after this lesson

- [ ] Perform elementwise addition A + B and scalar scaling c A.
- [ ] Verify distributive and commutative laws in NumPy.

## Prerequisites

- 03.04 Matrices as Compact Notation.

---

## 1. The idea

Matrix addition $(A + B)_{ij} = A_{ij} + B_{ij}$ and scalar multiplication $(cA)_{ij} = c A_{ij}$ operate elementwise on matrices of identical dimensions, making the space $\mathbb{R}^{m \times n}$ a vector space of dimension $m \cdot n$.

---

## 2. Worked example

$\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} + 2\begin{bmatrix} 0 & 1 \\ -1 & 2 \end{bmatrix} = \begin{bmatrix} 1 & 4 \\ 1 & 8 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[0.0, 1.0], [-1.0, 2.0]])
res = A + 2.0 * B
assert np.allclose(res, [[1.0, 4.0], [1.0, 8.0]])
```

---

## 4. The mistake people actually make

Attempting to add matrices with mismatched shapes without proper broadcasting rules.

---

## Check yourself

1. What condition is required to add two matrices A and B?
2. Is matrix addition commutative?

<details>
<summary>Answers</summary>

1. They must have identical shapes (dimensions).
2. Yes, A + B = B + A.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](15_Matrix_Multiplication_as_Composition.md)
