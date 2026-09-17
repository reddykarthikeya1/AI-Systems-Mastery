# Lesson 06.16 — Orthogonal Bases for Function Spaces

> **Module 06:** Orthogonality and Projections · Lesson 16 of 18

---

## What you will be able to do after this lesson

- [ ] Generalize inner products to continuous functions <f, g> = integral f(x) g(x) dx.
- [ ] Represent Fourier basis functions as orthogonal vectors in function space.

## Prerequisites

- 06.01 The Dot Product.

---

## 1. The idea

In continuous function space $L^2$, the inner product is $\langle f, g \rangle = \int_a^b f(x)g(x)dx$. The Fourier basis functions $\{\sin(nx), \cos(nx)\}$ are mutually orthogonal under this inner product, decomposing functions into frequency coefficients exactly as vectors decompose onto coordinate axes.

---

## 2. Worked example

Consider $f(x) = \sin(x)$ and $g(x) = \cos(x)$ over $[-\pi, \pi]$. $\int_{-\pi}^\pi \sin(x)\cos(x)dx = \frac{1}{2}\int \sin(2x)dx = 0$. They are orthogonal functions.

---

## 3. Verify it in code

```python
import numpy as np
# Numerical integration approximation over [-pi, pi]
x = np.linspace(-np.pi, np.pi, 1000)
dx = x[1] - x[0]
f = np.sin(x)
g = np.cos(x)
inner_prod = np.sum(f * g) * dx
assert np.isclose(inner_prod, 0.0, atol=1e-4)
```

---

## 4. The mistake people actually make

Assuming inner products only apply to discrete finite vectors.

---

## Check yourself

1. How is the inner product of two continuous functions f and g defined?
2. Are sin(x) and cos(x) orthogonal on [-pi, pi]?

<details>
<summary>Answers</summary>

1. As the definite integral of their pointwise product: integral f(x) g(x) dx.
2. Yes, their integral product is zero.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](17_Whitening_and_Decorrelation.md)
