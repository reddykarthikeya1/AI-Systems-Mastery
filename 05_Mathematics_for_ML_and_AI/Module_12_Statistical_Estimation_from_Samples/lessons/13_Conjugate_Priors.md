# Lesson 12.13 — Conjugate Priors

> **Module 12:** Statistical Estimation from Samples · Lesson 13 of 22

---

## What you will be able to do after this lesson

- [ ] Define conjugacy: posterior p(theta | x) belongs to the same family as prior p(theta).
- [ ] Perform Beta-Binomial and Gaussian-Gaussian updates analytically.

## Prerequisites

- 12.11 MAP Estimation.

---

## 1. The idea

A prior is **conjugate** to a likelihood if the posterior belongs to the exact same parametric family. This allows exact analytical Bayesian updates without numerical integration:
- **Beta prior + Binomial likelihood** $\to$ **Beta posterior**: $\text{Beta}(\alpha + k, \beta + n - k)$.
- **Gaussian prior + Gaussian likelihood** $\to$ **Gaussian posterior**.

---

## 2. Worked example

Prior $\text{Beta}(3, 3)$. Observe 4 heads and 1 tail ($n=5, k=4$). Posterior is $\text{Beta}(3+4, 3+1) = \text{Beta}(7, 4)$.

---

## 3. Verify it in code

```python
import numpy as np
alpha_prior, beta_prior = 3.0, 3.0
heads, tails = 4, 1

alpha_post = alpha_prior + heads
beta_post = beta_prior + tails

assert alpha_post == 7.0
assert beta_post == 4.0
# Posterior mean
post_mean = alpha_post / (alpha_post + beta_post)
assert np.isclose(post_mean, 7.0 / 11.0)
```

---

## 4. The mistake people actually make

Using non-conjugate priors and expecting closed-form analytical posterior distributions.

---

## Check yourself

1. What is the conjugate prior for the Bernoulli/Binomial likelihood?
2. What is the conjugate prior for the mean of a Normal likelihood with known variance?

<details>
<summary>Answers</summary>

1. The Beta distribution.
2. A Normal distribution.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](14_Confidence_Intervals.md)
