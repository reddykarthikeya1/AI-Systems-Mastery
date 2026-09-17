# Lesson 07.09 — Quadratic Forms and Their Matrices

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 9 of 12

---

## What you will be able to do after this lesson

- [ ] Represent quadratic polynomials as x^T A x with symmetric matrix A.
- [ ] Verify that skew-symmetric components contribute zero to the quadratic form.

## Prerequisites

- Matrix multiplication (Module 03).

---

## 1. The idea

A **quadratic form** is a scalar polynomial of degree 2: $q(\mathbf{x}) = \mathbf{x}^T A \mathbf{x} = \sum_{i,j} A_{ij} x_i x_j$. Any general square matrix can be split into symmetric and skew-symmetric parts: $A = A_{sym} + A_{skew}$. Because $\mathbf{x}^T A_{skew} \mathbf{x} = 0$, we can always assume $A$ is symmetric without loss of generality.

---

## 2. Worked example

Let $q(x_1, x_2) = 3 x_1^2 + 4 x_1 x_2 + 5 x_2^2$. The cross term $4 x_1 x_2$ splits evenly into $2 x_1 x_2 + 2 x_2 x_1$. The symmetric matrix is $A = \begin{bmatrix} 3 & 2 \\ 2 & 5 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np

# Non-symmetric matrix
A_non_sym = np.array([[3.0, 4.0], [0.0, 5.0]])
A_sym = 0.5 * (A_non_sym + A_non_sym.T)

x = np.array([2.0, -1.0])
q1 = x @ A_non_sym @ x
q2 = x @ A_sym @ x

assert np.isclose(q1, q2)
assert np.isclose(q1, 3.0*(4) + 4.0*(2)*(-1) + 5.0*(1))
```

---

## 4. The mistake people actually make

Trying to analyze positive definiteness of a non-symmetric matrix directly without symmetrizing it first.

---

## Check yourself

1. Why can any quadratic form be represented by a symmetric matrix?
2. What is x^T A x when A is skew-symmetric (A = -A^T)?

<details>
<summary>Answers</summary>

1. Because the skew-symmetric component vanishes identically: x^T A_skew x = 0.
2. It is always identically zero.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](10_Positive_Definiteness_and_Its_Tests.md)
