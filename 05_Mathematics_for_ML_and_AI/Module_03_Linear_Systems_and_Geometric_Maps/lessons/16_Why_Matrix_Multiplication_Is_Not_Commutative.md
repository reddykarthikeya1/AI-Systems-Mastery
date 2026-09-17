# Lesson 03.16 — Why Matrix Multiplication Is Not Commutative

> **Module 03:** Linear Systems and Geometric Maps · Lesson 16 of 35

---

## What you will be able to do after this lesson

- [ ] Prove AB != BA in general using geometric rotation and reflection examples.
- [ ] Identify commutators [A, B] = AB - BA.

## Prerequisites

- 03.15 Matrix Multiplication as Composition.

---

## 1. The idea

Unlike real numbers, matrix multiplication is **non-commutative**: in general $AB \neq BA$. Geometrically, the order of geometric transformations matters: reflecting across the x-axis then rotating 90 degrees produces a different orientation than rotating 90 degrees then reflecting.

---

## 2. Worked example

Let $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$ and $B = \begin{bmatrix} 0 & 0 \\ 1 & 0 \end{bmatrix}$. $AB = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$, but $BA = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}$. Clearly $AB \neq BA$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[0.0, 1.0], [0.0, 0.0]])
B = np.array([[0.0, 0.0], [1.0, 0.0]])
AB = A @ B
BA = B @ A
assert not np.allclose(AB, BA)
assert np.allclose(AB - BA, [[1.0, 0.0], [0.0, -1.0]])
```

---

## 4. The mistake people actually make

Assuming (A + B)^2 = A^2 + 2AB + B^2. Because AB != BA, (A + B)^2 = A^2 + AB + BA + B^2.

---

## Check yourself

1. What is (A + B)^2 expanded correctly for matrices?
2. When do two diagonal matrices commute?

<details>
<summary>Answers</summary>

1. A^2 + AB + BA + B^2.
2. Always; diagonal matrices always commute with each other.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](17_The_Identity_Matrix.md)
