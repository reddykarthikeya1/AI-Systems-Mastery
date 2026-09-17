# Lesson 12.17 — Hypothesis Testing and the p-Value

> **Module 12:** Statistical Estimation from Samples · Lesson 17 of 22

---

## What you will be able to do after this lesson

- [ ] Define null hypothesis H_0 and test statistic Z = (x_bar - mu_0) / SE.
- [ ] Compute two-tailed p-value via normal CDF.

## Prerequisites

- 12.05 Standard Error.

---

## 1. The idea

In hypothesis testing, we formulate a null hypothesis $H_0: \theta = \theta_0$. The **p-value** is the probability of observing a test statistic at least as extreme as the one computed from data, *assuming $H_0$ is true*: $p = P(|Z| \ge |z_{obs}| \mid H_0)$. If $p < \alpha$, we reject $H_0$.

---

## 2. Worked example

Test $H_0: \mu = 0$ against $H_1: \mu \neq 0$. Observed $z = 2.0$. Tail probability $P(Z \ge 2.0) \approx 0.0228$. Two-tailed p-value is $2 \times 0.0228 = 0.0455 < 0.05$. Reject $H_0$.

---

## 3. Verify it in code

```python
import numpy as np
# Approximate normal CDF via error function: 0.5 * (1 + erf(x / sqrt(2)))
from math import erf
def norm_cdf(x):
    return 0.5 * (1.0 + erf(x / np.sqrt(2.0)))

z_obs = 2.0
p_val = 2.0 * (1.0 - norm_cdf(z_obs))
assert np.isclose(p_val, 0.0455, atol=1e-3)
assert p_val < 0.05
```

---

## 4. The mistake people actually make

Believing a small p-value measures effect size. With large n, a practically meaningless difference can have p < 0.001.

---

## Check yourself

1. What is the definition of a p-value?
2. Does p < 0.05 prove the null hypothesis is false?

<details>
<summary>Answers</summary>

1. The probability of observing data as or more extreme than observed, assuming H_0 is true.
2. No, it only indicates the observed data would be unlikely under H_0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](18_What_a_pValue_Does_Not_Mean.md)
