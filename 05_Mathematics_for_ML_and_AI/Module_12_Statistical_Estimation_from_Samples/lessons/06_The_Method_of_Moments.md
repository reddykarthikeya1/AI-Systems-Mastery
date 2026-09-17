# Lesson 12.06 — The Method of Moments

> **Module 12:** Statistical Estimation from Samples · Lesson 6 of 22

---

## What you will be able to do after this lesson

- [ ] Equate theoretical population moments E[X^k] with sample moments 1/n sum x_i^k.
- [ ] Estimate Gamma and Uniform parameters via method of moments.

## Prerequisites

- 12.01 Populations, Samples and Estimators.

---

## 1. The idea

The **Method of Moments (MoM)** estimates parameters by setting sample moments $m_k = \frac{1}{n}\sum x_i^k$ equal to theoretical moments $\mu_k(\theta) = \mathbb{E}[X^k]$ and solving for $\theta$. It is simple and computationally fast, serving as a reliable initialization for iterative MLE.

---

## 2. Worked example

Uniform $U(0, b)$: theoretical mean is $b/2$. Setting $\bar{x} = b/2 \implies \hat{b}_{MoM} = 2\bar{x}$. For $\bar{x} = 3.5$, $\hat{b} = 7.0$.

---

## 3. Verify it in code

```python
import numpy as np
x = np.array([2.0, 4.0, 3.0, 5.0])
sample_mean = np.mean(x)
b_hat = 2.0 * sample_mean
assert np.isclose(b_hat, 7.0)
```

---

## 4. The mistake people actually make

Using method of moments estimates without verifying that parameters fall within valid distribution boundaries.

---

## Check yourself

1. How does Method of Moments derive parameter estimators?
2. What is a major advantage of Method of Moments?

<details>
<summary>Answers</summary>

1. By matching theoretical population moments with empirical sample moments.
2. It often yields simple closed-form algebraic solutions.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](07_Maximum_Likelihood_Estimation.md)
