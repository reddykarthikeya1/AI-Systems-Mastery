# Lesson 10.36 — The Law of Large Numbers

> **Module 10:** Reasoning Under Uncertainty · Lesson 36 of 41

---

## What you will be able to do after this lesson

- [ ] Distinguish Weak Law (convergence in probability) from Strong Law (almost sure convergence).
- [ ] Verify convergence of sample mean to population mean in NumPy.

## Prerequisites

- 10.34 Chebyshev's Inequality.

---

## 1. The idea

The **Law of Large Numbers (LLN)** guarantees that the sample mean $\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$ converges to the true population mean $\mu$:
- **Weak Law (WLLN)**: $\lim_{n \to \infty} P(|\bar{X}_n - \mu| > \epsilon) = 0$ (proved by Chebyshev).
- **Strong Law (SLLN)**: $P(\lim_{n \to \infty} \bar{X}_n = \mu) = 1$ (almost sure convergence).

---

## 2. Worked example

Flipping a coin: as $n \to \infty$, the fraction of heads converges almost surely to $0.5$.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
flips = np.random.binomial(1, 0.5, 100000)
running_mean = np.cumsum(flips) / np.arange(1, 100001)
assert np.isclose(running_mean[-1], 0.5, atol=1e-3)
```

---

## 4. The mistake people actually make

Thinking the Law of Large Numbers balances past luck (e.g. 5 heads in a row will be balanced by 5 tails). The law dilutes deviations; it does not compensate.

---

## Check yourself

1. What type of convergence is guaranteed by the Weak Law of Large Numbers?
2. Does the LLN predict future coin flips will compensate for past streaks?

<details>
<summary>Answers</summary>

1. Convergence in probability.
2. No, it dilutes deviations by increasing n, never compensating.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](37_The_Central_Limit_Theorem.md)
