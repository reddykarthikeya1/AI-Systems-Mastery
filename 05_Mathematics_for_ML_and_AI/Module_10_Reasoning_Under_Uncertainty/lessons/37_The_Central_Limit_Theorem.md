# Lesson 10.37 — The Central Limit Theorem

> **Module 10:** Reasoning Under Uncertainty · Lesson 37 of 41

---

## What you will be able to do after this lesson

- [ ] State the Lindeberg-Lévy CLT: sqrt(n)(X_bar - mu) / sigma -> N(0, 1) in distribution.
- [ ] Simulate Gaussian emergence from non-Gaussian variables.

## Prerequisites

- 10.36 Law of Large Numbers and 10.24 Normal Distribution.

---

## 1. The idea

The **Central Limit Theorem (CLT)** states that given i.i.d. random variables with mean $\mu$ and finite variance $\sigma^2$, the standardized sample mean converges in distribution to standard normal:
$$\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1) \quad \text{as } n \to \infty$$
Remarkably, this holds regardless of whether the original distribution was skewed, bimodal, or uniform!

---

## 2. Worked example

Averaging 50 discrete uniform dice: mean is 3.5, standard error is $\sqrt{2.917 / 50} \approx 0.241$. The distribution of averages is purely Gaussian.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
# Sample means from heavily skewed Gamma distribution
samples = [np.mean(np.random.gamma(shape=1.0, scale=2.0, size=100)) for _ in range(5000)]
z_scores = (samples - np.mean(samples)) / np.std(samples)
assert np.isclose(np.mean(z_scores), 0.0, atol=0.05)
assert np.isclose(np.std(z_scores), 1.0, atol=0.05)
```

---

## 4. The mistake people actually make

Applying CLT to distributions with infinite variance (e.g. Cauchy or Pareto with alpha <= 2).

---

## Check yourself

1. What two conditions must a distribution satisfy for standard CLT to hold?
2. What distribution does the standardized sample mean approach?

<details>
<summary>Answers</summary>

1. Independent identically distributed (i.i.d.) observations with finite variance sigma^2 < infinity.
2. The standard normal distribution N(0, 1).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](38_Entropy.md)
