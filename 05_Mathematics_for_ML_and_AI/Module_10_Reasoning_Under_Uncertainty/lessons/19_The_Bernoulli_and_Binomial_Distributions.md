# Lesson 10.19 — The Bernoulli and Binomial Distributions

> **Module 10:** Reasoning Under Uncertainty · Lesson 19 of 41

---

## What you will be able to do after this lesson

- [ ] Formulate Bernoulli(p) and Binomial(n, p): P(k) = C(n, k) p^k (1-p)^(n-k).
- [ ] Verify mean E[X] = n p and variance Var(X) = n p (1-p).

## Prerequisites

- 10.04 Combinations.

---

## 1. The idea

- **Bernoulli($p$)**: single coin toss ($X \in \{0, 1\}$). $\mathbb{E}[X] = p$, $\text{Var}(X) = p(1-p)$.
- **Binomial($n, p$)**: sum of $n$ independent $\text{Bernoulli}(p)$ trials. $P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$. By linearity of expectation, $\mathbb{E}[X] = np$, $\text{Var}(X) = np(1-p)$.

---

## 2. Worked example

10 coin flips with $p = 0.5$: expected heads $= 10(0.5) = 5$. Variance $= 10(0.5)(0.5) = 2.5$. Standard deviation $\approx 1.58$.

---

## 3. Verify it in code

```python
import numpy as np
from math import comb
n, p = 10, 0.5
k = 5
prob_5 = comb(n, k) * (p**k) * ((1 - p)**(n - k))
assert np.isclose(prob_5, 252.0 / 1024.0)
assert np.isclose(n * p, 5.0)
assert np.isclose(n * p * (1 - p), 2.5)
```

---

## 4. The mistake people actually make

Using Binomial distribution when trials are dependent (e.g. sampling without replacement).

---

## Check yourself

1. What is the variance of a Bernoulli(p) trial?
2. What distribution describes sampling with replacement vs without replacement?

<details>
<summary>Answers</summary>

1. p(1 - p).
2. With replacement is Binomial; without replacement is Hypergeometric.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](20_The_Geometric_and_Negative_Binomial_Distributions.md)
