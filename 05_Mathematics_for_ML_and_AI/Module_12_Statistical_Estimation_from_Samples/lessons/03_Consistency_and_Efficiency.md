# Lesson 12.03 — Consistency and Efficiency

> **Module 12:** Statistical Estimation from Samples · Lesson 3 of 22

---

## What you will be able to do after this lesson

- [ ] Define consistency as convergence in probability: theta_hat_n -> theta as n -> inf.
- [ ] Define efficiency as achieving the lowest possible variance among unbiased estimators.

## Prerequisites

- 12.02 Bias and Variance.

---

## 1. The idea

An estimator is **consistent** if it converges in probability to the true parameter as sample size grows: $\lim_{n \to \infty} P(|\hat{\theta}_n - \theta| > \epsilon) = 0$. An unbiased estimator is **efficient** if its variance attains the Cramér-Rao Lower Bound.

---

## 2. Worked example

For sample mean $\bar{X}_n$, $\text{Var}(\bar{X}_n) = \sigma^2 / n \to 0$ as $n \to \infty$. By Chebyshev's inequality, $\bar{X}_n$ is consistent for $\mu$.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
true_mu = 5.0
ns = [10, 100, 1000, 10000]
errors = [abs(np.mean(np.random.normal(true_mu, 1.0, n)) - true_mu) for n in ns]
assert errors[-1] < errors[0]
```

---

## 4. The mistake people actually make

Confusing unbiasedness (a finite-sample property) with consistency (an asymptotic property as n -> inf).

---

## Check yourself

1. Does consistency guarantee an estimator is unbiased for small samples?
2. What happens to the variance of a consistent estimator as n -> infinity?

<details>
<summary>Answers</summary>

1. No, an estimator can be biased for small n yet consistent asymptotically (e.g. 1/n sum (x - x_bar)^2).
2. It shrinks to zero.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](04_The_Sampling_Distribution.md)
