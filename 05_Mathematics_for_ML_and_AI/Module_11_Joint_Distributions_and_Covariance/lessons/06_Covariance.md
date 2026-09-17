# Lesson 11.06 — Covariance

> **Module 11:** Joint Distributions and Covariance · Lesson 6 of 29

---

## What you will be able to do after this lesson

- [ ] Compute Cov(X, Y) = E[(X - mu_X)(Y - mu_Y)] = E[XY] - E[X]E[Y].
- [ ] Verify Cov(X, X) = Var(X).

## Prerequisites

- Expectation and variance (Module 10).

---

## 1. The idea

**Covariance** measures linear co-dependence: $\text{Cov}(X, Y) = \mathbb{E}[(X - \mu_X)(Y - \mu_Y)] = \mathbb{E}[XY] - \mathbb{E}[X]\mathbb{E}[Y]$. Positive covariance means above-average values of $X$ tend to co-occur with above-average values of $Y$.

---

## 2. Worked example

Let $X = [1, 2, 3]$ and $Y = [2, 4, 6]$ ($Y = 2X$). $\mu_X = 2, \mu_Y = 4$. Centered: $[-1, 0, 1]$ and $[-2, 0, 2]$. Covariance is $\frac{1}{2}((-1)(-2) + 0 + (1)(2)) = 4/2 = 2.0$. $\text{Var}(X) = 1.0$, so $\text{Cov}(X, 2X) = 2 \text{Var}(X) = 2.0$.

---

## 3. Verify it in code

```python
import numpy as np
x = np.array([1.0, 2.0, 3.0])
y = np.array([2.0, 4.0, 6.0])
cov_xy = np.cov(x, y, ddof=1)[0, 1]
var_x = np.var(x, ddof=1)
assert np.isclose(cov_xy, 2.0 * var_x)
assert np.isclose(cov_xy, 2.0)
```

---

## 4. The mistake people actually make

Using raw magnitude of covariance to compare strength of relationships across variables with different units.

---

## Check yourself

1. What is Cov(X, X) equal to?
2. If X and Y are independent, what is their covariance?

<details>
<summary>Answers</summary>

1. Var(X).
2. Zero: Cov(X, Y) = 0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](07_Correlation_and_Its_Limits.md)
