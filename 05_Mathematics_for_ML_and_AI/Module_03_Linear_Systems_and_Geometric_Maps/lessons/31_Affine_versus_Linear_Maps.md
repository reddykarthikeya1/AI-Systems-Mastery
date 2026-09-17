# Lesson 03.31 — Affine versus Linear Maps

> **Module 03:** Linear Systems and Geometric Maps · Lesson 31 of 35

---

## What you will be able to do after this lesson

- [ ] Distinguish linear maps f(x) = A x from affine maps f(x) = A x + b.
- [ ] Explain why affine maps preserve collinearity and parallelism but move the origin.

## Prerequisites

- 03.28 Linear Maps as Geometric Transformations.

---

## 1. The idea

An **affine map** $f(\mathbf{x}) = A\mathbf{x} + \mathbf{b}$ is a linear map followed by a translation vector $\mathbf{b}$. Affine maps preserve straight lines and ratios of distances along lines, but do not satisfy $f(\mathbf{0}) = \mathbf{0}$ or $f(\mathbf{u} + \mathbf{v}) = f(\mathbf{u}) + f(\mathbf{v})$ when $\mathbf{b} \neq \mathbf{0}$.

---

## 2. Worked example

Let $A = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}, \mathbf{b} = [1, 3]^T$. For $\mathbf{x} = [0, 0]^T$, $f(\mathbf{0}) = [1, 3]^T \neq \mathbf{0}$.

---

## 3. Verify it in code

```python
import numpy as np
A = 2.0 * np.eye(2)
b = np.array([1.0, 3.0])
f = lambda x: A @ x + b

assert np.allclose(f(np.zeros(2)), b)
u = np.array([1.0, 0.0])
v = np.array([0.0, 1.0])
# Non-linearity when b != 0
assert not np.allclose(f(u + v), f(u) + f(v))
```

---

## 4. The mistake people actually make

Calling neural network layers 'linear layers' without noting they are affine maps because they include bias vectors b.

---

## Check yourself

1. Is f(x) = 3 x + 5 a linear function in the linear algebra sense?
2. What geometric property do affine transformations preserve?

<details>
<summary>Answers</summary>

1. No, it is an affine function (does not map 0 to 0).
2. Collinearity (straight lines remain straight lines) and parallelism.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](32_Homogeneous_Coordinates.md)
