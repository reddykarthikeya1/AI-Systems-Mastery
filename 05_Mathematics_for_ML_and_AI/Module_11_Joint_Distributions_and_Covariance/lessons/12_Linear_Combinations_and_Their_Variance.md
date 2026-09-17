# Lesson 11.12 — Linear Combinations and Their Variance

> **Module 11:** Joint Distributions and Covariance · Lesson 12 of 29

---

## What you will be able to do after this lesson

- [ ] Expand Var(a X + b Y) = a^2 Var(X) + b^2 Var(Y) + 2ab Cov(X, Y).
- [ ] Explain diversification in financial portfolio optimization.

## Prerequisites

- 11.06 Covariance.

---

## 1. The idea

When combining random variables, variances do not simply add unless variables are uncorrelated:
$$\text{Var}(aX + bY) = a^2 \text{Var}(X) + b^2 \text{Var}(Y) + 2ab\text{Cov}(X, Y)$$
If $\text{Cov}(X, Y) < 0$, negative covariance dampens overall variance, which is the mathematical foundation of risk diversification and ensembling.

---

## 2. Worked example

Let $\text{Var}(X) = 1, \text{Var}(Y) = 1, \text{Cov}(X, Y) = -0.5$. Variance of $0.5X + 0.5Y$ is $0.25(1) + 0.25(1) + 2(0.25)(-0.5) = 0.5 - 0.25 = 0.25$ (half the variance of each asset!).

---

## 3. Verify it in code

```python
import numpy as np
var_x, var_y = 1.0, 1.0
cov_xy = -0.5
a, b = 0.5, 0.5
var_comb = a**2 * var_x + b**2 * var_y + 2.0 * a * b * cov_xy
assert np.isclose(var_comb, 0.25)
```

---

## 4. The mistake people actually make

Dropping the cross-term 2ab Cov(X, Y) when computing the variance of correlated sums.

---

## Check yourself

1. When does Var(X + Y) = Var(X) + Var(Y)?
2. What happens to Var(X + Y) when X and Y have negative covariance?

<details>
<summary>Answers</summary>

1. When X and Y are uncorrelated: Cov(X, Y) = 0.
2. The total variance is strictly less than Var(X) + Var(Y).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](13_Conditional_Expectation.md)
