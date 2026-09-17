# Lesson 03.05 — Augmented Matrices

> **Module 03:** Linear Systems and Geometric Maps · Lesson 5 of 35

---

## What you will be able to do after this lesson

- [ ] Construct the augmented matrix [A | b] for linear systems.
- [ ] Manipulate augmented matrices in NumPy.

## Prerequisites

- 03.04 Matrices as Compact Notation.

---

## 1. The idea

An **augmented matrix** $[A \mid \mathbf{b}]$ concatenates the coefficient matrix $A$ and constant vector $\mathbf{b}$ into an $m \times (n+1)$ table, keeping track of equations and constants together without writing variable names.

---

## 2. Worked example

For system with $A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$ and $\mathbf{b} = [5, 11]^T$, augmented matrix is $[A \mid \mathbf{b}] = \begin{bmatrix} 1 & 2 & 5 \\ 3 & 4 & 11 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0], [3.0, 4.0]])
b = np.array([5.0, 11.0])
Ab = np.column_stack([A, b])
assert Ab.shape == (2, 3)
assert np.allclose(Ab[:, -1], b)
```

---

## 4. The mistake people actually make

Applying a row operation to the coefficient block A while forgetting to update the constant vector b.

---

## Check yourself

1. What is the shape of [A | b] for an m x n system?
2. Why are augmented matrices useful?

<details>
<summary>Answers</summary>

1. Shape is m x (n + 1).
2. They permit simultaneous row operations on equations and constants.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](06_Elementary_Row_Operations.md)
