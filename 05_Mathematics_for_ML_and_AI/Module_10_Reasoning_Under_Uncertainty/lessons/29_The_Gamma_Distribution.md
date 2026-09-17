# Lesson 10.29 — The Gamma Distribution

> **Module 10:** Reasoning Under Uncertainty · Lesson 29 of 41

---

## What you will be able to do after this lesson

- [ ] Define Gamma(alpha, beta) distribution over positive reals (0, inf).
- [ ] Model sum of alpha independent Exponential waiting times.

## Prerequisites

- 10.23 Exponential Distribution.

---

## 1. The idea

The **Gamma distribution** models waiting times for $\alpha$ independent Poisson events to occur: $f(x) \propto x^{\alpha - 1} e^{-\beta x}$ for $x > 0$. $\mathbb{E}[X] = \alpha / \beta$, $\text{Var}(X) = \alpha / \beta^2$. It serves as the conjugate prior for precision (inverse variance) of Gaussians.

---

## 2. Worked example

Waiting for 3 customer arrivals ($\alpha = 3$) at rate $\beta = 2$ per hour: expected waiting time is $3/2 = 1.5$ hours.

---

## 3. Verify it in code

```python
import numpy as np
alpha, beta = 3.0, 2.0
mean = alpha / beta
var = alpha / (beta**2)
assert np.isclose(mean, 1.5)
assert np.isclose(var, 0.75)
```

---

## 4. The mistake people actually make

Confusing rate parameterization beta with scale parameterization theta = 1/beta.

---

## Check yourself

1. What is Gamma(1, beta) identical to?
2. What is the support of the Gamma distribution?

<details>
<summary>Answers</summary>

1. The Exponential(beta) distribution.
2. All positive real numbers: (0, infinity).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](30_The_Categorical_and_Multinomial_Distributions.md)
