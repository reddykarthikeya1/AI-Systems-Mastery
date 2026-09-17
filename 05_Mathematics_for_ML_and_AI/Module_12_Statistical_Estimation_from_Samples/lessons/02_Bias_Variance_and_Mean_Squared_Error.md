# Lesson 12.02 — Bias, Variance and Mean Squared Error

> **Module 12:** Statistical Estimation from Samples · Lesson 2 of 22

---

## What you will be able to do after this lesson

- [ ] Prove MSE(theta_hat) = Bias(theta_hat)^2 + Var(theta_hat).
- [ ] Quantify the bias-variance tradeoff in parameter estimation.

## Prerequisites

- 12.01 Populations, Samples and Estimators.

---

## 1. The idea

**Bias** is systematic error: $\text{Bias}(\hat{\theta}) = \mathbb{E}[\hat{\theta}] - \theta$. **Variance** measures dispersion: $\text{Var}(\hat{\theta}) = \mathbb{E}[(\hat{\theta} - \mathbb{E}[\hat{\theta}])^2]$. Total error is governed by the universal decomposition:
$$\text{MSE}(\hat{\theta}) = \mathbb{E}[(\hat{\theta} - \theta)^2] = \text{Bias}(\hat{\theta})^2 + \text{Var}(\hat{\theta})$$

---

## 2. Worked example

Estimator has bias 0.2 and variance 0.05. $\text{MSE} = (0.2)^2 + 0.05 = 0.04 + 0.05 = 0.09$.

---

## 3. Verify it in code

```python
import numpy as np
bias = 0.2
var = 0.05
mse = bias**2 + var
assert np.isclose(mse, 0.09)
```

---

## 4. The mistake people actually make

Assuming an unbiased estimator always has lower MSE than a biased one. A slightly biased estimator with much lower variance often wins.

---

## Check yourself

1. What is the mathematical definition of an unbiased estimator?
2. What is MSE composed of?

<details>
<summary>Answers</summary>

1. E[theta_hat] = theta (Bias = 0).
2. Squared bias plus variance: Bias^2 + Var.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](03_Consistency_and_Efficiency.md)
