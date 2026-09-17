# Lesson 10.27 — The Log-Normal Distribution

> **Module 10:** Reasoning Under Uncertainty · Lesson 27 of 41

---

## What you will be able to do after this lesson

- [ ] Define Log-Normal: X ~ LogNormal iff log(X) ~ Normal.
- [ ] Model multiplicative growth and heavy-tailed positive quantities.

## Prerequisites

- 10.24 Normal Distribution.

---

## 1. The idea

A variable $X > 0$ is **Log-Normal** if its logarithm is normally distributed: $\log X \sim \mathcal{N}(\mu, \sigma^2)$. By the multiplicative CLT, products of many positive random variables converge to Log-Normal (incomes, stock prices, latency).

---

## 2. Worked example

If $\log X \sim \mathcal{N}(0, 1)$, median is $e^0 = 1.0$, but mean is $e^{0 + 1/2} = \sqrt{e} \approx 1.649$ (right-skewed).

---

## 3. Verify it in code

```python
import numpy as np
mu, sigma = 0.0, 1.0
theoretical_mean = np.exp(mu + (sigma**2) / 2.0)
assert np.isclose(theoretical_mean, np.exp(0.5))
```

---

## 4. The mistake people actually make

Taking arithmetic mean of log-normal data and assuming it represents the typical (median) user experience.

---

## Check yourself

1. If X is Log-Normal, what distribution does log(X) follow?
2. Why is network latency typically Log-Normal rather than Normal?

<details>
<summary>Answers</summary>

1. A Normal distribution.
2. Because latency compounds multiplicatively across routing hops and queue stages.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](28_The_Beta_Distribution.md)
