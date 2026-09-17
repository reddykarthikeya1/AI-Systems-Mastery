# Lesson 10.14 — The Cumulative Distribution Function

> **Module 10:** Reasoning Under Uncertainty · Lesson 14 of 41

---

## What you will be able to do after this lesson

- [ ] Define CDF F(x) = P(X <= x).
- [ ] Compute interval probabilities via F(b) - F(a).

## Prerequisites

- 10.12 PMF and 10.13 PDF.

---

## 1. The idea

The **Cumulative Distribution Function (CDF)** $F(x) = P(X \le x)$ applies universally to both discrete and continuous variables. Properties:
1. $0 \le F(x) \le 1$.
2. Monotonically non-decreasing ($x_1 < x_2 \implies F(x_1) \le F(x_2)$).
3. $\lim_{x \to -\infty} F(x) = 0$ and $\lim_{x \to \infty} F(x) = 1$.
4. $P(a < X \le b) = F(b) - F(a)$.

---

## 2. Worked example

For exponential distribution $F(x) = 1 - e^{-\lambda x}$. With $\lambda = 1$, $P(1 < X \le 2) = F(2) - F(1) = (1 - e^{-2}) - (1 - e^{-1}) = e^{-1} - e^{-2} \approx 0.3679 - 0.1353 = 0.2326$.

---

## 3. Verify it in code

```python
import numpy as np
lam = 1.0
F = lambda x: 1.0 - np.exp(-lam * x)
p_interval = F(2.0) - F(1.0)
assert np.isclose(p_interval, np.exp(-1.0) - np.exp(-2.0))
assert 0.0 <= F(1.0) <= F(2.0) <= 1.0
```

---

## 4. The mistake people actually make

Taking derivative of discrete CDFs. Discrete CDFs are step functions; their derivatives are Dirac delta spikes.

---

## Check yourself

1. Can a CDF ever decrease as x increases?
2. What is F(infinity) for any valid random variable?

<details>
<summary>Answers</summary>

1. Never; CDFs are monotonically non-decreasing.
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

[Module README](../README.md) · [Next →](15_Expected_Value.md)
