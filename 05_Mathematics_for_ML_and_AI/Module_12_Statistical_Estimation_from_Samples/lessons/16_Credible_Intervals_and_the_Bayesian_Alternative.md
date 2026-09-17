# Lesson 12.16 — Credible Intervals and the Bayesian Alternative

> **Module 12:** Statistical Estimation from Samples · Lesson 16 of 22

---

## What you will be able to do after this lesson

- [ ] Construct a Bayesian 95% credible interval from posterior percentiles.
- [ ] Contrast credible interval interpretation with frequentist confidence interval.

## Prerequisites

- 12.13 Conjugate Priors and 12.15 CI Meaning.

---

## 1. The idea

In Bayesian statistics, $\theta$ is a random variable endowed with a posterior distribution $p(\theta \mid X)$. A **95% Credible Interval** $[a, b]$ satisfies $\int_a^b p(\theta \mid X) d\theta = 0.95$. It genuinely means: *Given this data, there is a 95% probability that $\theta$ lies between $a$ and $b$*.

---

## 2. Worked example

For posterior $\mathcal{N}(10, 2^2)$, a 95% credible interval is $10 \pm 1.96(2) = [6.08, 13.92]$.

---

## 3. Verify it in code

```python
import numpy as np
post_mu = 10.0
post_std = 2.0
z = 1.96
cred_interval = (post_mu - z * post_std, post_mu + z * post_std)
assert np.isclose(cred_interval[0], 6.08)
assert np.isclose(cred_interval[1], 13.92)
```

---

## 4. The mistake people actually make

Conflating Bayesian credible intervals (which depend on a prior) with frequentist confidence intervals.

---

## Check yourself

1. Can you say there is a 95% probability theta is in [a, b] for a Bayesian credible interval?
2. What does a credible interval require that a frequentist CI does not?

<details>
<summary>Answers</summary>

1. Yes, because Bayesian parameters are treated as random variables with posterior distributions.
2. A prior distribution p(theta).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](17_Hypothesis_Testing_and_the_pValue.md)
