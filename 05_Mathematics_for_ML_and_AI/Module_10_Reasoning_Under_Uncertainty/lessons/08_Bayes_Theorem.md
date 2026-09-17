# Lesson 10.08 — Bayes' Theorem

> **Module 10:** Reasoning Under Uncertainty · Lesson 8 of 41

---

## What you will be able to do after this lesson

- [ ] Invert conditional probabilities via Bayes' Theorem: P(B | A) = P(A | B) P(B) / P(A).
- [ ] Update prior beliefs into posterior probabilities.

## Prerequisites

- 10.05 Conditional Probability and 10.07 Law of Total Probability.

---

## 1. The idea

**Bayes' Theorem** is the mathematical engine of belief revision:
$$P(B_j \mid A) = \frac{P(A \mid B_j) P(B_j)}{\sum_i P(A \mid B_i) P(B_i)} = \frac{\text{Likelihood} \times \text{Prior}}{\text{Evidence}}$$
It calculates the probability of cause $B_j$ given observed effect $A$.

---

## 2. Worked example

Using the factory: Given a part is defective ($D$), what is the probability it came from Machine 2? $P(M_2 \mid D) = \frac{P(D \mid M_2) P(M_2)}{P(D)} = \frac{0.05 \times 0.4}{0.032} = \frac{0.020}{0.032} = 0.625$ (62.5%).

---

## 3. Verify it in code

```python
import numpy as np
p_m2 = 0.4
p_d_m2 = 0.05
p_d = 0.032
p_m2_given_d = (p_d_m2 * p_m2) / p_d
assert np.isclose(p_m2_given_d, 0.625)
```

---

## 4. The mistake people actually make

Neglecting the prior P(B) and equating P(B | A) with the likelihood P(A | B).

---

## Check yourself

1. What is the numerator in Bayes' rule?
2. What role does the denominator P(A) play?

<details>
<summary>Answers</summary>

1. Likelihood times Prior: P(A | B) P(B).
2. It acts as a normalizer ensuring posterior probabilities sum to 1.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](09_Base_Rates_and_the_Prosecutors_Fallacy.md)
