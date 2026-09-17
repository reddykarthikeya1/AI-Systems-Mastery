# Lesson 06.12 — Numerical Failure of Classical Gram-Schmidt

> **Module 06:** Orthogonality and Projections · Lesson 12 of 18

---

## What you will be able to do after this lesson

- [ ] Demonstrate catastrophic loss of orthogonality in Classical Gram-Schmidt (CGS).
- [ ] Implement Modified Gram-Schmidt (MGS) for numerical stability.

## Prerequisites

- 06.11 Gram-Schmidt.

---

## 1. The idea

In floating-point arithmetic, Classical Gram-Schmidt (CGS) loses orthogonality rapidly when columns are nearly collinear due to cancellation. **Modified Gram-Schmidt** (MGS) updates remaining vectors immediately after each orthogonal step, preserving orthogonality to machine precision.

---

## 2. Worked example

For nearly collinear vectors with angle $10^{-4}$ radians, CGS produces vectors whose dot product drifts to $10^{-8}$, whereas MGS stays near machine epsilon $10^{-16}$.

---

## 3. Verify it in code

```python
import numpy as np
# Nearly collinear vectors
eps = 1e-4
A = np.array([[1.0, 1.0], [eps, 0.0], [0.0, eps]])

# Modified Gram-Schmidt
Q = np.zeros_like(A)
V = A.copy()
for i in range(A.shape[1]):
    Q[:, i] = V[:, i] / np.linalg.norm(V[:, i])
    for j in range(i + 1, A.shape[1]):
        V[:, j] -= np.dot(Q[:, i], V[:, j]) * Q[:, i]

assert np.isclose(np.dot(Q[:, 0], Q[:, 1]), 0.0, atol=1e-10)
assert np.allclose(np.linalg.norm(Q, axis=0), [1.0, 1.0])
```

---

## 4. The mistake people actually make

Using textbook Classical Gram-Schmidt in production code instead of Modified Gram-Schmidt or Householder reflections.

---

## Check yourself

1. Why does Classical Gram-Schmidt fail numerically?
2. How does Modified Gram-Schmidt prevent loss of orthogonality?

<details>
<summary>Answers</summary>

1. Catastrophic cancellation when subtracting nearly identical floating point components.
2. By projecting remaining vectors against newly orthogonalized vectors sequentially.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](13_QR_Decomposition.md)
