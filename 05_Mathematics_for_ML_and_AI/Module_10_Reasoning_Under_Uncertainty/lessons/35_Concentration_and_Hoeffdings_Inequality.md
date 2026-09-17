# Lesson 10.35 — Concentration and Hoeffding's Inequality

> **Module 10:** Reasoning Under Uncertainty · Lesson 35 of 41

---

## What you will be able to do after this lesson

- [ ] State Hoeffding's inequality for bounded independent variables.
- [ ] Derive sample complexity bounds in PAC (Probably Approximately Correct) learning.

## Prerequisites

- 10.34 Markov and Chebyshev Inequalities.

---

## 1. The idea

For independent bounded random variables $X_i \in [a, b]$, **Hoeffding's Inequality** establishes exponential tail decay:
$$P(|\bar{X} - \mathbb{E}[\bar{X}]| \ge \epsilon) \le 2 \exp\left(-\frac{2 n \epsilon^2}{(b - a)^2}\right)$$
This proves that empirical averages concentrate exponentially fast around their true mean, underpinning PAC learning and generalization bounds in statistical learning theory.

---

## 2. Worked example

For bounded error in $[0, 1]$, $n = 1000$ and $\epsilon = 0.1$: $P(|\bar{X} - \mu| \ge 0.1) \le 2 \exp(-2(1000)(0.01)) = 2 e^{-20} \approx 4 \times 10^{-9}$.

---

## 3. Verify it in code

```python
import numpy as np
n = 1000
eps = 0.1
bound = 2.0 * np.exp(-2.0 * n * (eps**2))
assert bound < 1e-8
```

---

## 4. The mistake people actually make

Applying Hoeffding's inequality to heavy-tailed or dependent time-series observations.

---

## Check yourself

1. How fast does Hoeffding's bound decay with sample size n?
2. What field of machine learning theory relies heavily on Hoeffding's inequality?

<details>
<summary>Answers</summary>

1. Exponentially fast: O(exp(-c * n)).
2. PAC (Probably Approximately Correct) learning theory.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](36_The_Law_of_Large_Numbers.md)
