# Lesson 06.11 — Gram-Schmidt Orthogonalization

> **Module 06:** Orthogonality and Projections · Lesson 11 of 18

---

## What you will be able to do after this lesson

- [ ] Convert a set of linearly independent vectors into an orthonormal basis.
- [ ] Compute Gram-Schmidt orthogonalization step-by-step.

## Prerequisites

- 06.06 Projection Onto a Line.

---

## 1. The idea

The **Gram-Schmidt process** orthogonalizes vectors $\mathbf{a}_1, \dots, \mathbf{a}_k$:
$\mathbf{u}_1 = \mathbf{a}_1$
$\mathbf{u}_2 = \mathbf{a}_2 - \frac{\mathbf{u}_1^T \mathbf{a}_2}{\mathbf{u}_1^T \mathbf{u}_1}\mathbf{u}_1$
Each new vector has all projections onto previous directions subtracted out. Normalizing $\mathbf{q}_i = \mathbf{u}_i / \|\mathbf{u}_i\|$ yields an orthonormal basis.

---

## 2. Worked example

Let $\mathbf{a}_1 = [1, 1]^T, \mathbf{a}_2 = [1, 2]^T$.
$\mathbf{u}_1 = [1, 1]^T$.
$\mathbf{u}_2 = [1, 2]^T - \frac{3}{2}[1, 1]^T = [-0.5, 0.5]^T$.
Note $\mathbf{u}_1 \cdot \mathbf{u}_2 = -0.5 + 0.5 = 0$.

---

## 3. Verify it in code

```python
import numpy as np
a1 = np.array([1.0, 1.0])
a2 = np.array([1.0, 2.0])

u1 = a1
u2 = a2 - (np.dot(u1, a2) / np.dot(u1, u1)) * u1

assert np.isclose(np.dot(u1, u2), 0.0)
q1 = u1 / np.linalg.norm(u1)
q2 = u2 / np.linalg.norm(u2)
assert np.isclose(np.linalg.norm(q1), 1.0)
assert np.isclose(np.linalg.norm(q2), 1.0)
```

---

## 4. The mistake people actually make

Projecting onto a_j instead of the orthogonalized vector u_j during Gram-Schmidt iterations.

---

## Check yourself

1. Does Gram-Schmidt change the span of the vectors?
2. What happens if Gram-Schmidt is run on linearly dependent vectors?

<details>
<summary>Answers</summary>

1. No, span(q_1, ..., q_k) = span(a_1, ..., a_k) at every step.
2. One of the u_k vectors becomes zero.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](12_Numerical_Failure_of_Classical_GramSchmidt.md)
