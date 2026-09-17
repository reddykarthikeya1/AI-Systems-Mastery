# Lesson 04.01 — Vectors as Arrows and as Lists

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 1 of 21

---

## What you will be able to do after this lesson

- [ ] Connect the geometric view of vectors (directed arrows) with the algebraic view (ordered lists of numbers).
- [ ] Perform vector operations and verify length invariance in NumPy.

## Prerequisites

- Cartesian coordinates.

---

## 1. The idea

In physics and geometry, a **vector** is a directed arrow having magnitude and direction, invariant to where its tail is placed. In computer science and ML, a vector is an ordered tuple $\mathbf{x} = [x_1, \dots, x_n]^T \in \mathbb{R}^n$ representing coordinates relative to standard basis axes.

---

## 2. Worked example

Vector from $(1, 2)$ to $(4, 6)$ has displacement components $\mathbf{v} = [4-1, 6-2]^T = [3, 4]^T$. Its Euclidean magnitude is $\|\mathbf{v}\| = \sqrt{3^2 + 4^2} = 5$.

---

## 3. Verify it in code

```python
import numpy as np
tail = np.array([1.0, 2.0])
tip = np.array([4.0, 6.0])
v = tip - tail
length = np.linalg.norm(v)
assert np.allclose(v, [3.0, 4.0])
assert np.isclose(length, 5.0)
```

---

## 4. The mistake people actually make

Treating points and vectors as identical objects without recognizing that vectors represent displacements.

---

## Check yourself

1. Does shifting the origin change the displacement vector between two points?
2. What does a coordinate vector represent?

<details>
<summary>Answers</summary>

1. No, displacements are invariant under pure translation.
2. The coordinates of a vector relative to a specific chosen basis.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Vector_Addition_and_Scalar_Multiplication.md)
