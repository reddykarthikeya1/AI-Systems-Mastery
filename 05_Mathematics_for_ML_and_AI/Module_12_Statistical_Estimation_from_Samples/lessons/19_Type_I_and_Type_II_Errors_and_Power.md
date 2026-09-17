# Lesson 12.19 — Type I and Type II Errors and Power

> **Module 12:** Statistical Estimation from Samples · Lesson 19 of 22

---

## What you will be able to do after this lesson

- [ ] Define Type I error alpha (false positive) and Type II error beta (false negative).
- [ ] Define statistical power = 1 - beta.

## Prerequisites

- 12.17 Hypothesis Testing.

---

## 1. The idea

Decision outcomes in hypothesis testing:
- **Type I error** $\alpha = P(\text{Reject } H_0 \mid H_0 \text{ true})$ (False Alarm).
- **Type II error** $\beta = P(\text{Fail to reject } H_0 \mid H_1 \text{ true})$ (Miss).
- **Statistical Power** $= 1 - \beta$ is the probability of correctly detecting a real effect.

---

## 2. Worked example

Setting $\alpha = 0.05$ controls false alarms to 5%. If a test has $80\%$ power, $\beta = 1 - 0.80 = 0.20$ (20% chance of missing a real effect).

---

## 3. Verify it in code

```python
import numpy as np
alpha = 0.05
power = 0.80
beta = 1.0 - power
assert np.isclose(beta, 0.20)
assert np.isclose(power + beta, 1.0)
```

---

## 4. The mistake people actually make

Running an A/B test with underpowered sample size ($< 80\%$), leading to false negative conclusions that new models don't work.

---

## Check yourself

1. What is Type I error?
2. What is the relationship between Type II error beta and statistical power?

<details>
<summary>Answers</summary>

1. Rejecting a true null hypothesis (false positive).
2. Power = 1 - beta.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](20_Multiple_Comparisons_and_the_Bonferroni_Correction.md)
