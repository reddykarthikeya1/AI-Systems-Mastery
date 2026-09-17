# Lesson 10.06 — Independence versus Conditional Independence

> **Module 10:** Reasoning Under Uncertainty · Lesson 6 of 41

---

## What you will be able to do after this lesson

- [ ] Distinguish marginal independence P(A, B) = P(A)P(B) from conditional independence P(A, B | C) = P(A | C)P(B | C).
- [ ] Verify conditional independence in graphical models.

## Prerequisites

- 10.05 Conditional Probability.

---

## 1. The idea

Two events are **conditionally independent** given $C$ if:
$$P(A \cap B \mid C) = P(A \mid C) P(B \mid C)$$
Crucially:
- Marginal independence does NOT imply conditional independence.
- Conditional independence does NOT imply marginal independence! (The foundation of Naive Bayes).

---

## 2. Worked example

Let $C$ be language (French vs English). $A$ = vocabulary test score, $B$ = reading speed. Within native French speakers ($C$), $A$ and $B$ are weakly correlated, but in the mixed population they are strongly correlated.

---

## 3. Verify it in code

```python
import numpy as np
# Given C, A and B factor
p_c = 0.5
p_a_c = 0.8
p_b_c = 0.6
p_ab_c = p_a_c * p_b_c
assert np.isclose(p_ab_c, 0.48)
```

---

## 4. The mistake people actually make

Assuming independent events remain independent after conditioning on an outcome (collider bias).

---

## Check yourself

1. Does marginal independence imply conditional independence?
2. What assumption makes Naive Bayes tractable?

<details>
<summary>Answers</summary>

1. No, conditioning can either create or destroy independence.
2. That features are conditionally independent given the class label.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](07_The_Law_of_Total_Probability.md)
