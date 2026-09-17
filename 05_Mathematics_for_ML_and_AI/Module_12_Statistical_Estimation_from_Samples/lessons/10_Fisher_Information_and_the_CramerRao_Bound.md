# Lesson 12.10 — Fisher Information and the Cramér-Rao Bound

> **Module 12:** Statistical Estimation from Samples · Lesson 10 of 22

---

## What you will be able to do after this lesson

- [ ] Compute Fisher Information I(theta) = -E[d^2/dtheta^2 log f(X; theta)].
- [ ] State Cramér-Rao Lower Bound: Var(theta_hat) >= 1 / (n I(theta)).

## Prerequisites

- 12.09 Normal MLE.

---

## 1. The idea

**Fisher Information** $I(\theta) = \mathbb{E}[(\frac{\partial \ell}{\partial \theta})^2] = -\mathbb{E}[\frac{\partial^2 \ell}{\partial \theta^2}]$ measures the curvature of the log-likelihood (how much information data carries about $\theta$). The **Cramér-Rao Lower Bound (CRLB)** states that no unbiased estimator can have variance lower than $\frac{1}{n I(\theta)}$.

---

## 2. Worked example

For $\mathcal{N}(\mu, \sigma^2)$, $I(\mu) = 1/\sigma^2$. CRLB is $\sigma^2/n$. The sample mean has variance $\sigma^2/n$, proving $\bar{X}$ is a Minimum Variance Unbiased Estimator (MVUE).

---

## 3. Verify it in code

```python
import numpy as np
sigma = 2.0
n = 50
fisher_info = 1.0 / (sigma**2)
crlb = 1.0 / (n * fisher_info)
assert np.isclose(crlb, (sigma**2) / n)
assert np.isclose(crlb, 4.0 / 50.0)
```

---

## 4. The mistake people actually make

Assuming estimators can have zero variance. Any estimator based on a finite noisy sample is bounded below by the CRLB.

---

## Check yourself

1. What does the Cramér-Rao Lower Bound establish?
2. What does high Fisher Information indicate about the likelihood peak?

<details>
<summary>Answers</summary>

1. The theoretical minimum variance achievable by any unbiased estimator.
2. Sharp curvature (high confidence and low variance in parameter estimates).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](11_Maximum_A_Posteriori_Estimation.md)
