# Lesson 10.32 — Transformations of Random Variables

> **Module 10:** Reasoning Under Uncertainty · Lesson 32 of 41

---

## What you will be able to do after this lesson

- [ ] Derive distribution of Y = g(X) via CDF method F_Y(y) = P(g(X) <= y).
- [ ] Verify simulated histogram matching in NumPy.

## Prerequisites

- 10.14 Cumulative Distribution Function.

---

## 1. The idea

When applying function $Y = g(X)$ to random variable $X$, its distribution transforms. The standard CDF technique:
$$F_Y(y) = P(Y \le y) = P(g(X) \le y)$$
Differentiating with respect to $y$ gives the transformed PDF $f_Y(y) = F'_Y(y)$.

---

## 2. Worked example

Let $X \sim U(0, 1)$ and $Y = X^2$. $F_Y(y) = P(X^2 \le y) = P(X \le \sqrt{y}) = \sqrt{y}$. Density $f_Y(y) = \frac{d}{dy}\sqrt{y} = \frac{1}{2\sqrt{y}}$ for $y \in (0, 1)$.

---

## 3. Verify it in code

```python
import numpy as np
# For X ~ Uniform(0, 1) and Y = X^2, CDF F_Y(y) = sqrt(y)
# Anti-derivative: \int 1/(2*sqrt(y)) dy = sqrt(y)
# Integrating from 0.04 to 1.0 yields sqrt(1.0) - sqrt(0.04) = 0.8
y_grid = np.linspace(0.04, 1.0, 500)
dy = np.diff(y_grid)
midpoints = (y_grid[:-1] + y_grid[1:]) / 2.0
integral_approx = np.sum((1.0 / (2.0 * np.sqrt(midpoints))) * dy)
assert np.isclose(integral_approx, 0.8, atol=1e-3)
```

---

## 4. The mistake people actually make

Simply plugging g(x) into f_X(x) (i.e. f_Y(y) != f_X(g^(-1)(y))). The Jacobian derivative scaling factor is required!

---

## Check yourself

1. Why can't we simply substitute y into the PDF f_X?
2. What step converts F_Y(y) into the PDF f_Y(y)?

<details>
<summary>Answers</summary>

1. Because probability mass must be preserved across stretches and compressions of space.
2. Taking the first derivative: d/dy F_Y(y).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](33_The_ChangeofVariables_Formula.md)
