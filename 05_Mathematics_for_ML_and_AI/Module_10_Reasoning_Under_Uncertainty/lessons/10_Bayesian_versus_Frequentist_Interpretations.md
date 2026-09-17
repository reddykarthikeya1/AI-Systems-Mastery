# Lesson 10.10 — Bayesian versus Frequentist Interpretations

> **Module 10:** Reasoning Under Uncertainty · Lesson 10 of 41

---

## What you will be able to do after this lesson

- [ ] Contrast Frequentist probability (long-run relative frequency) with Bayesian probability (epistemic degree of belief).
- [ ] Recognize when each philosophical paradigm is appropriate.

## Prerequisites

- 10.01 Why Probability.

---

## 1. The idea

Two philosophical views of probability:
- **Frequentist**: probability is the limiting relative frequency in infinite repeated identical trials. Parameters are fixed constants; data is random.
- **Bayesian**: probability quantifies degree of belief (epistemic uncertainty). Parameters are random variables described by probability distributions; observed data is fixed.

---

## 2. Worked example

'There is a 70% chance of rain tomorrow.' Frequentist: impossible to repeat tomorrow 10,000 times. Bayesian: a coherent 0.7 degree of belief based on meteorological evidence.

---

## 3. Verify it in code

```python
import numpy as np
# Bayesian belief update: Beta(alpha, beta)
alpha_prior = 1.0
beta_prior = 1.0
# Observe 8 successes, 2 failures
alpha_post = alpha_prior + 8
beta_post = beta_prior + 2
expected_p = alpha_post / (alpha_post + beta_post)
assert np.isclose(expected_p, 9.0 / 12.0)
```

---

## 4. The mistake people actually make

Claiming one paradigm is mathematically invalid. Both obey Kolmogorov's axioms; they differ only in interpretation and philosophy.

---

## Check yourself

1. How does a Bayesian treat model parameters?
2. How does a Frequentist treat model parameters?

<details>
<summary>Answers</summary>

1. As random variables with probability distributions.
2. As fixed, unknown true constants.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](11_Random_Variables.md)
