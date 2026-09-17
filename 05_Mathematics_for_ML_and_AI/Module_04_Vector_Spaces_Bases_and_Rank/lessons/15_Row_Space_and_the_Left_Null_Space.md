# Lesson 04.15 — Row Space and the Left Null Space

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 15 of 21

---

## What you will be able to do after this lesson

- [ ] Define row space row(A) = col(A^T) and left null space null(A^T).
- [ ] Verify dimensions of all 4 subspaces in NumPy.

## Prerequisites

- 04.13 Column Space and 04.14 Null Space.

---

## 1. The idea

The **row space** of $A$ is $\text{row}(A) = \text{col}(A^T) \subseteq \mathbb{R}^n$. The **left null space** is $\text{null}(A^T) = \{\mathbf{y} \in \mathbb{R}^m : \mathbf{y}^T A = \mathbf{0}^T\} \subseteq \mathbb{R}^m$.

---

## 2. Worked example

For $A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$, $\text{row}(A) = \text{span}([1, 2]^T)$. Left null space $\text{null}(A^T) = \text{span}([-2, 1]^T)$ because $[-2, 1]\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix} = [0, 0]$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0], [2.0, 4.0]])
y = np.array([-2.0, 1.0])
assert np.allclose(y @ A, [0.0, 0.0])
assert np.allclose(A.T @ y, [0.0, 0.0])
```

---

## 4. The mistake people actually make

Confusing left null space (subspace of R^m) with null space (subspace of R^n).

---

## Check yourself

1. What is row(A) identical to?
2. Why is null(A^T) called the left null space?

<details>
<summary>Answers</summary>

1. The column space of the transpose: col(A^T).
2. Because y^T multiplies A from the left: y^T A = 0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](16_Rank_of_a_Matrix.md)
