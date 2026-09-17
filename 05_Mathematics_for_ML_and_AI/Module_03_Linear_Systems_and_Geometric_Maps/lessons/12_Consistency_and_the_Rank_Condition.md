# Lesson 03.12 — Consistency and the Rank Condition

> **Module 03:** Linear Systems and Geometric Maps · Lesson 12 of 35

---

## What you will be able to do after this lesson

- [ ] State the Rouché-Capelli Theorem: Ax = b is consistent iff rank(A) = rank([A | b]).
- [ ] Detect inconsistency via contradiction row [0 0 ... 0 | c] with c != 0.

## Prerequisites

- 03.05 Augmented Matrices and 03.11 Free Variables.

---

## 1. The idea

The **Rouché-Capelli Theorem** governs consistency:
- If $\text{rank}(A) < \text{rank}([A \mid \mathbf{b}])$, the system is **inconsistent** (no solution, contradiction $0 = c$).
- If $\text{rank}(A) = \text{rank}([A \mid \mathbf{b}]) = n$, the system has a **unique solution**.
- If $\text{rank}(A) = \text{rank}([A \mid \mathbf{b}]) < n$, the system has **infinitely many solutions**.

---

## 2. Worked example

System $x + y = 2$ and $x + y = 3$. $A = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$ has rank 1. Augmented $[A \mid \mathbf{b}] = \begin{bmatrix} 1 & 1 & 2 \\ 1 & 1 & 3 \end{bmatrix}$ reduces to $[0, 0 \mid 1]$, rank 2. Inconsistent.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 1.0], [1.0, 1.0]])
b = np.array([2.0, 3.0])
Ab = np.column_stack([A, b])
assert np.linalg.matrix_rank(A) == 1
assert np.linalg.matrix_rank(Ab) == 2
assert np.linalg.matrix_rank(A) < np.linalg.matrix_rank(Ab)
```

---

## 4. The mistake people actually make

Assuming parallel equations always have no solutions without checking if they are identical equations.

---

## Check yourself

1. What row appears in REF if a system is inconsistent?
2. What condition ensures a consistent system has infinitely many solutions?

<details>
<summary>Answers</summary>

1. A row of the form [0 0 ... 0 | c] where c != 0.
2. rank(A) == rank([A | b]) < n.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](13_Homogeneous_Systems_and_the_Null_Space.md)
