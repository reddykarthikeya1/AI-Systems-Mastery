# Lesson 10.34 — Markov's and Chebyshev's Inequalities

> **Module 10:** Reasoning Under Uncertainty · Lesson 34 of 41

---

## What you will be able to do after this lesson

- [ ] Apply Markov's inequality P(X >= a) <= E[X] / a for non-negative X.
- [ ] Apply Chebyshev's inequality P(|X - mu| >= k sigma) <= 1 / k^2.

## Prerequisites

- 10.15 Expected Value and 10.17 Variance.

---

## 1. The idea

Fundamental concentration inequalities:
- **Markov's Inequality**: For non-negative $X \ge 0$ and $a > 0$: $P(X \ge a) \le \frac{\mathbb{E}[X]}{a}$.
- **Chebyshev's Inequality**: For any distribution with finite variance: $P(|X - \mu| \ge k\sigma) \le \frac{1}{k^2}$.
These provide rigorous distribution-free bounds on tail probabilities.

---

## 2. Worked example

For any distribution whatsoever, the probability of deviating by more than $3\sigma$ from the mean is at most $1/3^2 = 1/9 \approx 11.1\%$.

---

## 3. Verify it in code

```python
import numpy as np
k = 3.0
chebyshev_bound = 1.0 / (k**2)
assert np.isclose(chebyshev_bound, 1.0 / 9.0)
```

---

## 4. The mistake people actually make

Applying Markov's inequality to variables that can take negative values.

---

## Check yourself

1. What condition must X satisfy to apply Markov's inequality?
2. According to Chebyshev, what is the maximum probability of deviating by >= 2 sigma?

<details>
<summary>Answers</summary>

1. X must be non-negative: X >= 0.
2. At most 1 / 2^2 = 25%.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](35_Concentration_and_Hoeffdings_Inequality.md)
