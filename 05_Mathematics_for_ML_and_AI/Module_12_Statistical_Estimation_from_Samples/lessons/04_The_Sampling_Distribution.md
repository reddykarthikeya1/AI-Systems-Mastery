# Lesson 12.04 — The Sampling Distribution

> **Module 12:** Statistical Estimation from Samples · Lesson 4 of 22

---

## What you will be able to do after this lesson

- [ ] Simulate the sampling distribution of a statistic via repeated sampling.
- [ ] Demonstrate Central Limit Theorem shape convergence.

## Prerequisites

- 12.01 Populations, Samples and Estimators.

---

## 1. The idea

The **sampling distribution** is the probability distribution of a statistic obtained from repeated independent samples of size $n$ from the population. By the CLT, the sampling distribution of the sample mean approaches normal $\mathcal{N}(\mu, \sigma^2/n)$ regardless of the population distribution.

---

## 2. Worked example

Sampling 10,000 means of size $n=30$ from a skewed Exponential distribution yields a nearly bell-shaped Gaussian histogram.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
means = [np.mean(np.random.exponential(scale=2.0, size=30)) for _ in range(1000)]
assert np.isclose(np.mean(means), 2.0, atol=0.1)
assert np.isclose(np.var(means), (2.0**2) / 30.0, atol=0.05)
```

---

## 4. The mistake people actually make

Confusing the sample distribution (histogram of the raw data) with the sampling distribution (distribution of a statistic).

---

## Check yourself

1. What distribution does the sampling distribution of the mean approach as sample size n grows?
2. What is the standard deviation of the sample mean called?

<details>
<summary>Answers</summary>

1. A normal distribution (Central Limit Theorem).
2. The standard error.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](05_The_Standard_Error.md)
