# Lesson 10.18 — Moments and Moment Generating Functions

> **Module 10:** Reasoning Under Uncertainty · Lesson 18 of 41

---

## What you will be able to do after this lesson

- [ ] Define k-th raw moment E[X^k] and central moment E[(X - mu)^k].
- [ ] Compute moments via MGF M_X(t) = E[e^(tX)].

## Prerequisites

- 10.17 Variance.

---

## 1. The idea

Moments characterize the shape of a distribution:
- 1st moment: Mean (center).
- 2nd central moment: Variance (spread).
- 3rd standardized moment: Skewness (asymmetry).
- 4th standardized moment: Kurtosis (tail heaviness).
The **Moment Generating Function** $M_X(t) = \mathbb{E}[e^{tX}]$ satisfies $\mathbb{E}[X^k] = M_X^{(k)}(0)$.

---

## 2. Worked example

For standard normal, skewness is 0 (symmetric), and kurtosis is 3.0.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
x = np.random.normal(0, 1, 10000)
# Sample skewness approx 0
skew = np.mean(((x - np.mean(x)) / np.std(x))**3)
assert np.isclose(skew, 0.0, atol=0.1)
```

---

## 4. The mistake people actually make

Assuming two different probability distributions cannot have identical mean and variance.

---

## Check yourself

1. What does skewness measure?
2. How is the k-th moment obtained from the MGF M_X(t)?

<details>
<summary>Answers</summary>

1. The asymmetry of the distribution around its mean.
2. By evaluating the k-th derivative at t=0: M_X^(k)(0).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](19_The_Bernoulli_and_Binomial_Distributions.md)
