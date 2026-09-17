# Lesson 06.08 — The Projection Matrix and Its Properties

> **Module 06:** Orthogonality and Projections · Lesson 8 of 18

---

## What you will be able to do after this lesson

- [ ] Prove projection matrices are idempotent (P^2 = P) and symmetric (P^T = P).
- [ ] Identify eigenvalues of projection matrices (only 0 and 1).

## Prerequisites

- 06.07 Projection Onto a Subspace.

---

## 1. The idea

An orthogonal projection matrix $P = A(A^T A)^{-1}A^T$ satisfies two algebraic identities:
1. **Idempotence**: $P^2 = P$ (projecting twice gives the same point).
2. **Symmetry**: $P^T = P$ (orthogonality of the projection).
Its eigenvalues can only be 1 (for vectors in the subspace) or 0 (for vectors in the orthogonal complement). $\text{trace}(P) = \text{rank}(P) = \dim(V)$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$. $P = \frac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$. $P^2 = \frac{1}{4}\begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix} = P$. $P^T = P$. Trace $= 0.5 + 0.5 = 1 = \text{rank}(P)$.

---

## 3. Verify it in code

```python
import numpy as np
a = np.array([[1.0], [1.0]])
P = a @ np.linalg.inv(a.T @ a) @ a.T
assert np.allclose(P @ P, P)
assert np.allclose(P.T, P)
eigs = np.linalg.eigvalsh(P)
assert np.allclose(np.sort(eigs), [0.0, 1.0])
assert np.isclose(np.trace(P), 1.0)
```

---

## 4. The mistake people actually make

Confusing non-orthogonal oblique projections (P^2 = P but P != P^T) with orthogonal projections (P^2 = P and P = P^T).

---

## Check yourself

1. What are the only possible eigenvalues of a projection matrix?
2. What is the trace of a projection matrix equal to?

<details>
<summary>Answers</summary>

1. 0 and 1.
2. The rank of the projection matrix (dimension of the subspace).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](09_Least_Squares_as_Orthogonal_Projection.md)
