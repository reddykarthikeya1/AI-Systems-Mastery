# Lesson 10.21 — The Poisson Distribution

> **Module 10:** Reasoning Under Uncertainty · Lesson 21 of 41

---

## What you will be able to do after this lesson

- [ ] Formulate Poisson(lambda) PMF: P(k) = lambda^k e^(-lambda) / k!.
- [ ] Derive Poisson as the limit of Binomial(n, p) with n -> inf, p -> 0, np = lambda.

## Prerequisites

- 10.19 Binomial Distributions.

---

## 1. The idea

The **Poisson distribution** models count of rare independent events occurring at constant average rate $\lambda$:
$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$
Key fingerprint: **mean equals variance**: $\mathbb{E}[X] = \text{Var}(X) = \lambda$.

---

## 2. Worked example

Website receives $\lambda = 3$ requests/sec. Probability of exactly 0 requests: $3^0 e^{-3} / 0! = e^{-3} \approx 0.0498$ (4.98%).

---

## 3. Verify it in code

```python
import numpy as np
from math import factorial
lam = 3.0
p_0 = (lam**0 * np.exp(-lam)) / factorial(0)
assert np.isclose(p_0, np.exp(-3.0))
# Sum of probabilities over k=0..20
probs = [(lam**k * np.exp(-lam)) / factorial(k) for k in range(25)]
assert np.isclose(np.sum(probs), 1.0)
```

---

## 4. The mistake people actually make

Fitting a Poisson model to overdispersed data where empirical variance significantly exceeds the mean (Negative Binomial is required).

---

## Check yourself

1. What unique property characterizes the mean and variance of a Poisson distribution?
2. Under what conditions does Binomial approach Poisson?

<details>
<summary>Answers</summary>

1. They are identical: E[X] = Var(X) = lambda.
2. When n is large, p is small, and np = lambda is constant (Law of Rare Events).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](22_The_Uniform_Distribution.md)
