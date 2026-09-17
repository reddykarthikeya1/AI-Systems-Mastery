# Lesson 11.16 — The Bias-Variance Decomposition

> **Module 11:** Joint Distributions and Covariance · Lesson 16 of 29

---

## What you will be able to do after this lesson

- [ ] Derive expected test error E[(y - f_hat(x))^2] = Bias^2 + Variance + Irreducible Noise sigma^2.
- [ ] Diagnose overfitting and underfitting.

## Prerequisites

- 12.02 Bias and Variance.

---

## 1. The idea

For true relationship $y = f(x) + \epsilon$ with $\text{Var}(\epsilon) = \sigma^2$:
$$\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}(\hat{f}(x))^2 + \text{Var}(\hat{f}(x)) + \sigma^2$$
- **Underfitting**: high bias, low variance.
- **Overfitting**: low bias, high variance.
- **Irreducible Error** $\sigma^2$: fundamental limit set by noise in the data generator.

---

## 2. Worked example

A complex model has Bias $= 0.1$, Model Variance $= 0.4$, and data noise $\sigma^2 = 0.5$. Expected test error $= 0.1^2 + 0.4 + 0.5 = 0.01 + 0.4 + 0.5 = 0.91$.

---

## 3. Verify it in code

```python
import numpy as np
bias = 0.1
var = 0.4
noise = 0.5
expected_loss = bias**2 + var + noise
assert np.isclose(expected_loss, 0.91)
```

---

## 4. The mistake people actually make

Attempting to tune a model to zero test loss when irreducible noise sigma^2 > 0.

---

## Check yourself

1. Can test error ever drop below sigma^2?
2. What characterizes an overfitted model in terms of bias and variance?

<details>
<summary>Answers</summary>

1. No, sigma^2 is the irreducible lower bound on prediction error.
2. Very low training bias but high estimator variance across samples.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](17_The_Multivariate_Normal_Distribution.md)
