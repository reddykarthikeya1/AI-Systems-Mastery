# Lesson 04.05 — Subspaces and How to Test for One

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 5 of 21

---

## What you will be able to do after this lesson

- [ ] Test a subset for the 3 subspace criteria: contains 0, closed under addition, closed under scalar multiplication.
- [ ] Verify that lines/planes not passing through the origin are NOT subspaces.

## Prerequisites

- 04.03 Vector Space Axioms.

---

## 1. The idea

A subset $W \subseteq V$ is a **subspace** if and only if:
1. The zero vector $\mathbf{0} \in W$.
2. If $\mathbf{u}, \mathbf{v} \in W$, then $\mathbf{u} + \mathbf{v} \in W$ (closed under addition).
3. If $\mathbf{u} \in W$ and $c \in \mathbb{R}$, then $c\mathbf{u} \in W$ (closed under scalar multiplication).

---

## 2. Worked example

The line $x_1 + x_2 = 0$ is a subspace: $(0, 0)$ is on the line, sum of two points is on the line, and scaling preserves the line. The line $x_1 + x_2 = 1$ is NOT a subspace because $(0, 0)$ is not on the line.

---

## 3. Verify it in code

```python
import numpy as np
# Test line through origin x1 + x2 = 0
v1 = np.array([1.0, -1.0])
v2 = np.array([-3.0, 3.0])
zero = np.array([0.0, 0.0])

# Subspace checks
assert np.isclose(zero[0] + zero[1], 0.0)
assert np.isclose((v1 + v2)[0] + (v1 + v2)[1], 0.0)
assert np.isclose((5.0 * v1)[0] + (5.0 * v1)[1], 0.0)
```

---

## 4. The mistake people actually make

Claiming an affine plane (e.g. z = 5) is a subspace. Because 0 is not in the plane, it is not a subspace.

---

## Check yourself

1. Why is a plane not passing through the origin never a vector subspace?
2. How many conditions are needed to verify a subset is a subspace?

<details>
<summary>Answers</summary>

1. Because it does not contain the zero vector.
2. Three: contains zero, closed under addition, closed under scalar multiplication.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](06_Span_of_a_Set_of_Vectors.md)
