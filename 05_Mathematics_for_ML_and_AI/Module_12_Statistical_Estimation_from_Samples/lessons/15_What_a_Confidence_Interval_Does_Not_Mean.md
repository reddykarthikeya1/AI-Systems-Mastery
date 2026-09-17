# Lesson 12.15 — What a Confidence Interval Does Not Mean

> **Module 12:** Statistical Estimation from Samples · Lesson 15 of 22

---

## What you will be able to do after this lesson

- [ ] Explain why P(theta in [L, U]) is either 0 or 1 once data is observed.
- [ ] Interpret confidence level as procedural coverage frequency over repeated experiments.

## Prerequisites

- 12.14 Confidence Intervals.

---

## 1. The idea

The most common statistical fallacy: *There is a 95% probability that the parameter is in $[a, b]$.* In frequentist statistics, $\theta$ is fixed, not random. Once numbers $[a, b]$ are computed, the interval either contains $\theta$ (probability 1) or it doesn't (probability 0). The '95%' describes the **procedure**: 95% of generated intervals contain $\theta$.

---

## 2. Worked example

Simulating 1,000 independent 95% intervals: approximately 950 cover true $\mu = 0$, while roughly 50 miss entirely.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
true_mu = 0.0
n = 30
z = 1.96
covered = 0
reps = 500

for _ in range(reps):
    sample = np.random.normal(true_mu, 1.0, n)
    m = np.mean(sample)
    se = 1.0 / np.sqrt(n)
    if (m - z * se) <= true_mu <= (m + z * se):
        covered += 1

coverage = covered / reps
assert 0.92 < coverage < 0.98
```

---

## 4. The mistake people actually make

Stating that a single calculated 95% CI has a 95% chance of containing the parameter.

---

## Check yourself

1. What does the 95% in a 95% confidence interval describe?
2. In frequentist statistics, is the parameter theta random?

<details>
<summary>Answers</summary>

1. The long-run coverage rate of the procedure across hypothetical repeated samples.
2. No, theta is a fixed unknown constant.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](16_Credible_Intervals_and_the_Bayesian_Alternative.md)
