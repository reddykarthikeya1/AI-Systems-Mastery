# Lesson 10.03 — The Axioms of Probability

> **Module 10:** Reasoning Under Uncertainty · Lesson 3 of 41

---

## What you will be able to do after this lesson

- [ ] State Kolmogorov's 3 axioms: non-negativity P(E) >= 0, unitarity P(Omega) = 1, countable additivity.
- [ ] Derive complement rule P(not E) = 1 - P(E).

## Prerequisites

- 10.02 Sample Spaces and Events.

---

## 1. The idea

Kolmogorov's Three Axioms:
1. **Non-negativity**: $P(E) \ge 0$ for every event $E$.
2. **Unitarity**: $P(\Omega) = 1$.
3. **Countable Additivity**: For disjoint events $E_1, E_2, \dots$ ($E_i \cap E_j = \emptyset$): $P(\bigcup E_i) = \sum P(E_i)$.
All probability laws (e.g. $P(A \cup B) = P(A) + P(B) - P(A \cap B)$) derive from these 3 axioms.

---

## 2. Worked example

If $P(A) = 0.6$ and $P(B) = 0.5$ with $P(A \cap B) = 0.2$: $P(A \cup B) = 0.6 + 0.5 - 0.2 = 0.9$. $P(A^c) = 1 - 0.6 = 0.4$.

---

## 3. Verify it in code

```python
import numpy as np
p_a = 0.6
p_b = 0.5
p_ab = 0.2
p_union = p_a + p_b - p_ab
assert np.isclose(p_union, 0.9)
assert np.isclose(1.0 - p_a, 0.4)
```

---

## 4. The mistake people actually make

Summing probabilities of non-disjoint events without subtracting their intersection.

---

## Check yourself

1. What is Kolmogorov's third axiom?
2. What is P(empty set)?

<details>
<summary>Answers</summary>

1. Countable additivity for mutually disjoint events.
2. Zero: P(empty) = 0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](04_Counting_Permutations_and_Combinations.md)
