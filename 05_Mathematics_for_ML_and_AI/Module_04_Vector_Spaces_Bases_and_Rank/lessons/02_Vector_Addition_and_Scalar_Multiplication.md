# Lesson 04.02 — Vector Addition and Scalar Multiplication

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 2 of 21

---

## What you will be able to do after this lesson

- [ ] Visualize vector addition via tip-to-tail and parallelogram rules.
- [ ] Compute linear combinations c1 v1 + c2 v2 in NumPy.

## Prerequisites

- 04.01 Vectors as Arrows and Lists.

---

## 1. The idea

The two primitive operations defining linear algebra are:
1. **Vector Addition**: $\mathbf{u} + \mathbf{v} = [u_1+v_1, \dots, u_n+v_n]^T$ (combining displacements).
2. **Scalar Multiplication**: $c\mathbf{v} = [c v_1, \dots, c v_n]^T$ (scaling length and reversing direction if $c < 0$).

---

## 2. Worked example

Let $\mathbf{u} = [1, 2]^T, \mathbf{v} = [3, -1]^T$. Linear combination $2\mathbf{u} - \mathbf{v} = 2[1, 2]^T - [3, -1]^T = [2-3, 4-(-1)]^T = [-1, 5]^T$.

---

## 3. Verify it in code

```python
import numpy as np
u = np.array([1.0, 2.0])
v = np.array([3.0, -1.0])
comb = 2.0 * u - v
assert np.allclose(comb, [-1.0, 5.0])
```

---

## 4. The mistake people actually make

Adding vectors of mismatched dimensions (e.g. R^2 with R^3).

---

## Check yourself

1. What is the geometric interpretation of vector addition?
2. What does multiplying a vector by scalar -1 do?

<details>
<summary>Answers</summary>

1. Placing the tail of the second vector at the tip of the first vector.
2. Reverses the vector direction by 180 degrees while preserving length.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](03_The_Vector_Space_Axioms.md)
