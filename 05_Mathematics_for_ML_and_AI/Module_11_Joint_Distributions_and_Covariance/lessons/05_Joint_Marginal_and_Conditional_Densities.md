# Lesson 11.05 — Joint, Marginal and Conditional Densities

> **Module 11:** Joint Distributions and Covariance · Lesson 5 of 29

---

## What you will be able to do after this lesson

- [ ] Extend joint probability to continuous random variables via 2D integrals.
- [ ] Verify f_X(x) = integral f_{X,Y}(x, y) dy in NumPy.

## Prerequisites

- 11.01 Joint Distributions.

---

## 1. The idea

For continuous variables, the joint PDF $f_{X,Y}(x, y) \ge 0$ satisfies $\int_{-\infty}^\infty \int_{-\infty}^\infty f_{X,Y}(x, y) dx dy = 1$. Probabilities are 2D volume integrals. Marginals are 1D integrals: $f_X(x) = \int_{-\infty}^\infty f_{X,Y}(x, y) dy$.

---

## 2. Worked example

Uniform on unit square $[0, 1] \times [0, 1]$: $f(x, y) = 1$. Marginal $f_X(x) = \int_0^1 1 dy = 1$. Probability $P(X < 0.5, Y < 0.5) = 0.5 \times 0.5 = 0.25$.

---

## 3. Verify it in code

```python
import numpy as np
# Numerical 2D integration of bivariate standard normal
grid = np.linspace(-3, 3, 100)
dx = dy = grid[1] - grid[0]
X, Y = np.meshgrid(grid, grid)
pdf = (1.0 / (2.0 * np.pi)) * np.exp(-0.5 * (X**2 + Y**2))
total_vol = np.sum(pdf) * dx * dy
assert np.isclose(total_vol, 1.0, atol=1e-2)
```

---

## 4. The mistake people actually make

Thinking probability density f(x, y) cannot exceed 1. Densities can be > 1 as long as their total integral equals 1.

---

## Check yourself

1. Can a continuous probability density function exceed 1.0?
2. What does the double integral of a joint PDF over R^2 equal?

<details>
<summary>Answers</summary>

1. Yes, density values can be arbitrarily large as long as integrals evaluate to probabilities <= 1.
2. Exactly 1.0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](06_Covariance.md)
