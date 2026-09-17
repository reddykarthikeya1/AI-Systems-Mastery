# Lesson 05.07 — Similar Matrices and Their Invariants

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 7 of 13

---

## What you will be able to do after this lesson

- [ ] Define similarity B = P^(-1) A P as change of basis.
- [ ] Demonstrate that similar matrices share trace, determinant, and eigenvalues.

## Prerequisites

- 05.06 Diagonalization.

---

## 1. The idea

Two matrices $A$ and $B$ are **similar** ($A \sim B$) if there exists an invertible $P$ such that $B = P^{-1}AP$. Similar matrices represent the same linear transformation under different coordinate bases. They share identical eigenvalues, trace, and determinant.

---

## 2. Worked example

Let $A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}$, $P = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, $P^{-1} = \begin{bmatrix} 1 & -1 \\ 0 & 1 \end{bmatrix}$. $B = P^{-1}AP = \begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$. $\text{tr}(A) = \text{tr}(B) = 5$, $\det(A) = \det(B) = 6$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[2.0, 1.0], [0.0, 3.0]])
P = np.array([[1.0, 1.0], [0.0, 1.0]])
B = np.linalg.inv(P) @ A @ P

assert np.isclose(np.trace(A), np.trace(B))
assert np.isclose(np.linalg.det(A), np.linalg.det(B))
assert np.allclose(np.sort(np.linalg.eigvals(A)), np.sort(np.linalg.eigvals(B)))
```

---

## 4. The mistake people actually make

Believing similar matrices have the same eigenvectors. Their eigenvalues match, but eigenvectors are transformed by P.

---

## Check yourself

1. Do similar matrices have the same eigenvectors?
2. What happens to the determinant under similarity transformation?

<details>
<summary>Answers</summary>

1. No, the eigenvectors are rotated/transformed by P.
2. The determinant is completely preserved: det(P^(-1) A P) = det(A).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](08_Matrix_Powers_via_Diagonalization.md)
