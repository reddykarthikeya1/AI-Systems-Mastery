# Lesson 05.05 — Algebraic versus Geometric Multiplicity

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 5 of 13

---

## What you will be able to do after this lesson

- [ ] Differentiate between algebraic multiplicity (root multiplicity) and geometric multiplicity.
- [ ] Identify non-diagonalizable matrices where geometric multiplicity is strictly less than algebraic.

## Prerequisites

- 05.04 Eigenspaces.

---

## 1. The idea

The **algebraic multiplicity** (AM) of $\lambda$ is its multiplicity as a root of $\det(A - \lambda I) = 0$. The **geometric multiplicity** (GM) is $\dim(\text{null}(A - \lambda I))$. It is always true that $1 \le \text{GM} \le \text{AM}$. When $\text{GM} < \text{AM}$, the matrix is defective and cannot be diagonalized.

---

## 2. Worked example

Let $J = \begin{bmatrix} 3 & 1 \\ 0 & 3 \end{bmatrix}$. Characteristic polynomial is $(3-\lambda)^2$, so $\lambda = 3$ has $\text{AM} = 2$. However, $J - 3I = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, which has rank 1, so nullity $\text{GM} = 2 - 1 = 1 < \text{AM}$.

---

## 3. Verify it in code

```python
import numpy as np

J = np.array([[3.0, 1.0], [0.0, 3.0]])
am = 2
gm = 2 - np.linalg.matrix_rank(J - 3.0 * np.eye(2))
assert am == 2
assert gm == 1
assert gm < am
```

---

## 4. The mistake people actually make

Assuming every matrix has n linearly independent eigenvectors. Defective shear matrices have fewer eigenvectors than dimensions.

---

## Check yourself

1. What inequality always connects geometric and algebraic multiplicity?
2. What is a matrix called when GM < AM for some eigenvalue?

<details>
<summary>Answers</summary>

1. 1 <= GM <= AM.
2. It is called a defective (or non-diagonalizable) matrix.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](06_Diagonalization_When_and_Why.md)
