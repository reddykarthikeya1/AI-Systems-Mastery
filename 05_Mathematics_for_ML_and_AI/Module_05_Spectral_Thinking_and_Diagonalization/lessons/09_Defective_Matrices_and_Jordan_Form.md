# Lesson 05.09 — Defective Matrices and Jordan Form

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 9 of 13

---

## What you will be able to do after this lesson

- [ ] Characterize Jordan canonical form J = V^(-1) A V for defective matrices.
- [ ] Identify generalized eigenvectors.

## Prerequisites

- 05.05 Algebraic vs Geometric Multiplicity.

---

## 1. The idea

When a matrix lacks a full set of eigenvectors ($\text{GM} < \text{AM}$), it cannot be diagonalized. Instead, it can be decomposed into **Jordan Normal Form** $A = M J M^{-1}$, where $J$ consists of Jordan blocks with eigenvalues on the diagonal and 1s on the superdiagonal.

---

## 2. Worked example

The shear matrix $A = \begin{bmatrix} 2 & 1 \\ 0 & 2 \end{bmatrix}$ is already a Jordan block of size 2. Its only eigenvector direction is $[1, 0]^T$. The generalized eigenvector $\mathbf{v}_2$ satisfies $(A - 2I)\mathbf{v}_2 = \mathbf{v}_1$.

---

## 3. Verify it in code

```python
import numpy as np

J = np.array([[2.0, 1.0], [0.0, 2.0]])
v1 = np.array([1.0, 0.0])

# Verify v1 is eigenvector
assert np.allclose(J @ v1, 2.0 * v1)

# Generalized eigenvector v2
v2 = np.array([0.0, 1.0])
assert np.allclose((J - 2.0 * np.eye(2)) @ v2, v1)
```

---

## 4. The mistake people actually make

Assuming defective matrices are common in real machine learning data. Most noisy empirical data yields distinct eigenvalues, but defective structures arise in dynamical systems.

---

## Check yourself

1. What sits on the superdiagonal of a non-trivial Jordan block?
2. How many independent eigenvectors does a single k x k Jordan block possess?

<details>
<summary>Answers</summary>

1. Ones (1s).
2. Exactly one independent eigenvector.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](10_Complex_Eigenvalues_and_Rotation.md)
