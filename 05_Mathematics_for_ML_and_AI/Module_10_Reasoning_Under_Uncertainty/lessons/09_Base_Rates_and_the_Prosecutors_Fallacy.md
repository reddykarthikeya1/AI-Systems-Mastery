# Lesson 10.09 — Base Rates and the Prosecutor's Fallacy

> **Module 10:** Reasoning Under Uncertainty · Lesson 9 of 41

---

## What you will be able to do after this lesson

- [ ] Demonstrate the Base Rate Fallacy: rare conditions have low positive predictive value even with 99% accurate tests.
- [ ] Identify the Prosecutor's Fallacy P(match | innocent) vs P(innocent | match).

## Prerequisites

- 10.08 Bayes Theorem.

---

## 1. The idea

The **Base Rate Fallacy** occurs when people ignore the low prior prevalence $P(Disease)$ of a rare condition. If a disease affects 1 in 10,000, a test with 99% sensitivity and 99% specificity yields mostly false positives: $P(Disease \mid +) \approx 1\%$, because the false alarm count from the 9,999 healthy people ($~100$) swamps the 1 true positive!

---

## 2. Worked example

Prior $P(D) = 0.001$. Test accuracy 99% ($P(+ \mid D)=0.99, P(+ \mid D^c)=0.01$).
$P(+) = 0.001(0.99) + 0.999(0.01) = 0.00099 + 0.00999 = 0.01098$.
$P(D \mid +) = 0.00099 / 0.01098 \approx 0.090$ (only 9% chance of having disease despite positive test!).

---

## 3. Verify it in code

```python
import numpy as np
p_d = 0.001
sens = 0.99
spec = 0.99
p_pos = p_d * sens + (1.0 - p_d) * (1.0 - spec)
ppv = (sens * p_d) / p_pos
assert np.isclose(ppv, 0.09016, atol=1e-3)
assert ppv < 0.10
```

---

## 4. The mistake people actually make

Interpreting 99% test accuracy as meaning a person who tests positive has a 99% chance of being sick.

---

## Check yourself

1. Why are most positive test results false positives for ultra-rare diseases?
2. What is Positive Predictive Value (PPV)?

<details>
<summary>Answers</summary>

1. Because the vast healthy population generates far more false alarms than true cases.
2. P(Disease | Positive test).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](10_Bayesian_versus_Frequentist_Interpretations.md)
