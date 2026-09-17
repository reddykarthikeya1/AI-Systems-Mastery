# Lesson 12.14 — Confidence Intervals

> **Module 12:** Statistical Estimation from Samples · Lesson 14 of 22

---

## What you will be able to do after this lesson

- [ ] Construct a (1 - alpha) frequentist confidence interval: x_bar +- z_(alpha/2) * (s / sqrt(n)).
- [ ] Verify 95% coverage probability via Monte Carlo simulation.

## Prerequisites

- 12.05 The Standard Error.

---

## 1. The idea

A **confidence interval** at level $1 - \alpha$ (e.g. 95%) is an interval $[\hat{\theta}_L, \hat{\theta}_U]$ constructed such that in 95% of repeated independent experiments, the computed interval will cover the true parameter $\theta$. For known variance: $\bar{x} \pm z_{\alpha/2}\frac{\sigma}{\sqrt{n}}$.

---

## 2. Worked example

Sample mean $\bar{x} = 50$, $\sigma = 10, n = 100$. For 95% CI, $z_{0.025} = 1.96$. $\text{Margin of error} = 1.96(10/\sqrt{100}) = 1.96$. Interval is $[48.04, 51.96]$.

---

## 3. Verify it in code

```python
import numpy as np
x_bar = 50.0
sigma = 10.0
n = 100
z = 1.96
margin = z * (sigma / np.sqrt(n))
ci = (x_bar - margin, x_bar + margin)
assert np.isclose(ci[0], 48.04)
assert np.isclose(ci[1], 51.96)
```

---

## 4. The mistake people actually make

Claiming there is a 95% probability that true theta lies inside this specific observed interval [48.04, 51.96]. (See Lesson 12.15).

---

## Check yourself

1. What z-critical value corresponds to a two-sided 95% confidence interval?
2. What determines the width of a confidence interval?

<details>
<summary>Answers</summary>

1. 1.96.
2. The confidence level (z), data variability (sigma), and sample size (1/sqrt(n)).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](15_What_a_Confidence_Interval_Does_Not_Mean.md)
