# Lesson 12.09 — MLE for the Normal and Bernoulli

> **Module 12:** Statistical Estimation from Samples · Lesson 9 of 22

---

## What you will be able to do after this lesson

- [ ] Derive closed-form MLE for Normal distribution: mu_hat = x_bar and sigma_hat^2 = 1/n sum (x_i - x_bar)^2.
- [ ] Identify the 1/n vs 1/(n-1) variance bias.

## Prerequisites

- 12.08 Log-Likelihood.

---

## 1. The idea

Setting $\frac{\partial \ell}{\partial \mu} = 0$ yields $\hat{\mu} = \frac{1}{n}\sum x_i$ (unbiased). Setting $\frac{\partial \ell}{\partial \sigma^2} = 0$ yields $\hat{\sigma}^2_{MLE} = \frac{1}{n}\sum (x_i - \bar{x})^2$. Notice $\mathbb{E}[\hat{\sigma}^2_{MLE}] = \frac{n-1}{n}\sigma^2$, so the MLE of variance is biased downwards (underestimates variance).

---

## 2. Worked example

For sample $[2, 4]$, $\bar{x} = 3$. $\hat{\sigma}^2_{MLE} = ((2-3)^2 + (4-3)^2)/2 = 1.0$. Unbiased sample variance with Bessel correction is $2.0/(2-1) = 2.0$.

---

## 3. Verify it in code

```python
import numpy as np
x = np.array([2.0, 4.0])
mu_mle = np.mean(x)
sigma2_mle = np.var(x, ddof=0)
sigma2_unbiased = np.var(x, ddof=1)
assert np.isclose(mu_mle, 3.0)
assert np.isclose(sigma2_mle, 1.0)
assert np.isclose(sigma2_unbiased, 2.0)
```

---

## 4. The mistake people actually make

Using ddof=0 (MLE variance) when an unbiased estimate of population variance is required.

---

## Check yourself

1. Is the MLE of the variance for a normal distribution unbiased?
2. What factor corrects the MLE variance bias?

<details>
<summary>Answers</summary>

1. No, it has bias (n - 1)/n.
2. Bessel's correction factor: n / (n - 1).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](10_Fisher_Information_and_the_CramerRao_Bound.md)
