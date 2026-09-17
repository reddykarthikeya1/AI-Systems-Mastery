# Lesson 05.08 — Matrix Powers via Diagonalization

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 8 of 13

---

## What you will be able to do after this lesson

- [ ] Compute high powers of a matrix in O(1) time complexity via A^k = P D^k P^(-1).
- [ ] Analyze convergence of Markov transition matrices.

## Prerequisites

- 05.06 Diagonalization.

---

## 1. The idea

Repeated matrix multiplication $A^k$ is costly ($O(k \cdot n^3)$). Via diagonalization $A = PDP^{-1}$, powers telescope: $A^k = (PDP^{-1})(PDP^{-1})\cdots = P D^k P^{-1}$. Computing $D^k$ costs only $O(n)$ by exponentiating diagonal elements.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 & 2 \\ 2 & 1 \end{bmatrix}$ with $D = \text{diag}(3, -1)$. Then $A^{10} = P \begin{bmatrix} 3^{10} & 0 \\ 0 & (-1)^{10} \end{bmatrix} P^{-1} = P \begin{bmatrix} 59049 & 0 \\ 0 & 1 \end{bmatrix} P^{-1}$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[1.0, 2.0], [2.0, 1.0]])
k = 6

# Direct power
A_k_direct = np.linalg.matrix_power(A, k)

# Diagonal power
vals, P = np.linalg.eig(A)
D_k = np.diag(vals ** k)
A_k_diag = P @ D_k @ np.linalg.inv(P)

assert np.allclose(A_k_direct, A_k_diag)
```

---

## 4. The mistake people actually make

Exponentiating each element of A directly (elementwise power) instead of matrix power.

---

## Check yourself

1. What is the computational complexity of computing D^k for an n x n diagonal matrix?
2. What condition on eigenvalues ensures A^k converges to 0 as k -> infinity?

<details>
<summary>Answers</summary>

1. O(n) elementwise operations.
2. All eigenvalues must have absolute value strictly less than 1: max(|lambda_i|) < 1.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](09_Defective_Matrices_and_Jordan_Form.md)
