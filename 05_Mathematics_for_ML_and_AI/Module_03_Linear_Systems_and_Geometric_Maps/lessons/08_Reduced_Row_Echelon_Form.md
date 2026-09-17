# Lesson 03.08 — Reduced Row Echelon Form

> **Module 03:** Linear Systems and Geometric Maps · Lesson 8 of 35

---

## What you will be able to do after this lesson

- [ ] Define RREF: all pivots equal 1 and are the only non-zero entries in their column.
- [ ] Prove RREF is unique for every matrix.

## Prerequisites

- 03.07 Row Echelon Form.

---

## 1. The idea

A matrix is in **Reduced Row Echelon Form (RREF)** if it is in REF, every pivot is 1, and every pivot is the *only* non-zero entry in its entire column. Unlike REF, the RREF of any matrix is mathematically unique.

---

## 2. Worked example

Matrix $\begin{bmatrix} 1 & 0 & 3 \\ 0 & 1 & -2 \\ 0 & 0 & 0 \end{bmatrix}$ is in RREF. Pivots are at $(0, 0)$ and $(1, 1)$ with 1s, and column 3 contains free variable weights.

---

## 3. Verify it in code

```python
import numpy as np
R = np.array([[1.0, 0.0, 3.0], [0.0, 1.0, -2.0], [0.0, 0.0, 0.0]])
assert np.isclose(R[0, 0], 1.0) and np.isclose(R[1, 1], 1.0)
assert np.isclose(R[0, 1], 0.0) and np.isclose(R[1, 0], 0.0)
```

---

## 4. The mistake people actually make

Believing a matrix can have multiple distinct RREFs. The RREF is strictly unique.

---

## Check yourself

1. What must every pivot equal in RREF?
2. Is RREF unique for a given matrix?

<details>
<summary>Answers</summary>

1. Exactly 1.
2. Yes, every matrix has exactly one unique RREF.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](09_Gaussian_Elimination_Step_by_Step.md)
