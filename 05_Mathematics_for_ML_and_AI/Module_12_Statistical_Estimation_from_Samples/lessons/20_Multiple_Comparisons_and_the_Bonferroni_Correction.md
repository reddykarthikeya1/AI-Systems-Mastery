# Lesson 12.20 — Multiple Comparisons and the Bonferroni Correction

> **Module 12:** Statistical Estimation from Samples · Lesson 20 of 22

---

## What you will be able to do after this lesson

- [ ] Calculate family-wise error rate FWER = 1 - (1 - alpha)^m for m tests.
- [ ] Apply Bonferroni threshold alpha / m to prevent p-hacking.

## Prerequisites

- 12.19 Type I and Type II Errors.

---

## 1. The idea

Testing $m$ independent hypotheses at level $\alpha = 0.05$ causes the **family-wise error rate** to explode: $\text{FWER} = 1 - (1 - \alpha)^m$. For $m = 20$ tests, $\text{FWER} = 1 - (0.95)^{20} \approx 64.2\%$ (you are more likely than not to find a false positive!). The **Bonferroni correction** uses threshold $\alpha_{adj} = \alpha / m$.

---

## 2. Worked example

For $m = 20$ tests and $\alpha = 0.05$, adjusted threshold is $\alpha_{adj} = 0.05 / 20 = 0.0025$. Only tests with $p < 0.0025$ are declared significant.

---

## 3. Verify it in code

```python
import numpy as np
m = 20
alpha = 0.05
fwer_naive = 1.0 - (1.0 - alpha)**m
assert fwer_naive > 0.60  # 64% chance of false positive!

alpha_bonferroni = alpha / m
assert np.isclose(alpha_bonferroni, 0.0025)
```

---

## 4. The mistake people actually make

Testing 50 different feature variations and celebrating the one that reached p < 0.05 without multiple testing correction (p-hacking).

---

## Check yourself

1. What is the probability of at least one false positive when running 20 independent tests at alpha=0.05?
2. What is the Bonferroni corrected threshold for m tests?

<details>
<summary>Answers</summary>

1. Approximately 64.2%.
2. alpha / m.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](21_The_Bootstrap.md)
