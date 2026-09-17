# Lesson 05.10 — Complex Eigenvalues and Rotation

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 10 of 13

---

## What you will be able to do after this lesson

- [ ] Interpret complex eigenvalues a +- bi geometrically as rotation and scaling.
- [ ] Extract the angle of rotation theta = atan2(b, a).

## Prerequisites

- 05.02 Characteristic Polynomial.

---

## 1. The idea

A real matrix can have complex conjugate eigenvalues $\lambda = a \pm bi = r e^{\pm i \theta}$. Geometrically, such transformations cannot leave any 1D real subspace unrotated; they represent a combination of 2D rotation by angle $\theta$ and radial scaling by magnitude $r = \sqrt{a^2 + b^2}$.

---

## 2. Worked example

Let $R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$. Characteristic equation is $\lambda^2 + 1 = 0 \implies \lambda = \pm i$. Here $a = 0, b = 1$. The scale factor is $r = 1$ and angle $\theta = \pi/2$ (90 degree counter-clockwise rotation).

---

## 3. Verify it in code

```python
import numpy as np

R = np.array([[0.0, -1.0], [1.0, 0.0]])
vals = np.linalg.eigvals(R)

# Verify eigenvalues are +/- 1j
assert np.allclose(np.abs(vals), [1.0, 1.0])
assert np.isclose(vals[0].real, 0.0)
assert np.isclose(abs(vals[0].imag), 1.0)
```

---

## 4. The mistake people actually make

Discarding complex eigenvalues as invalid bugs when training recurrent networks. Complex eigenvalues govern oscillations.

---

## Check yourself

1. What physical geometric motion does a complex eigenvalue pair correspond to?
2. What is the spectral radius of a pure 2D rotation matrix?

<details>
<summary>Answers</summary>

1. A combination of rotation in a 2D plane and scaling.
2. The spectral radius is exactly 1.0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](11_The_Spectral_Theorem_for_Symmetric_Matrices.md)
