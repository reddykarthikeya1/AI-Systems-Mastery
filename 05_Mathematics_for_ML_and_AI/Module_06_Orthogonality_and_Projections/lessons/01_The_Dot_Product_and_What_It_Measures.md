# Lesson 06.01 — The Dot Product and What It Measures

> **Module 06:** Orthogonality and Projections · Lesson 1 of 18

---

## What you will be able to do after this lesson

- [ ] Compute inner product u^T v and express it as ||u|| ||v|| cos(theta).
- [ ] Verify geometric projection using dot products in NumPy.

## Prerequisites

- Vector arithmetic (Module 04).

---

## 1. The idea

The dot product $\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^n u_i v_i = \mathbf{u}^T \mathbf{v}$ bridges algebraic coordinates and geometric concepts of length and angle. It quantifies how much two vectors point in the same direction.

---

## 2. Worked example

Let $\mathbf{u} = [3, 4]^T, \mathbf{v} = [1, 0]^T$. $\mathbf{u} \cdot \mathbf{v} = 3(1) + 4(0) = 3$. $\|\mathbf{u}\| = 5, \|\mathbf{v}\| = 1$. $\cos(\theta) = 3 / 5 = 0.6$.

---

## 3. Verify it in code

```python
import numpy as np
u = np.array([3.0, 4.0])
v = np.array([1.0, 0.0])
dot = np.dot(u, v)
cos_theta = dot / (np.linalg.norm(u) * np.linalg.norm(v))
assert np.isclose(dot, 3.0)
assert np.isclose(cos_theta, 0.6)
```

---

## 4. The mistake people actually make

Conflating elementwise product (u * v) with dot product (np.dot(u, v)).

---

## Check yourself

1. What is the dot product of two perpendicular vectors?
2. Can the dot product be negative?

<details>
<summary>Answers</summary>

1. Exactly zero.
2. Yes, when the angle between them exceeds 90 degrees (obtuse angle).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Norms_L1_L2_and_Beyond.md)
