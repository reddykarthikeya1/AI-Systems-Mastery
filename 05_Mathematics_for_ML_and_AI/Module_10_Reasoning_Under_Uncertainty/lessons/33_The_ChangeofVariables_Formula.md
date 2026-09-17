# Lesson 10.33 — The Change-of-Variables Formula

> **Module 10:** Reasoning Under Uncertainty · Lesson 33 of 41

---

## What you will be able to do after this lesson

- [ ] State change-of-variables formula: f_Y(y) = f_X(g^(-1)(y)) |d/dy g^(-1)(y)|.
- [ ] Understand Normalizing Flows in modern generative AI.

## Prerequisites

- 10.32 Transformations of Random Variables.

---

## 1. The idea

For invertible monotonic map $y = g(x)$, the **change-of-variables formula** preserves probability mass:
$$f_Y(y) = f_X(g^{-1}(y)) \left| \frac{d}{dy} g^{-1}(y) \right| = f_X(x) \left| \frac{dg}{dx} \right|^{-1}$$
In multi-dimensions, this generalizes to multiplying by the absolute determinant of the Jacobian $|\det J_{g^{-1}}|$, the mathematical engine behind **Normalizing Flows**.

---

## 2. Worked example

Let $y = 3x + 2$. Inverse is $x = (y-2)/3$, derivative is $1/3$. So $f_Y(y) = \frac{1}{3}f_X(\frac{y-2}{3})$.

---

## 3. Verify it in code

```python
import numpy as np
# Linear scaling X ~ N(0, 1), Y = 3X
# PDF of Y at 0 should be (1 / (3 * sqrt(2 * pi)))
f_x_0 = 1.0 / np.sqrt(2.0 * np.pi)
f_y_0 = f_x_0 * (1.0 / 3.0)
assert np.isclose(f_y_0, 1.0 / (3.0 * np.sqrt(2.0 * np.pi)))
```

---

## 4. The mistake people actually make

Forgetting the absolute value on the Jacobian determinant, leading to negative probability densities.

---

## Check yourself

1. What term compensates for the stretching or compression of space in change-of-variables?
2. What deep generative model family relies directly on this formula?

<details>
<summary>Answers</summary>

1. The absolute value of the derivative |dx/dy| (or Jacobian determinant).
2. Normalizing Flows.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](34_Markovs_and_Chebyshevs_Inequalities.md)
