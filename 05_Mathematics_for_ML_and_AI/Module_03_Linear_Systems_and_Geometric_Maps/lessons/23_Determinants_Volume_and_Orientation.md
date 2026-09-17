# Lesson 03.23 — Determinants: Volume and Orientation

> **Module 03:** Linear Systems and Geometric Maps · Lesson 23 of 35

---

## What you will be able to do after this lesson

- [ ] Interpret |det(A)| as the volume distortion factor under linear transformation.
- [ ] Interpret sign of det(A) as preservation (+1) or reversal (-1) of orientation.

## Prerequisites

- 03.21 Determinants.

---

## 1. The idea

Geometrically, $|\det(A)|$ represents the ratio of transformed volume to original volume for any region in $\mathbb{R}^n$. The sign indicates **orientation**: positive preserves chirality (right-handed systems stay right-handed), while negative indicates a reflection occurred.

---

## 2. Worked example

Reflection matrix $R = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ has $\det(R) = -1$. Volume is preserved ($|-1| = 1$), but orientation is flipped.

---

## 3. Verify it in code

```python
import numpy as np
R = np.array([[1.0, 0.0], [0.0, -1.0]])
assert np.isclose(np.linalg.det(R), -1.0)
assert np.isclose(abs(np.linalg.det(R)), 1.0)
```

---

## 4. The mistake people actually make

Assuming negative determinant means the matrix shrinks volume. The absolute value determines volume change; the sign determines orientation.

---

## Check yourself

1. What happens to the volume of a cube when transformed by matrix A?
2. What does a negative determinant indicate?

<details>
<summary>Answers</summary>

1. It is multiplied by |det(A)|.
2. The orientation of space has been flipped (reflection).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](24_Cramers_Rule_and_Why_It_Is_Impractical.md)
