# Lesson 03.32 — Homogeneous Coordinates

> **Module 03:** Linear Systems and Geometric Maps · Lesson 32 of 35

---

## What you will be able to do after this lesson

- [ ] Embed 2D/3D affine transformations into (n+1)x(n+1) linear matrix multiplications.
- [ ] Perform unified rotation, scaling, and translation in NumPy.

## Prerequisites

- 03.31 Affine versus Linear Maps.

---

## 1. The idea

**Homogeneous coordinates** append a 1 to vectors: $\tilde{\mathbf{x}} = [x, y, 1]^T$. This unifies translation into matrix multiplication:
$$\begin{bmatrix} \mathbf{y} \\ 1 \end{bmatrix} = \begin{bmatrix} A & \mathbf{b} \\ \mathbf{0}^T & 1 \end{bmatrix} \begin{bmatrix} \mathbf{x} \\ 1 \end{bmatrix}$$
This allows graphics engines, robotics kinematics, and spatial transformers to compose rotations, shears, and translations into a single matrix product.

---

## 2. Worked example

Translate by $(dx=3, dy=5)$: $T = \begin{bmatrix} 1 & 0 & 3 \\ 0 & 1 & 5 \\ 0 & 0 & 1 \end{bmatrix}$. Multiplying $[2, 4, 1]^T$ yields $[2+3, 4+5, 1]^T = [5, 9, 1]^T$.

---

## 3. Verify it in code

```python
import numpy as np
# 2D Affine transform in 3x3 homogeneous coordinates
dx, dy = 3.0, 5.0
T = np.array([
    [1.0, 0.0, dx],
    [0.0, 1.0, dy],
    [0.0, 0.0, 1.0]
])

p_homo = np.array([2.0, 4.0, 1.0])
p_out = T @ p_homo
assert np.allclose(p_out, [5.0, 9.0, 1.0])
```

---

## 4. The mistake people actually make

Adding the extra coordinate 1 to direction vectors. Point coordinates use 1, while direction/velocity vectors use 0 (so translation ignores them).

---

## Check yourself

1. What is the value of the trailing coordinate for a point in homogeneous coordinates?
2. What is the trailing coordinate for a pure direction vector?

<details>
<summary>Answers</summary>

1. 1.
2. 0 (so translations have no effect).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](33_Least_Squares_via_the_Normal_Equations.md)
