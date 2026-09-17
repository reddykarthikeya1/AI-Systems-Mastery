# Lesson 10.02 — Sample Spaces and Events

> **Module 10:** Reasoning Under Uncertainty · Lesson 2 of 41

---

## What you will be able to do after this lesson

- [ ] Define sample space Omega and event E as subset of Omega.
- [ ] Compute event probabilities via set operations.

## Prerequisites

- 10.01 Why Probability.

---

## 1. The idea

The **sample space** $\Omega$ is the set of all mutually exclusive possible outcomes of a random trial. An **event** $E \subseteq \Omega$ is any subset of outcomes. The probability of event $E$ is the measure of its subset relative to $\Omega$.

---

## 2. Worked example

Rolling a 6-sided die: $\Omega = \{1, 2, 3, 4, 5, 6\}$. Event 'even number' is $E = \{2, 4, 6\}$. $P(E) = |E| / |\Omega| = 3/6 = 0.5$.

---

## 3. Verify it in code

```python
import numpy as np
omega = set(range(1, 7))
event_even = {2, 4, 6}
p_even = len(event_even) / len(omega)
assert np.isclose(p_even, 0.5)
```

---

## 4. The mistake people actually make

Specifying a sample space whose elementary outcomes are not mutually exclusive or collectively exhaustive.

---

## Check yourself

1. Can two outcomes in sample space Omega occur simultaneously in a single trial?
2. What is an event mathematically?

<details>
<summary>Answers</summary>

1. No, elementary outcomes in Omega are mutually exclusive.
2. A subset of the sample space Omega.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](03_The_Axioms_of_Probability.md)
