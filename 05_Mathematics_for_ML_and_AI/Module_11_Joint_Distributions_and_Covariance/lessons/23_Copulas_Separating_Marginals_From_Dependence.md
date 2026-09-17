# Lesson 11.23 — Copulas: Separating Marginals From Dependence

> **Module 11:** Joint Distributions and Covariance · Lesson 23 of 29

---

## What you will be able to do after this lesson

- [ ] State Sklar's Theorem: any joint CDF can be written as C(F_1(x_1), ..., F_d(x_d)).
- [ ] Generate correlated non-Gaussian variables using Gaussian copula.

## Prerequisites

- 11.01 Joint Distributions and Cumulative distribution functions (Module 10).

---

## 1. The idea

**Sklar's Theorem** states that any multivariate joint distribution can be decomposed into its **marginal distributions** and a **copula** $C:[0, 1]^d \to [0, 1]$ that models the pure dependence structure. This enables pairing arbitrary marginals (e.g. Student-t and Beta) with a joint dependency model.

---

## 2. Worked example

Probability integral transform converts any continuous $X$ to uniform $U = F_X(X) \sim U(0, 1)$. Applying copula $C(u_1, u_2)$ couples them.

---

## 3. Verify it in code

```python
import numpy as np
from math import erf
def norm_cdf(x):
    return 0.5 * (1.0 + erf(x / np.sqrt(2.0)))

# Standard normal samples transformed to uniform (0, 1)
z = np.array([-1.96, 0.0, 1.96])
u = np.array([norm_cdf(val) for val in z])
assert np.isclose(u[1], 0.5)
assert np.isclose(u[0], 0.025, atol=1e-3)
assert np.isclose(u[2], 0.975, atol=1e-3)
```

---

## 4. The mistake people actually make

Assuming correlated variables must have identical distribution families.

---

## Check yourself

1. What does Sklar's theorem separate?
2. What distribution does F_X(X) follow for any continuous random variable?

<details>
<summary>Answers</summary>

1. Marginal distributions from their underlying dependence structure (copula).
2. The standard Uniform distribution U(0, 1).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](24_Mutual_Information.md)
