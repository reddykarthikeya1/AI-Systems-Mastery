# Lesson 05.04 — Eigenspaces and Geometric Multiplicity

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 4 of 13

---

## What you will be able to do after this lesson

- [ ] Compute the eigenspace null(A - lambda I) by Gaussian elimination.
- [ ] Define geometric multiplicity as the dimension of the eigenspace.

## Prerequisites

- 05.02 Characteristic Polynomial and Null Space.

---

## 1. The idea

For an eigenvalue $\lambda$, the set of all eigenvectors along with $\mathbf{0}$ forms a subspace called the **eigenspace** $E_\lambda = \text{null}(A - \lambda I)$. The **geometric multiplicity** of $\lambda$ is $\dim(E_\lambda) = \text{nullity}(A - \lambda I)$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}$ with eigenvalue $\lambda = 2$. $A - 2I = \begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$. The null space is all of $\mathbb{R}^2$. The geometric multiplicity is 2.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[2.0, 0.0], [0.0, 2.0]])
lam = 2.0
M = A - lam * np.eye(2)
rank = np.linalg.matrix_rank(M)
geo_mult = A.shape[0] - rank
assert geo_mult == 2
assert rank == 0
```

---

## 4. The mistake people actually make

Confusing the number of eigenvectors (which is infinite) with the dimension of the eigenspace.

---

## Check yourself

1. Can the geometric multiplicity of an eigenvalue be zero?
2. What is the minimum geometric multiplicity for any valid eigenvalue?

<details>
<summary>Answers</summary>

1. No, by definition an eigenvalue must have at least one non-zero eigenvector.
2. The minimum geometric multiplicity is always 1.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](05_Algebraic_versus_Geometric_Multiplicity.md)
