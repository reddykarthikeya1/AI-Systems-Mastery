# Lesson 06.15 — Orthogonal Matrices and Isometries

> **Module 06:** Orthogonality and Projections · Lesson 15 of 18

---

## What you will be able to do after this lesson

- [ ] Prove orthogonal transformations preserve vector lengths (isometry) and inner products.
- [ ] Verify condition number kappa(Q) = 1.

## Prerequisites

- 06.04 Orthogonal Vectors.

---

## 1. The idea

A square matrix $Q$ is **orthogonal** if $Q^T Q = Q Q^T = I$. It acts as an **isometry**: $\|Q\mathbf{x}\| = \|\mathbf{x}\|$ and $(Q\mathbf{u}) \cdot (Q\mathbf{v}) = \mathbf{u} \cdot \mathbf{v}$. Orthogonal maps perform rigid rotations and reflections, never amplifying numerical noise ($\kappa(Q) = 1$).

---

## 2. Worked example

Let $Q = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$ for $\theta = \pi/4$. Length of $\mathbf{x} = [2, 0]^T$ is 2. Length of $Q\mathbf{x} = [\sqrt{2}, \sqrt{2}]^T$ is $\sqrt{2+2} = 2$.

---

## 3. Verify it in code

```python
import numpy as np
theta = np.pi / 4
Q = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])

assert np.allclose(Q.T @ Q, np.eye(2))
x = np.array([3.0, -4.0])
assert np.isclose(np.linalg.norm(Q @ x), np.linalg.norm(x))
assert np.isclose(np.linalg.cond(Q), 1.0)
```

---

## 4. The mistake people actually make

Assuming an orthogonal matrix must have determinant +1. Det can be +1 (rotation) or -1 (reflection).

---

## Check yourself

1. What is the condition number of an orthogonal matrix?
2. What are the two possible values for det(Q) of an orthogonal matrix?

<details>
<summary>Answers</summary>

1. Exactly 1.0.
2. +1 (pure rotation) or -1 (reflection).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](16_Orthogonal_Bases_for_Function_Spaces.md)
