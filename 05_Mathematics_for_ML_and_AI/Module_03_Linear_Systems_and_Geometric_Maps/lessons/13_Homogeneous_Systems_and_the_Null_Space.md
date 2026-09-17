# Lesson 03.13 — Homogeneous Systems and the Null Space

> **Module 03:** Linear Systems and Geometric Maps · Lesson 13 of 35

---

## What you will be able to do after this lesson

- [ ] Prove homogeneous systems Ax = 0 always have the trivial solution x = 0.
- [ ] Characterize when non-trivial solutions exist (rank < n).

## Prerequisites

- 03.11 Free Variables and 03.12 Consistency.

---

## 1. The idea

A **homogeneous system** $A\mathbf{x} = \mathbf{0}$ is always consistent because $\mathbf{x} = \mathbf{0}$ (the trivial solution) always satisfies it. Non-trivial solutions exist if and only if there is at least one free variable ($\text{rank}(A) < n$). The set of all solutions forms the **null space**.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 3 \end{bmatrix}$. $x_1 + 3x_2 = 0 \implies x_1 = -3x_2$. Non-trivial solution is $[-3, 1]^T$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 3.0]])
v_null = np.array([-3.0, 1.0])
assert np.allclose(A @ v_null, [0.0])
assert not np.allclose(v_null, [0.0, 0.0])
```

---

## 4. The mistake people actually make

Claiming a homogeneous system can have no solutions. The zero vector is always a solution.

---

## Check yourself

1. Can a homogeneous system Ax = 0 ever be inconsistent?
2. Under what condition does Ax = 0 have non-zero solutions?

<details>
<summary>Answers</summary>

1. Never; x = 0 is always a solution.
2. When rank(A) < n (more columns than rank).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](14_Matrix_Addition_and_Scalar_Multiplication.md)
