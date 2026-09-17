# Lesson 03.17 — The Identity Matrix

> **Module 03:** Linear Systems and Geometric Maps · Lesson 17 of 35

---

## What you will be able to do after this lesson

- [ ] Define identity matrix I_n with delta_ij Kronecker delta entries.
- [ ] Verify neutral element property I A = A I = A.

## Prerequisites

- 03.15 Matrix Multiplication.

---

## 1. The idea

The **identity matrix** $I_n \in \mathbb{R}^{n \times n}$ has 1s on the main diagonal and 0s elsewhere ($I_{ij} = \delta_{ij}$). It acts as the multiplicative identity: $A I_n = A$ and $I_m A = A$ for any $m \times n$ matrix $A$.

---

## 2. Worked example

For $\mathbf{x} = [3, -5]^T$: $I_2 \mathbf{x} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 3 \\ -5 \end{bmatrix} = \begin{bmatrix} 3 \\ -5 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
I = np.eye(3)
A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
assert np.allclose(I @ A, A)
assert np.allclose(A @ I, A)
```

---

## 4. The mistake people actually make

Assuming an identity matrix can be non-square. By definition, identity matrices are square.

---

## Check yourself

1. What are the diagonal entries of the identity matrix?
2. What is I^k for any integer power k?

<details>
<summary>Answers</summary>

1. All ones (1.0).
2. Always the identity matrix I.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](18_Transpose_and_Its_Algebraic_Rules.md)
