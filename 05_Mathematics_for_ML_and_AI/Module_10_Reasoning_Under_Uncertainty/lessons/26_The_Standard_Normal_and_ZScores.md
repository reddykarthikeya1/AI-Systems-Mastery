# Lesson 10.26 — The Standard Normal and Z-Scores

> **Module 10:** Reasoning Under Uncertainty · Lesson 26 of 41

---

## What you will be able to do after this lesson

- [ ] Standardize variables into Z-scores: Z = (X - mu) / sigma.
- [ ] Map between standard normal and arbitrary Gaussian coordinates.

## Prerequisites

- 10.24 Normal Distribution.

---

## 1. The idea

The **Standard Normal** $Z \sim \mathcal{N}(0, 1)$ has $\mu = 0$ and $\sigma = 1$. Any normal $X \sim \mathcal{N}(\mu, \sigma^2)$ is standardized via $Z = \frac{X - \mu}{\sigma}$. A Z-score expresses how many standard deviations an observation lies from the mean.

---

## 2. Worked example

Student scores 85 on exam with $\mu = 70, \sigma = 10$. $Z = (85 - 70)/10 = 1.5$ (1.5 standard deviations above class average).

---

## 3. Verify it in code

```python
import numpy as np
mu, sigma = 70.0, 10.0
x = 85.0
z = (x - mu) / sigma
assert np.isclose(z, 1.5)
# Reverse transformation
assert np.isclose(mu + z * sigma, x)
```

---

## 4. The mistake people actually make

Standardizing test sets using test-set mean and variance instead of training-set statistics (data leakage).

---

## Check yourself

1. What are the mean and standard deviation of a standard normal distribution?
2. What does a Z-score of -2.0 mean?

<details>
<summary>Answers</summary>

1. Mean = 0, Standard Deviation = 1.
2. The observation is exactly 2 standard deviations below the mean.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](27_The_LogNormal_Distribution.md)
