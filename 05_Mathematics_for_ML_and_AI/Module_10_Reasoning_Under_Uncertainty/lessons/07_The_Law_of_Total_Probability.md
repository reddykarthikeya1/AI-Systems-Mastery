# Lesson 10.07 — The Law of Total Probability

> **Module 10:** Reasoning Under Uncertainty · Lesson 7 of 41

---

## What you will be able to do after this lesson

- [ ] Decompose P(A) = sum_i P(A | B_i) P(B_i) over partition B_1, ..., B_k.
- [ ] Calculate marginal probability across heterogeneous subpopulations.

## Prerequisites

- 10.05 Conditional Probability.

---

## 1. The idea

If $B_1, \dots, B_k$ partition the sample space $\Omega$ ($\bigcup B_i = \Omega$ and $B_i \cap B_j = \emptyset$), then for any event $A$:
$$P(A) = \sum_{i=1}^k P(A \cap B_i) = \sum_{i=1}^k P(A \mid B_i) P(B_i)$$
This breaks intractable global probabilities into weighted averages of conditional cases.

---

## 2. Worked example

Factory with 2 machines: Machine 1 produces 60% of parts (2% defective), Machine 2 produces 40% (5% defective). Total defective rate: $P(D) = 0.6(0.02) + 0.4(0.05) = 0.012 + 0.020 = 0.032$ (3.2%).

---

## 3. Verify it in code

```python
import numpy as np
p_m1 = 0.6
p_m2 = 0.4
p_d_m1 = 0.02
p_d_m2 = 0.05
p_d = p_m1 * p_d_m1 + p_m2 * p_d_m2
assert np.isclose(p_d, 0.032)
```

---

## 4. The mistake people actually make

Applying the law of total probability when events B_i overlap or do not cover the whole space.

---

## Check yourself

1. What property must the sets B_1, ..., B_k satisfy to apply the Law of Total Probability?
2. What does P(A) equal if all P(A | B_i) = c?

<details>
<summary>Answers</summary>

1. They must form a partition of Omega (disjoint and covering Omega).
2. c (the constant probability).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](08_Bayes_Theorem.md)
