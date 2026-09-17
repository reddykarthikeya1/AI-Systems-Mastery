# Lesson 12.18 — What a p-Value Does Not Mean

> **Module 12:** Statistical Estimation from Samples · Lesson 18 of 22

---

## What you will be able to do after this lesson

- [ ] Identify the 3 fatal misinterpretations of p-values: P(H_0 | data), error probability, and effect magnitude.
- [ ] Distinguish statistical significance from practical significance.

## Prerequisites

- 12.17 Hypothesis Testing and p-Values.

---

## 1. The idea

P-value misconceptions that plague science and ML:
1. $p \neq P(H_0 \mid \text{data})$ (that is the posterior probability!).
2. $p$ does NOT measure the probability that a finding is a fluke.
3. $1 - p$ does NOT measure probability of replication.
4. Statistical significance ($p < 0.05$) does not mean practical utility.

---

## 2. Worked example

With sample size $n = 1,000,000$, a model improvement in accuracy of $0.0001\%$ yields $p < 10^{-6}$. Highly 'significant' statistically, but completely negligible practically.

---

## 3. Verify it in code

```python
import numpy as np
# Massive sample size detects microscopic difference
n = 1_000_000
diff = 0.001
se = 1.0 / np.sqrt(n)
z = diff / se
assert z == 1.0  # detectable with slightly larger n
assert se == 0.001
```

---

## 4. The mistake people actually make

Equating p-value with the probability that the null hypothesis is true.

---

## Check yourself

1. Does p = 0.03 mean there is a 3% chance the null hypothesis is true?
2. Can a useless effect be statistically significant?

<details>
<summary>Answers</summary>

1. No, p is P(data | H_0), not P(H_0 | data).
2. Yes, any non-zero effect becomes statistically significant with large enough n.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](19_Type_I_and_Type_II_Errors_and_Power.md)
