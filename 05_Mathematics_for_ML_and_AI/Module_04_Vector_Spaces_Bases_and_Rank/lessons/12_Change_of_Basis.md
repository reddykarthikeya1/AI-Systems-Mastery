# Lesson 04.12 — Change of Basis

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 12 of 21

---

## What you will be able to do after this lesson

- [ ] Construct change-of-basis matrix P_{C <- B} = C^(-1) B.
- [ ] Transform operator matrices between bases as [T]_C = P [T]_B P^(-1).

## Prerequisites

- 04.11 Coordinates Relative to a Basis.

---

## 1. The idea

To convert coordinates from basis $\mathcal{B}$ to basis $\mathcal{C}$:
$$[\mathbf{x}]_\mathcal{C} = P_{\mathcal{C} \leftarrow \mathcal{B}} [\mathbf{x}]_\mathcal{B}, \quad \text{where } P_{\mathcal{C} \leftarrow \mathcal{B}} = C^{-1}B$$
For a linear transformation $T$, its matrix transforms via similarity: $[T]_\mathcal{C} = P [T]_\mathcal{B} P^{-1}$.

---

## 2. Worked example

Let $B = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$ (standard) and $C = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$. $P = C^{-1}B = \begin{bmatrix} 1 & -1 \\ 0 & 1 \end{bmatrix}$. For $[\mathbf{x}]_B = [5, 2]^T$, $[\mathbf{x}]_C = [5-2, 2]^T = [3, 2]^T$.

---

## 3. Verify it in code

```python
import numpy as np
B = np.eye(2)
C = np.array([[1.0, 1.0], [0.0, 1.0]])
P = np.linalg.inv(C) @ B
x_B = np.array([5.0, 2.0])
x_C = P @ x_B
assert np.allclose(x_C, [3.0, 2.0])
assert np.allclose(C @ x_C, B @ x_B)
```

---

## 4. The mistake people actually make

Inverting the wrong basis matrix when constructing the transition matrix P.

---

## Check yourself

1. If P translates from basis B to C, what translates from C to B?
2. What is P_{B <- B}?

<details>
<summary>Answers</summary>

1. The matrix inverse P^(-1).
2. The identity matrix I.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](13_Column_Space.md)
