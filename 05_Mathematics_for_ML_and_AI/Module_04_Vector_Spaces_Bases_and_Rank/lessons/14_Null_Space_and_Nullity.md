# Lesson 04.14 — Null Space and Nullity

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 14 of 21

---

## What you will be able to do after this lesson

- [ ] Define null space null(A) = {x : Ax = 0} and nullity = dim(null(A)).
- [ ] Find a basis for the null space using SVD or elimination.

## Prerequisites

- 04.13 Column Space.

---

## 1. The idea

The **null space** (or kernel) of $A \in \mathbb{R}^{m \times n}$ is the set of all vectors that $A$ crushes to zero: $\text{null}(A) = \{\mathbf{x} \in \mathbb{R}^n : A\mathbf{x} = \mathbf{0}\}$. Its dimension is called the **nullity** of $A$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 2 \end{bmatrix}$ ($1 \times 2$ matrix). $x_1 + 2x_2 = 0 \implies x_1 = -2x_2$. Basis for $\text{null}(A)$ is $[-2, 1]^T$. Nullity is 1.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0]])
# Null space vector
v = np.array([-2.0, 1.0])
assert np.allclose(A @ v, [0.0])

# Nullity via SVD
U, s, Vt = np.linalg.svd(A)
nullity = A.shape[1] - len(s)
assert nullity == 1
```

---

## 4. The mistake people actually make

Thinking the null space is in R^m. Since x multiplies columns of A, null(A) is a subspace of R^n.

---

## Check yourself

1. In which space does null(A) live for an m x n matrix?
2. If null(A) contains only {0}, what does that say about the columns of A?

<details>
<summary>Answers</summary>

1. In R^n (the domain).
2. The columns of A are linearly independent.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](15_Row_Space_and_the_Left_Null_Space.md)
