# Lesson 10.01 — Why Probability, Not Just Statistics

> **Module 10:** Reasoning Under Uncertainty · Lesson 1 of 41

---

## What you will be able to do after this lesson

- [ ] Distinguish forward deductive probability (data generator known) from backward inductive statistics (parameters unknown).
- [ ] Simulate generative models in NumPy.

## Prerequisites

- Set language (Module 01).

---

## 1. The idea

**Probability** is forward reasoning: knowing the generative data mechanism ($P(X \mid \theta)$), it predicts the properties of outcomes. **Statistics** is inverse reasoning: observing noisy data ($X$), it infers the underlying generating process ($\theta$). Machine learning requires both: probabilistic models define data generators; statistical learning fits parameters.

---

## 2. Worked example

Probability: fair coin ($p=0.5$), what is $P(\text{3 heads in 3 flips}) = (0.5)^3 = 0.125$. Statistics: observe 3 heads in 3 flips, what is likely range of $p$?

---

## 3. Verify it in code

```python
import numpy as np
p = 0.5
prob_3_heads = p**3
assert np.isclose(prob_3_heads, 0.125)
```

---

## 4. The mistake people actually make

Treating observed sample frequencies as immutable population laws rather than random realizations.

---

## Check yourself

1. What is the forward direction of reasoning in probability?
2. What is the inverse direction of reasoning in statistics?

<details>
<summary>Answers</summary>

1. From known parameters to predicted data distributions.
2. From observed data back to unknown parameters.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Sample_Spaces_and_Events.md)
