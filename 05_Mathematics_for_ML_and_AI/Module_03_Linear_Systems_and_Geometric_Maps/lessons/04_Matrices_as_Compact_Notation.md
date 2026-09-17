# Lesson 03.04 — Matrices as Compact Notation

> **Module 03:** Linear Systems and Geometric Maps · Lesson 4 of 35

---

## What you will be able to do after this lesson

- [ ] Convert a system of m linear equations in n variables into matrix equation Ax = b.
- [ ] Verify matrix-vector multiplication in NumPy.

## Prerequisites

- 03.02 Systems of Linear Equations.

---

## 1. The idea

A linear system of $m$ equations in $n$ unknowns can be written compactly as $A\mathbf{x} = \mathbf{b}$, where $A \in \mathbb{R}^{m \times n}$ is the coefficient matrix, $\mathbf{x} \in \mathbb{R}^n$ is the unknown vector, and $\mathbf{b} \in \mathbb{R}^m$ is the right-hand side vector.

---

## 2. Worked example

System: $2x_1 + 3x_2 = 8$ and $x_1 - 4x_2 = -7$. Matrix $A = \begin{bmatrix} 2 & 3 \\ 1 & -4 \end{bmatrix}$, $\mathbf{x} = [x_1, x_2]^T$, $\mathbf{b} = [8, -7]^T$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[2.0, 3.0], [1.0, -4.0]])
b = np.array([8.0, -7.0])
x = np.array([1.0, 2.0])
assert np.allclose(A @ x, b)
```

---

## 4. The mistake people actually make

Transposing row and column indices when translating linear equations into matrix A.

---

## Check yourself

1. What do the rows of matrix A represent in Ax = b?
2. What do the columns of matrix A represent?

<details>
<summary>Answers</summary>

1. Each row represents an individual constraint (equation).
2. Each column represents the coefficients multiplying a specific variable across all equations.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](05_Augmented_Matrices.md)
