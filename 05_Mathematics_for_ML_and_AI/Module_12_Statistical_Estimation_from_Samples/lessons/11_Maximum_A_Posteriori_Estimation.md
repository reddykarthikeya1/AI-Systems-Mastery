# Lesson 12.11 — Maximum A Posteriori Estimation

> **Module 12:** Statistical Estimation from Samples · Lesson 11 of 22

---

## What you will be able to do after this lesson

- [ ] Formulate MAP estimation theta_hat_MAP = argmax [log p(X | theta) + log p(theta)].
- [ ] Combine prior belief with empirical data.

## Prerequisites

- 12.08 Log-Likelihood and Bayes Rule (Module 10).

---

## 1. The idea

**Maximum A Posteriori (MAP)** estimation incorporates a **prior distribution** $p(\theta)$ over parameters using Bayes' rule:
$$\hat{\theta}_{MAP} = \text{argmax}_\theta [p(X \mid \theta) p(\theta)] = \text{argmax}_\theta [\log p(X \mid \theta) + \log p(\theta)]$$
As sample size $n \to \infty$, the likelihood term dominates the prior, and MAP converges to MLE.

---

## 2. Worked example

Prior says coin $p \sim \text{Beta}(2, 2)$ (pseudo-counts 1 head, 1 tail). Observing 3 heads in 3 flips ($n=3$): MLE gives $\hat{p} = 1.0$. MAP gives $(3 + 1)/(3 + 2) = 4/5 = 0.8$, preventing extreme overfitting.

---

## 3. Verify it in code

```python
import numpy as np
# Coin flip with 3 heads in 3 tosses
heads, total = 3, 3
p_mle = heads / total

# Beta(2, 2) prior mode: (h + alpha - 1) / (n + alpha + beta - 2)
alpha, beta_param = 2.0, 2.0
p_map = (heads + alpha - 1) / (total + alpha + beta_param - 2)

assert np.isclose(p_mle, 1.0)
assert np.isclose(p_map, 4.0 / 5.0)
assert p_map < p_mle
```

---

## 4. The mistake people actually make

Believing MAP outputs a full posterior probability distribution. MAP only finds the single point with maximum posterior density (mode).

---

## Check yourself

1. What additional term does MAP add to the MLE objective?
2. What happens to MAP estimation as the dataset size n approaches infinity?

<details>
<summary>Answers</summary>

1. The log-prior density: log p(theta).
2. It converges to the Maximum Likelihood Estimate (MLE).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](12_MAP_as_Regularized_MLE.md)
