# Lesson 12.01 — Populations, Samples and Estimators

> **Module 12:** Statistical Estimation from Samples · Lesson 1 of 22

---

## What you will be able to do after this lesson

- [ ] Distinguish fixed population parameter theta from random sample estimator theta_hat.
- [ ] Compute plug-in empirical sample estimates in NumPy.

## Prerequisites

- Random variables and expectation (Module 10).

---

## 1. The idea

The **population** is the full underlying data distribution with fixed true parameter $\theta$. A **sample** $\{x_1, \dots, x_n\}$ is a random draw of size $n$. An **estimator** $\hat{\theta}(X_1, \dots, X_n)$ is a function (statistic) of the sample. Because the sample is random, $\hat{\theta}$ is itself a random variable with its own distribution.

---

## 2. Worked example

For population mean $\mu = 10$, sample is $[8, 12, 11, 9]$. Sample mean is $\hat{\mu} = (8+12+11+9)/4 = 10.0$. Another sample might yield $9.5$.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
pop_mean = 10.0
sample = np.array([8.0, 12.0, 11.0, 9.0])
sample_mean = np.mean(sample)
assert np.isclose(sample_mean, pop_mean)
assert isinstance(sample_mean, float)
```

---

## 4. The mistake people actually make

Treating sample statistics as fixed constants rather than realizations of random variables.

---

## Check yourself

1. Is the true population parameter theta random?
2. Why does estimator theta_hat vary across samples?

<details>
<summary>Answers</summary>

1. No, in classical statistics theta is a fixed unknown constant.
2. Because each sample contains a different random subset of data.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Bias_Variance_and_Mean_Squared_Error.md)
