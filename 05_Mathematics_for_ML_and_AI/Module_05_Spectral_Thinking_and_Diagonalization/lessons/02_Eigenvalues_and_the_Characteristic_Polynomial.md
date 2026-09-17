# Lesson 05.02 — Eigenvalues and the Characteristic Polynomial

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 2 of 13

---

## What you will be able to do after this lesson

- [ ] Formulate the characteristic equation det(A - lambda I) = 0.
- [ ] Find eigenvalues by solving the roots of the characteristic polynomial in NumPy.

## Prerequisites

- 05.01 Eigenvectors and Determinants (Module 03).

---

## 1. The idea

The relation $A\mathbf{v} = \lambda \mathbf{v}$ can be rewritten as $(A - \lambda I)\mathbf{v} = \mathbf{0}$. For non-trivial solutions $\mathbf{v} \neq \mathbf{0}$ to exist, the matrix $(A - \lambda I)$ must have a non-trivial null space, which means its determinant must be zero: $p(\lambda) = \det(A - \lambda I) = 0$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$. $\det(A - \lambda I) = (2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = (\lambda - 3)(\lambda - 1) = 0$. The eigenvalues are $\lambda_1 = 3, \lambda_2 = 1$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])
w, v = np.linalg.eig(A)
assert np.allclose(np.sort(w), [1.0, 3.0])

# Verify det(A - lambda I) == 0
for lam in [1.0, 3.0]:
    assert np.isclose(np.linalg.det(A - lam * np.eye(2)), 0.0)
```

---

## 4. The mistake people actually make

Attempting to compute eigenvalues by directly factoring non-square matrices. Eigenvalues are strictly defined for square matrices.

---

## Check yourself

1. What is the degree of the characteristic polynomial for an n x n matrix?
2. Can an n x n real matrix have complex eigenvalues?

<details>
<summary>Answers</summary>

1. The degree is always n.
2. Yes, if the roots of det(A - lambda I) = 0 are complex conjugate pairs.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](03_Computing_Eigenvalues_by_Hand.md)
