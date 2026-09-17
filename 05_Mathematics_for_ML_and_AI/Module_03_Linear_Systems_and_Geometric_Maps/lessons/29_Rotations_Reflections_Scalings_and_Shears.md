# Lesson 03.29 — Rotations, Reflections, Scalings and Shears

> **Module 03:** Linear Systems and Geometric Maps · Lesson 29 of 35

---

## What you will be able to do after this lesson

- [ ] Construct 2D matrices for rotation R(theta), reflection, non-uniform scaling, and horizontal/vertical shear.
- [ ] Verify geometric properties in NumPy.

## Prerequisites

- 03.28 Linear Maps as Geometric Transformations.

---

## 1. The idea

Fundamental 2D linear building blocks:
- **Rotation**: $R_\theta = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$
- **Scaling**: $S = \begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix}$
- **Reflection**: $M_x = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$
- **Shear**: $H_x = \begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ (preserves area, $\det = 1$).

---

## 2. Worked example

Horizontal shear with $k = 2$: point $(1, 1)$ transforms to $(1 + 2(1), 1) = (3, 1)$. Area of unit square is preserved: $\det(H) = 1(1) - 2(0) = 1$.

---

## 3. Verify it in code

```python
import numpy as np
theta = np.pi / 2
R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
v = np.array([1.0, 0.0])
assert np.allclose(R @ v, [0.0, 1.0])

H = np.array([[1.0, 2.0], [0.0, 1.0]])
p = np.array([1.0, 1.0])
assert np.allclose(H @ p, [3.0, 1.0])
assert np.isclose(np.linalg.det(H), 1.0)
```

---

## 4. The mistake people actually make

Assuming shear transformations alter area. A pure shear preserves area perfectly (det = 1).

---

## Check yourself

1. What is the determinant of a shear matrix?
2. What is the determinant of a 2D rotation matrix?

<details>
<summary>Answers</summary>

1. Exactly 1.0.
2. Exactly 1.0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](30_Composing_Transformations.md)
