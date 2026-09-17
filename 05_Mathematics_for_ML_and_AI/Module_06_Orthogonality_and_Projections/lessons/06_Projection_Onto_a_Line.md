# Lesson 06.06 — Projection Onto a Line

> **Module 06:** Orthogonality and Projections · Lesson 6 of 18

---

## What you will be able to do after this lesson

- [ ] Derive scalar projection c = (a^T b) / (a^T a) and projection vector p = c a.
- [ ] Verify error vector e = b - p is perpendicular to a.

## Prerequisites

- 06.01 The Dot Product.

---

## 1. The idea

Projecting vector $\mathbf{b}$ onto the line spanned by $\mathbf{a}$ finds the closest point $\mathbf{p} = \hat{x}\mathbf{a}$. Orthogonality condition $\mathbf{a}^T(\mathbf{b} - \hat{x}\mathbf{a}) = 0 \implies \hat{x} = \frac{\mathbf{a}^T \mathbf{b}}{\mathbf{a}^T \mathbf{a}}$. The projection matrix is $P = \frac{\mathbf{a}\mathbf{a}^T}{\mathbf{a}^T \mathbf{a}}$.

---

## 2. Worked example

Let $\mathbf{a} = [1, 0]^T, \mathbf{b} = [3, 4]^T$. $\hat{x} = 3(1)/1 = 3$. $\mathbf{p} = [3, 0]^T$. Error $\mathbf{e} = \mathbf{b} - \mathbf{p} = [0, 4]^T$. Note $\mathbf{a} \cdot \mathbf{e} = 1(0) + 0(4) = 0$.

---

## 3. Verify it in code

```python
import numpy as np
a = np.array([1.0, 0.0])
b = np.array([3.0, 4.0])
p = (np.dot(a, b) / np.dot(a, a)) * a
e = b - p
assert np.allclose(p, [3.0, 0.0])
assert np.isclose(np.dot(a, e), 0.0)
```

---

## 4. The mistake people actually make

Dividing by ||a|| instead of ||a||^2 when computing the scalar projection coefficient along non-unit vector a.

---

## Check yourself

1. What is the projection matrix P onto line spanned by unit vector u?
2. What is the dot product between the error vector e and the direction vector a?

<details>
<summary>Answers</summary>

1. P = u u^T.
2. Zero (e is orthogonal to a).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](07_Projection_Onto_a_Subspace.md)
