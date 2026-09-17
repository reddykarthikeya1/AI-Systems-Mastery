# Lesson 12.21 — The Bootstrap

> **Module 12:** Statistical Estimation from Samples · Lesson 21 of 22

---

## What you will be able to do after this lesson

- [ ] Perform non-parametric bootstrap resampling with replacement.
- [ ] Compute standard errors and confidence intervals for arbitrary complex statistics.

## Prerequisites

- 12.04 Sampling Distribution.

---

## 1. The idea

The **Bootstrap** (Efron, 1979) estimates sampling distributions without assuming normality or analytical formulas. Treating the empirical sample as a proxy population, it repeatedly draws samples of size $n$ **with replacement**, computes the statistic $\hat{\theta}^{*b}$, and uses the empirical distribution of $\hat{\theta}^*$ for standard error and percentiles.

---

## 2. Worked example

For 5 data points, sample with replacement: e.g. $[x_1, x_1, x_3, x_4, x_4]$. Repeat 1,000 times to obtain the bootstrap distribution of the median.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
data = np.array([12.0, 15.0, 14.0, 19.0, 22.0, 105.0]) # Outlier present
B = 1000
boot_medians = [np.median(np.random.choice(data, size=len(data), replace=True)) for _ in range(B)]

se_median = np.std(boot_medians)
ci_95 = (np.percentile(boot_medians, 2.5), np.percentile(boot_medians, 97.5))
assert ci_95[0] < np.median(data) < ci_95[1]
assert se_median > 0
```

---

## 4. The mistake people actually make

Resampling without replacement. Sampling without replacement just shuffles the original sample, yielding identical statistics every time.

---

## Check yourself

1. Must bootstrap resampling be performed with or without replacement?
2. What is a key advantage of the bootstrap?

<details>
<summary>Answers</summary>

1. With replacement.
2. It computes valid standard errors and confidence intervals for complex statistics without parametric distribution assumptions.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](22_Module_Project_Estimate_Interval_and_Test_All_From_Scratch.md)
