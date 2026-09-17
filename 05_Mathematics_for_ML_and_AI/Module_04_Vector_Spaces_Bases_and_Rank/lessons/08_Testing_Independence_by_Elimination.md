# Lesson 04.08 — Testing Independence by Elimination

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 8 of 21

---

## What you will be able to do after this lesson

- [ ] Use Gaussian elimination to identify pivot and free columns.
- [ ] Prove that columns with pivots are linearly independent.

## Prerequisites

- 04.07 Linear Independence and Row Echelon Form.

---

## 1. The idea

To test independence of $\{\mathbf{v}_1, \dots, \mathbf{v}_k\}$, form matrix $A = [\mathbf{v}_1 \dots \mathbf{v}_k]$ and reduce to Row Echelon Form (REF). Columns with pivots correspond to linearly independent vectors. Free columns indicate linear dependence.

---

## 2. Worked example

Matrix $A = \begin{bmatrix} 1 & 2 & 3 \\ 0 & 1 & 1 \\ 0 & 0 & 0 \end{bmatrix}$. Pivots are in columns 1 and 2. Column 3 is a free column ($v_3 = v_1 + v_2$). Columns 1 and 2 form the independent set.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([
    [1.0, 2.0, 3.0],
    [0.0, 1.0, 1.0],
    [1.0, 3.0, 4.0]
])
rank = np.linalg.matrix_rank(A)
assert rank == 2  # 2 independent columns, 1 redundant
assert np.isclose(np.linalg.det(A), 0.0)
```

---

## 4. The mistake people actually make

Picking pivot columns from the row-reduced echelon matrix rather than taking the corresponding original columns of A.

---

## Check yourself

1. What does a free column in row echelon form signify?
2. If an n x n matrix has rank n, are its columns independent?

<details>
<summary>Answers</summary>

1. That the corresponding column is a linear combination of previous pivot columns.
2. Yes, all n columns are linearly independent.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](09_Basis_of_a_Vector_Space.md)
