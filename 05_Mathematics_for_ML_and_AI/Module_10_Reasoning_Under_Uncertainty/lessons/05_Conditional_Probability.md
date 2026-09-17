# Lesson 10.05 — Conditional Probability

> **Module 10:** Reasoning Under Uncertainty · Lesson 5 of 41

---

## What you will be able to do after this lesson

- [ ] Define conditional probability P(A | B) = P(A cap B) / P(B).
- [ ] Update sample space from Omega to B.

## Prerequisites

- 10.03 Probability Axioms.

---

## 1. The idea

Conditioning on event $B$ shrinks the effective sample space from $\Omega$ down to $B$:
$$P(A \mid B) = \frac{P(A \cap B)}{P(B)} \quad (\text{for } P(B) > 0)$$
It answers: *Given that B has definitively occurred, what fraction of B also belongs to A?*

---

## 2. Worked example

Die roll: $P(\text{roll } 4) = 1/6$. Given that the roll is even ($B=\{2, 4, 6\}$, $P(B)=1/2$), $P(4 \mid \text{even}) = (1/6) / (1/2) = 1/3$.

---

## 3. Verify it in code

```python
import numpy as np
p_ab = 1.0 / 6.0
p_b = 3.0 / 6.0
p_a_given_b = p_ab / p_b
assert np.isclose(p_a_given_b, 1.0 / 3.0)
```

---

## 4. The mistake people actually make

Confusing P(A | B) with P(B | A). (e.g. P(cough | lung cancer) != P(lung cancer | cough)).

---

## Check yourself

1. Is P(A | B) generally equal to P(B | A)?
2. What is P(B | B)?

<details>
<summary>Answers</summary>

1. No, the direction of conditioning alters the denominator and meaning.
2. Exactly 1.0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](06_Independence_versus_Conditional_Independence.md)
