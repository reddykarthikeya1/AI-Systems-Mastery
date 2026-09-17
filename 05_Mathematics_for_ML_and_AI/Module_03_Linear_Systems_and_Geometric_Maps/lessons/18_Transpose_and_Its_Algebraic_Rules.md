# Lesson 03.18 — Transpose and Its Algebraic Rules

> **Module 03:** Linear Systems and Geometric Maps · Lesson 18 of 35

---

## What you will be able to do after this lesson

- [ ] Define matrix transpose (A^T)_{ij} = A_{ji}.
- [ ] Apply reversal rule (A B)^T = B^T A^T.

## Prerequisites

- 03.15 Matrix Multiplication.

---

## 1. The idea

The **transpose** $A^T$ swaps rows and columns: $(A^T)_{ij} = A_{ji}$. The crucial algebraic identity is the **reversal rule**: $(AB)^T = B^T A^T$. A matrix is **symmetric** if $A = A^T$, and **skew-symmetric** if $A = -A^T$.

---

## 2. Worked example

Let $A$ be $2 \times 3$ and $B$ be $3 \times 4$. $AB$ is $2 \times 4$, so $(AB)^T$ is $4 \times 2$. $B^T$ is $4 \times 3$ and $A^T$ is $3 \times 2$, so $B^T A^T$ is $4 \times 2$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[5.0, 6.0], [7.0, 8.0]])
assert np.allclose((A @ B).T, B.T @ A.T)
# Symmetric decomposition A = A_sym + A_skew
A_sym = 0.5 * (A + A.T)
A_skew = 0.5 * (A - A.T)
assert np.allclose(A_sym + A_skew, A)
assert np.allclose(A_sym, A_sym.T)
assert np.allclose(A_skew, -A_skew.T)
```

---

## 4. The mistake people actually make

Writing (A B)^T = A^T B^T, which causes dimension errors and algebraic falsehood.

---

## Check yourself

1. What is (A^T)^T?
2. What is (A B C)^T equal to?

<details>
<summary>Answers</summary>

1. A.
2. C^T B^T A^T (reversed order of transposes).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](19_Matrix_Inverse_Definition_and_Existence.md)
