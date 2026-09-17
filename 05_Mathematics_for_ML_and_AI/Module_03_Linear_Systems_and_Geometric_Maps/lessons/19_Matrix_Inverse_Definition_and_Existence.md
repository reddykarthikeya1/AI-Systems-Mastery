# Lesson 03.19 — Matrix Inverse: Definition and Existence

> **Module 03:** Linear Systems and Geometric Maps · Lesson 19 of 35

---

## What you will be able to do after this lesson

- [ ] Define inverse A^(-1) such that A A^(-1) = A^(-1) A = I.
- [ ] State invertibility criteria: square, full rank, non-zero determinant.

## Prerequisites

- 03.17 The Identity Matrix.

---

## 1. The idea

A square matrix $A \in \mathbb{R}^{n \times n}$ is **invertible** (or non-singular) if there exists $A^{-1}$ such that $A A^{-1} = A^{-1} A = I_n$. If $\det(A) = 0$ or $\text{rank}(A) < n$, $A$ has a non-trivial null space and no inverse exists.

---

## 2. Worked example

For $2 \times 2$ matrix $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$, $A^{-1} = \frac{1}{ad - bc}\begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$ provided $ad - bc \neq 0$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[4.0, 7.0], [2.0, 6.0]])
A_inv = np.linalg.inv(A)
assert np.allclose(A @ A_inv, np.eye(2))
assert np.allclose(A_inv @ A, np.eye(2))
```

---

## 4. The mistake people actually make

Attempting to invert a non-square rectangular matrix with standard matrix inverse.

---

## Check yourself

1. What is (A B)^(-1) for invertible matrices?
2. Can a matrix with determinant 0 be inverted?

<details>
<summary>Answers</summary>

1. B^(-1) A^(-1) (order is reversed).
2. No, singular matrices have no inverse.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](20_Computing_the_Inverse_by_Elimination.md)
