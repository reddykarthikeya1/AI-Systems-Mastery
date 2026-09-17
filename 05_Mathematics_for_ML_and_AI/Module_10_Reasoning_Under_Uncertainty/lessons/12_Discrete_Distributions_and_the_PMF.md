# Lesson 10.12 — Discrete Distributions and the PMF

> **Module 10:** Reasoning Under Uncertainty · Lesson 12 of 41

---

## What you will be able to do after this lesson

- [ ] Define Probability Mass Function p(x) = P(X = x).
- [ ] Verify normalization sum_x p(x) = 1 in NumPy.

## Prerequisites

- 10.11 Random Variables.

---

## 1. The idea

For a discrete random variable, the **Probability Mass Function (PMF)** $p(x) = P(X = x)$ satisfies $p(x) \ge 0$ and $\sum_x p(x) = 1$. The probability of any event $A$ is $\sum_{x \in A} p(x)$.

---

## 2. Worked example

Fair die: $p(x) = 1/6$ for $x \in \{1, 2, 3, 4, 5, 6\}$. $\sum_{x=1}^6 1/6 = 1.0$.

---

## 3. Verify it in code

```python
import numpy as np
pmf = np.full(6, 1.0 / 6.0)
assert np.all(pmf >= 0.0)
assert np.isclose(np.sum(pmf), 1.0)
```

---

## 4. The mistake people actually make

Assigning PMF values greater than 1. For discrete variables, p(x) is a true probability, so 0 <= p(x) <= 1.

---

## Check yourself

1. What is the maximum possible value of a discrete PMF p(x)?
2. What must the sum of a PMF over all supported values equal?

<details>
<summary>Answers</summary>

1. 1.0.
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

[Module README](../README.md) · [Next →](13_Continuous_Distributions_and_the_PDF.md)
