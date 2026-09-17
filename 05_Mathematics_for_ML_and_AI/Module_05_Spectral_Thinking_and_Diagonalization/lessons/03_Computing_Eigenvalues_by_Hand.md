# Lesson 05.03 — Computing Eigenvalues by Hand

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 3 of 13

---

## What you will be able to do after this lesson

- [ ] Compute eigenvalues for 2x2 and triangular matrices by hand using trace and determinant.
- [ ] Verify the trace and determinant eigenvalue identities.

## Prerequisites

- 05.02 Characteristic Polynomial.

---

## 1. The idea

For any $2 \times 2$ matrix $A$, the characteristic polynomial simplifies to $\lambda^2 - \text{tr}(A)\lambda + \det(A) = 0$. The sum of eigenvalues equals the trace, and the product of eigenvalues equals the determinant.

---

## 2. Worked example

For $A = \begin{bmatrix} 4 & 2 \\ 1 & 3 \end{bmatrix}$: $\text{tr}(A) = 4 + 3 = 7$, $\det(A) = 4(3) - 2(1) = 10$. $\lambda^2 - 7\lambda + 10 = (\lambda - 5)(\lambda - 2) = 0$. So $\lambda_1 = 5, \lambda_2 = 2$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[4.0, 2.0], [1.0, 3.0]])
trace_A = np.trace(A)
det_A = np.linalg.det(A)

eigs = np.linalg.eigvals(A)
assert np.isclose(trace_A, np.sum(eigs))
assert np.isclose(det_A, np.prod(eigs))
assert np.allclose(np.sort(eigs), [2.0, 5.0])
```

---

## 4. The mistake people actually make

Thinking eigenvalues of a sum equal the sum of eigenvalues. In general eig(A + B) != eig(A) + eig(B).

---

## Check yourself

1. How are the eigenvalues of a triangular matrix determined?
2. What is the relation between det(A) and its eigenvalues?

<details>
<summary>Answers</summary>

1. For triangular matrices, eigenvalues are simply the diagonal entries.
2. det(A) is equal to the product of all its eigenvalues.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](04_Eigenspaces_and_Geometric_Multiplicity.md)
