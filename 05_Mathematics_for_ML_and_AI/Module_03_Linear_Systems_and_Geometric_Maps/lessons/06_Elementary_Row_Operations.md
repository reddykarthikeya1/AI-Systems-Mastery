# Lesson 03.06 — Elementary Row Operations

> **Module 03:** Linear Systems and Geometric Maps · Lesson 6 of 35

---

## What you will be able to do after this lesson

- [ ] Apply the 3 elementary row operations: swap rows, scale row, add multiple of row to another.
- [ ] Prove that elementary row operations preserve the solution set.

## Prerequisites

- 03.05 Augmented Matrices.

---

## 1. The idea

The 3 elementary row operations (swapping $R_i \leftrightarrow R_j$, scaling $R_i \leftarrow c R_i$ ($c \neq 0$), and adding $R_i \leftarrow R_i + c R_j$) are reversible linear transformations represented by invertible elementary matrices $E$. Therefore $\text{sol}(A\mathbf{x} = \mathbf{b}) = \text{sol}(EA\mathbf{x} = E\mathbf{b})$.

---

## 2. Worked example

Augmented row: $[2, 4 \mid 10]$. Scale by $0.5$: $[1, 2 \mid 5]$. Solution set is unchanged.

---

## 3. Verify it in code

```python
import numpy as np
M = np.array([[2.0, 4.0, 10.0], [1.0, -1.0, 2.0]])
# Swap
M[[0, 1]] = M[[1, 0]]
assert np.allclose(M[0], [1.0, -1.0, 2.0])
# Add -2 * R0 to R1
M[1] -= 2.0 * M[0]
assert np.allclose(M[1], [0.0, 6.0, 6.0])
```

---

## 4. The mistake people actually make

Multiplying a row by scalar zero, which destroys information and alters the solution space.

---

## Check yourself

1. Can a row be scaled by 0 in elementary row operations?
2. Why do elementary row operations preserve solutions?

<details>
<summary>Answers</summary>

1. No, the scalar must be strictly non-zero.
2. Because each operation is reversible via an inverse elementary operation.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](07_Row_Echelon_Form.md)
