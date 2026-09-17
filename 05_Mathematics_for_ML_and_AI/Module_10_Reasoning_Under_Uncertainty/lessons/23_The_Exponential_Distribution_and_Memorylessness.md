# Lesson 10.23 — The Exponential Distribution and Memorylessness

> **Module 10:** Reasoning Under Uncertainty · Lesson 23 of 41

---

## What you will be able to do after this lesson

- [ ] Define Exponential(lambda) PDF f(x) = lambda e^(-lambda x).
- [ ] Verify memorylessness P(X > s + t | X > s) = P(X > t) in NumPy.

## Prerequisites

- 10.13 Continuous PDF and 10.20 Geometric Distribution.

---

## 1. The idea

The **Exponential distribution** models waiting time between Poisson events. $\mathbb{E}[X] = 1/\lambda$, $\text{Var}(X) = 1/\lambda^2$. It is the **only continuous distribution with memorylessness**: $\forall s, t > 0$, $P(X > s + t \mid X > s) = P(X > t)$.

---

## 2. Worked example

Server time between crashes with $\lambda = 0.5$ per day. Mean $= 1/0.5 = 2$ days. Given server survived 3 days, probability of surviving another day is $P(X > 1) = e^{-0.5} \approx 0.606$.

---

## 3. Verify it in code

```python
import numpy as np
lam = 0.5
# Survival function S(t) = P(X > t) = exp(-lam * t)
s_t = lambda t: np.exp(-lam * t)
# Memorylessness: S(s + t) / S(s) == S(t)
s, t = 3.0, 1.0
assert np.isclose(s_t(s + t) / s_t(s), s_t(t))
```

---

## 4. The mistake people actually make

Using exponential distribution for component lifespans subject to mechanical wear and tear (Weibull is required).

---

## Check yourself

1. What is the mean of Exponential(lambda)?
2. What is the only continuous memoryless distribution?

<details>
<summary>Answers</summary>

1. 1 / lambda.
2. The Exponential distribution.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](24_The_Normal_Distribution.md)
