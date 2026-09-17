# Lesson 03.28 — Linear Maps as Geometric Transformations

> **Module 03:** Linear Systems and Geometric Maps · Lesson 28 of 35

---

## What you will be able to do after this lesson

- [ ] Prove a map T is linear iff T(c u + d v) = c T(u) + d T(v).
- [ ] Represent any linear transformation by the matrix of its basis images.

## Prerequisites

- 03.04 Matrices as Compact Notation.

---

## 1. The idea

A transformation $T: \mathbb{R}^n \to \mathbb{R}^m$ is a **linear map** if it preserves vector addition and scalar multiplication: $T(c\mathbf{u} + d\mathbf{v}) = c T(\mathbf{u}) + d T(\mathbf{v})$. Crucially, grid lines remain parallel and evenly spaced, and the origin never moves ($T(\mathbf{0}) = \mathbf{0}$). Its matrix columns are simply the transformed standard basis vectors $T(\mathbf{e}_j)$.

---

## 2. Worked example

If $T(\mathbf{e}_1) = [2, 1]^T$ and $T(\mathbf{e}_2) = [-1, 3]^T$, the transformation matrix is $A = \begin{bmatrix} 2 & -1 \\ 1 & 3 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
e1 = np.array([1.0, 0.0])
e2 = np.array([0.0, 1.0])
A = np.array([[2.0, -1.0], [1.0, 3.0]])
assert np.allclose(A @ e1, [2.0, 1.0])
assert np.allclose(A @ e2, [-1.0, 3.0])
assert np.allclose(A @ np.zeros(2), np.zeros(2))
```

---

## 4. The mistake people actually make

Treating translation f(x) = x + b as a linear transformation. Translation moves the origin, so it is affine, not linear.

---

## Check yourself

1. Can a linear transformation move the origin?
2. What do the columns of transformation matrix A represent?

<details>
<summary>Answers</summary>

1. No, T(0) must equal 0.
2. The images of the standard basis vectors: T(e_1), ..., T(e_n).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](29_Rotations_Reflections_Scalings_and_Shears.md)
