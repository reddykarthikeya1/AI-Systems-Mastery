# Lesson 04.11 — Coordinates Relative to a Basis

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 11 of 21

---

## What you will be able to do after this lesson

- [ ] Compute coordinate vector [x]_B by solving B [x]_B = x.
- [ ] Verify that coordinate mapping is an isomorphism.

## Prerequisites

- 04.09 Basis of a Vector Space.

---

## 1. The idea

Given basis $\mathcal{B} = \{\mathbf{b}_1, \dots, \mathbf{b}_n\}$, the **coordinates** $[\mathbf{x}]_\mathcal{B} = [c_1, \dots, c_n]^T$ are the unique scalars such that $\mathbf{x} = \sum c_i \mathbf{b}_i$. In matrix notation: $\mathbf{x} = B [\mathbf{x}]_\mathcal{B} \implies [\mathbf{x}]_\mathcal{B} = B^{-1}\mathbf{x}$.

---

## 2. Worked example

Let $B = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$ and $\mathbf{x} = [4, 9]^T$. Then $[\mathbf{x}]_B = B^{-1}\mathbf{x} = [4/2, 9/3]^T = [2, 3]^T$.

---

## 3. Verify it in code

```python
import numpy as np
B = np.array([[2.0, 0.0], [0.0, 3.0]])
x = np.array([4.0, 9.0])
coords = np.linalg.solve(B, x)
assert np.allclose(coords, [2.0, 3.0])
assert np.allclose(B @ coords, x)
```

---

## 4. The mistake people actually make

Multiplying B @ x instead of inverting/solving B [x]_B = x to find coordinates.

---

## Check yourself

1. What matrix converts coordinates [x]_B to standard coordinates x?
2. What matrix converts standard coordinates to [x]_B?

<details>
<summary>Answers</summary>

1. The basis matrix B.
2. The inverse basis matrix B^(-1).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](12_Change_of_Basis.md)
