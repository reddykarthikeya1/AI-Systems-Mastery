# Lesson 05.01 — Eigenvectors: Directions a Map Does Not Turn

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 1 of 13

---

## What you will be able to do after this lesson

- [ ] Define an eigenvector geometrically as a non-zero vector whose direction is invariant under matrix transformation.
- [ ] Compute whether a candidate vector is an eigenvector using A v = lambda v in NumPy.

## Prerequisites

- Matrix-vector multiplication (Module 03).

---

## 1. The idea

A linear transformation $A \in \mathbb{R}^{n \times n}$ typically rotates, stretches, and shears vectors. An **eigenvector** $\mathbf{v} \neq \mathbf{0}$ is a special direction where the transformation acts purely as a scalar stretch: $A\mathbf{v} = \lambda \mathbf{v}$. The scalar $\lambda$ is the corresponding **eigenvalue**.

---

## 2. Worked example

Let $A = \begin{bmatrix} 3 & 1 \\ 1 & 3 \end{bmatrix}$ and vector $\mathbf{v} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$. Then $A\mathbf{v} = \begin{bmatrix} 3(1)+1(1) \\ 1(1)+3(1) \end{bmatrix} = \begin{bmatrix} 4 \\ 4 \end{bmatrix} = 4 \begin{bmatrix} 1 \\ 1 \end{bmatrix}$. Thus $\mathbf{v}$ is an eigenvector with eigenvalue $\lambda = 4$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[3.0, 1.0], [1.0, 3.0]])
v = np.array([1.0, 1.0])
Av = A @ v

# Check proportionality
lambda_val = 4.0
assert np.allclose(Av, lambda_val * v)

# Orthogonal candidate v2 = [-1, 1]
v2 = np.array([-1.0, 1.0])
Av2 = A @ v2
assert np.allclose(Av2, 2.0 * v2)
```

---

## 4. The mistake people actually make

Considering the zero vector as an eigenvector. By definition, eigenvectors must be non-zero vectors so that eigenvalue relations are non-trivial.

---

## Check yourself

1. Can the zero vector be an eigenvector?
2. If A v = 0 for non-zero v, is v an eigenvector?

<details>
<summary>Answers</summary>

1. No, the zero vector is explicitly excluded by definition.
2. Yes, v is an eigenvector with eigenvalue lambda = 0 (meaning v lies in the null space of A).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Eigenvalues_and_the_Characteristic_Polynomial.md)
