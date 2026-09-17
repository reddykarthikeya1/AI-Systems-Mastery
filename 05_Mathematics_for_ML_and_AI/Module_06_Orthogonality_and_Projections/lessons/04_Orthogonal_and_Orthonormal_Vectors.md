# Lesson 06.04 — Orthogonal and Orthonormal Vectors

> **Module 06:** Orthogonality and Projections · Lesson 4 of 18

---

## What you will be able to do after this lesson

- [ ] Define orthogonal (u^T v = 0) and orthonormal (u_i^T u_j = delta_ij) sets.
- [ ] Verify Pythagorean theorem ||u + v||^2 = ||u||^2 + ||v||^2 for orthogonal vectors.

## Prerequisites

- 06.01 The Dot Product.

---

## 1. The idea

Vectors are **orthogonal** if their inner product is zero ($\mathbf{u} \cdot \mathbf{v} = 0$). They are **orthonormal** if they are pairwise orthogonal and each has unit length ($\|\mathbf{u}_i\| = 1$).

---

## 2. Worked example

Let $\mathbf{u} = [1, 1]^T / \sqrt{2}, \mathbf{v} = [-1, 1]^T / \sqrt{2}$. $\mathbf{u} \cdot \mathbf{v} = (-1 + 1)/2 = 0$. $\|\mathbf{u}\| = 1, \|\mathbf{v}\| = 1$. They form an orthonormal set.

---

## 3. Verify it in code

```python
import numpy as np
u = np.array([1.0, 1.0]) / np.sqrt(2)
v = np.array([-1.0, 1.0]) / np.sqrt(2)
assert np.isclose(np.dot(u, v), 0.0)
assert np.isclose(np.linalg.norm(u), 1.0)
assert np.isclose(np.linalg.norm(v), 1.0)
# Pythagorean theorem
assert np.isclose(np.linalg.norm(u + v)**2, np.linalg.norm(u)**2 + np.linalg.norm(v)**2)
```

---

## 4. The mistake people actually make

Assuming non-zero orthogonal vectors must be of unit length. Orthogonality only requires dot product zero.

---

## Check yourself

1. Can a set of non-zero mutually orthogonal vectors be linearly dependent?
2. What is the dot product of any orthonormal vector with itself?

<details>
<summary>Answers</summary>

1. No, any set of mutually orthogonal non-zero vectors is always linearly independent.
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

[Module README](../README.md) · [Next →](05_Orthogonal_Complements.md)
