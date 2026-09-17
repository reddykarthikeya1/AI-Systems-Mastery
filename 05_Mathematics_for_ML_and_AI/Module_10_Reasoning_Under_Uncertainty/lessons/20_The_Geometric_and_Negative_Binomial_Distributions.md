# Lesson 10.20 — The Geometric and Negative Binomial Distributions

> **Module 10:** Reasoning Under Uncertainty · Lesson 20 of 41

---

## What you will be able to do after this lesson

- [ ] Define Geometric(p) as number of trials until first success: P(k) = (1-p)^(k-1) p.
- [ ] Prove memorylessness property P(X > s + t | X > s) = P(X > t).

## Prerequisites

- 10.19 Bernoulli Distributions.

---

## 1. The idea

The **Geometric distribution** models the trial number $k$ of the *first* success: $P(X = k) = (1-p)^{k-1} p$. Mean is $\mathbb{E}[X] = 1/p$. It is the only discrete distribution with the **memoryless property**: the past failures do not alter the probability of future success.

---

## 2. Worked example

Rolling until first 6 ($p = 1/6$): expected rolls $= 1 / (1/6) = 6$. Probability of needing 3 rolls: $(5/6)^2 (1/6) = 25/216 \approx 0.116$.

---

## 3. Verify it in code

```python
import numpy as np
p = 1.0 / 6.0
p_k3 = ((1.0 - p)**2) * p
assert np.isclose(p_k3, 25.0 / 216.0)
assert np.isclose(1.0 / p, 6.0)
```

---

## 4. The mistake people actually make

Believing a coin is 'due' to land heads after 5 consecutive tails (Gambler's fallacy). Memorylessness guarantees P(heads) is still p.

---

## Check yourself

1. What is the mean of a Geometric(p) distribution?
2. What does memorylessness mean in practice?

<details>
<summary>Answers</summary>

1. 1 / p.
2. Past failures provide zero information about how many more trials will be needed.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](21_The_Poisson_Distribution.md)
