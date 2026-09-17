# Lesson 03.15 — Matrix Multiplication as Composition

> **Module 03:** Linear Systems and Geometric Maps · Lesson 15 of 35

---

## What you will be able to do after this lesson

- [ ] Interpret matrix multiplication C = A B as functional composition T_A(T_B(x)).
- [ ] Verify associative law (A B) C = A (B C).

## Prerequisites

- 03.14 Matrix Addition.

---

## 1. The idea

Matrix multiplication is defined so that multiplying by $AB$ corresponds to applying linear transformation $B$ followed by linear transformation $A$: $(A B)\mathbf{x} = A(B\mathbf{x})$. For $A \in \mathbb{R}^{m \times k}$ and $B \in \mathbb{R}^{k \times n}$, $C_{ij} = \sum_{p=1}^k A_{ip} B_{pj}$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}, B = \begin{bmatrix} 2 & 0 \\ 1 & 3 \end{bmatrix}$. $AB = \begin{bmatrix} 1(2)+2(1) & 1(0)+2(3) \\ 0(2)+1(1) & 0(0)+1(3) \end{bmatrix} = \begin{bmatrix} 4 & 6 \\ 1 & 3 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0], [0.0, 1.0]])
B = np.array([[2.0, 0.0], [1.0, 3.0]])
C = A @ B
assert np.allclose(C, [[4.0, 6.0], [1.0, 3.0]])
# Associativity
D = np.array([[1.0], [-1.0]])
assert np.allclose((A @ B) @ D, A @ (B @ D))
```

---

## 4. The mistake people actually make

Confusing matrix multiplication (@) with elementwise Hadamard multiplication (*).

---

## Check yourself

1. Why must the inner dimensions match for matrix multiplication A @ B?
2. Is matrix multiplication associative?

<details>
<summary>Answers</summary>

1. Because the output space of map B must match the input domain of map A.
2. Yes, (A B) C = A (B C).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](16_Why_Matrix_Multiplication_Is_Not_Commutative.md)
