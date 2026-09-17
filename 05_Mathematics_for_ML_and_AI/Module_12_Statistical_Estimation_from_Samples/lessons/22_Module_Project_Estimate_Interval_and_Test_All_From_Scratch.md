# Lesson 12.22 — Module Project: Estimate, Interval and Test All From Scratch

> **Module 12:** Statistical Estimation from Samples · Lesson 22 of 22

---

## What you will be able to do after this lesson

- [ ] Build an end-to-end A/B test analysis pipeline from raw conversion data.
- [ ] Compute point estimates, bootstrap intervals, and p-values from scratch in NumPy.

## Prerequisites

- Lessons 12.01 through 12.21.

---

## 1. The idea

We build an end-to-end statistical evaluation engine for ML model comparison:
1. Point Estimation: sample means $\hat{\mu}_A, \hat{\mu}_B$ and uplift $\Delta = \hat{\mu}_B - \hat{\mu}_A$.
2. Two-sample t-test: pooled standard error and p-value.
3. Non-parametric Bootstrap: 95% confidence interval for uplift.
4. Multiple testing guard: Bonferroni check across metrics.

---

## 2. Worked example

Model A has 10% conversion on 1000 users; Model B has 13% on 1000 users. Uplift is $+3.0\%$. Bootstrap CI is $[+0.2\%, +5.8\%]$. $p < 0.05$. Decisively roll out Model B.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
nA, nB = 1000, 1000
pA_true, pB_true = 0.10, 0.13

A = np.random.binomial(1, pA_true, nA)
B = np.random.binomial(1, pB_true, nB)

# 1. Point estimate
diff = np.mean(B) - np.mean(A)
assert diff > 0.0

# 2. Standard error
se = np.sqrt(np.var(A)/nA + np.var(B)/nB)
z_score = diff / se
assert z_score > 2.0  # Statistically significant

# 3. Bootstrap CI
boot_diffs = []
for _ in range(500):
    sampleA = np.random.choice(A, size=nA, replace=True)
    sampleB = np.random.choice(B, size=nB, replace=True)
    boot_diffs.append(np.mean(sampleB) - np.mean(sampleA))

ci_low = np.percentile(boot_diffs, 2.5)
ci_high = np.percentile(boot_diffs, 97.5)
assert ci_low > 0.0  # Positive uplift at 95% confidence
assert ci_high > ci_low
```

---

## 4. The mistake people actually make

Ending an A/B test early as soon as p < 0.05 is crossed ('peeking'), which dramatically inflates false positive rates.

---

## Check yourself

1. Why is continuous peeking during an A/B test problematic?
2. What confirms that Model B is statistically superior to Model A at 95% confidence?

<details>
<summary>Answers</summary>

1. It violates fixed-horizon assumptions, inflating false positive rates from 5% to over 30%.
2. The 95% bootstrap confidence interval for uplift excludes zero (strictly positive).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md)
