# Lesson 03.30 — Composing Transformations

> **Module 03:** Linear Systems and Geometric Maps · Lesson 30 of 35

---

## What you will be able to do after this lesson

- [ ] Multiply transformation matrices in correct sequence: first T1 then T2 is T2 @ T1.
- [ ] Verify non-commutativity of geometric composition.

## Prerequisites

- 03.29 Rotations and Shears.

---

## 1. The idea

Composing transformations evaluates from right to left: applying $A$ then $B$ then $C$ to vector $\mathbf{x}$ is $C(B(A\mathbf{x})) = (C B A)\mathbf{x}$. Because matrix multiplication is associative, the combined transformation matrix $M = CBA$ can be precomputed once and applied to millions of vertices in graphics and robotics.

---

## 2. Worked example

Rotate by 90 degrees then scale x by 2:
$R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}, S = \begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}$. Combined $M = S R = \begin{bmatrix} 0 & -2 \\ 1 & 0 \end{bmatrix}$. Vector $[1, 0]^T$ transforms to $[0, 1]^T$.

---

## 3. Verify it in code

```python
import numpy as np
R = np.array([[0.0, -1.0], [1.0, 0.0]])
S = np.array([[2.0, 0.0], [0.0, 1.0]])
M = S @ R
x = np.array([1.0, 0.0])
assert np.allclose(M @ x, [0.0, 1.0])
```

---

## 4. The mistake people actually make

Multiplying matrices in forward chronological order (T1 @ T2) instead of reverse order (T2 @ T1).

---

## Check yourself

1. What order are matrices multiplied when applying T1 then T2 then T3?
2. What is the key benefit of precomputing M = T3 @ T2 @ T1?

<details>
<summary>Answers</summary>

1. T3 @ T2 @ T1.
2. All transformations collapse into a single matrix, so each point requires only one matrix-vector multiply.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](31_Affine_versus_Linear_Maps.md)
