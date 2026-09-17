# Lesson 03.07 — Row Echelon Form

> **Module 03:** Linear Systems and Geometric Maps · Lesson 7 of 35

---

## What you will be able to do after this lesson

- [ ] Identify the 3 criteria of Row Echelon Form (REF): leading entries move strictly right, zero rows at bottom.
- [ ] Extract pivot positions.

## Prerequisites

- 03.06 Elementary Row Operations.

---

## 1. The idea

A matrix is in **Row Echelon Form (REF)** if:
1. All zero rows are at the bottom.
2. The leading entry (pivot) of each non-zero row is strictly to the right of the leading entry above it.
3. All entries below a pivot are zero.

---

## 2. Worked example

Matrix $\begin{bmatrix} 2 & 1 & 4 \\ 0 & 3 & -1 \\ 0 & 0 & 5 \end{bmatrix}$ is in REF with pivots at $(0, 0), (1, 1), (2, 2)$.

---

## 3. Verify it in code

```python
import numpy as np
M = np.array([[2.0, 1.0, 4.0], [0.0, 3.0, -1.0], [0.0, 0.0, 5.0]])
# Check upper triangular structure (below diagonal entries are 0)
assert np.allclose(np.tril(M, -1), 0.0)
assert M[0, 0] != 0 and M[1, 1] != 0 and M[2, 2] != 0
```

---

## 4. The mistake people actually make

Confusing Row Echelon Form (REF) with Reduced Row Echelon Form (RREF). REF requires zeros only below pivots.

---

## Check yourself

1. Where must all-zero rows be located in REF?
2. Must pivots in REF equal 1?

<details>
<summary>Answers</summary>

1. At the very bottom of the matrix.
2. No; pivots can be any non-zero number in general REF.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](08_Reduced_Row_Echelon_Form.md)
