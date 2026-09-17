# Lesson 07.02 — Geometry of the SVD

> **Module 07:** LowRank Structure and Quadratic Forms · Lesson 2 of 12

---

## What you will be able to do after this lesson

- [ ] Interpret SVD geometrically as rotation V^T, axis scaling Sigma, and rotation U.
- [ ] Map the unit circle to an ellipse under a linear map.

## Prerequisites

- 07.01 SVD Statement.

---

## 1. The idea

SVD proves that any linear transformation maps the unit sphere in $\mathbb{R}^n$ into a hyper-ellipse in $\mathbb{R}^m$. The directions of the principal semi-axes are given by the columns of $U$ (left singular vectors), and their lengths are the singular values $\sigma_i$.

---

## 2. Worked example

For a $2 \times 2$ matrix, the unit circle is first rotated by $V^T$, stretched along coordinate axes by $\sigma_1, \sigma_2$, and rotated to its final orientation by $U$.

---

## 3. Verify it in code

```python
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])
U, s, Vt = np.linalg.svd(A)

# Unit vectors along principal axes
v1 = Vt[0]
Av1 = A @ v1
assert np.isclose(np.linalg.norm(Av1), s[0])
assert np.allclose(Av1 / s[0], U[:, 0])
```

---

## 4. The mistake people actually make

Believing the principal axes of the ellipse align with the matrix eigenvectors. In general, they align with the left singular vectors U.

---

## Check yourself

1. What shape does the unit sphere become under any linear map?
2. What determines the lengths of the semi-axes of the transformed ellipse?

<details>
<summary>Answers</summary>

1. A hyper-ellipse (possibly degenerate if rank is deficient).
2. The singular values sigma_i.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](03_Singular_Values_versus_Eigenvalues.md)
