# Lesson 03.21 — Determinants of 2x2 and 3x3 Matrices

> **Module 03:** Linear Systems and Geometric Maps · Lesson 21 of 35

---

## What you will be able to do after this lesson

- [ ] Compute 2x2 determinant ad - bc and 3x3 determinant via cofactor expansion.
- [ ] Relate determinant to signed area and volume.

## Prerequisites

- 03.04 Matrices as Compact Notation.

---

## 1. The idea

The **determinant** $\det(A)$ is a scalar measuring the signed volume scaling factor of the transformation. For $2 \times 2$: $\det(A) = ad - bc$. For $3 \times 3$, cofactor expansion along row 1 gives $a(ei - fh) - b(di - fg) + c(dh - eg)$.

---

## 2. Worked example

$A = \begin{bmatrix} 3 & 1 \\ 2 & 4 \end{bmatrix}$. $\det(A) = 3(4) - 1(2) = 12 - 2 = 10$.

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[3.0, 1.0], [2.0, 4.0]])
assert np.isclose(np.linalg.det(A), 10.0)

A3 = np.array([[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [1.0, 0.0, 6.0]])
# det = 1*(24) - 2*(-5) + 3*(-4) = 24 + 10 - 12 = 22
assert np.isclose(np.linalg.det(A3), 22.0)
```

---

## 4. The mistake people actually make

Alternating signs (+ - +) incorrectly during 3x3 cofactor expansion.

---

## Check yourself

1. What is det(A) for a 2x2 matrix [[a, b], [c, d]]?
2. What does det(A) = 0 imply about the matrix?

<details>
<summary>Answers</summary>

1. ad - bc.
2. The matrix is singular (flattens space to zero volume) and has no inverse.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](22_Determinant_Properties_and_Row_Operations.md)
