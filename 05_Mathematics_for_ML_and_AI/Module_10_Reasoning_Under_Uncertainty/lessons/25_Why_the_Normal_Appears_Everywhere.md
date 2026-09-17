# Lesson 10.25 — Why the Normal Appears Everywhere

> **Module 10:** Reasoning Under Uncertainty · Lesson 25 of 41

---

## What you will be able to do after this lesson

- [ ] Explain Maximum Entropy property: Gaussian maximizes entropy for fixed variance.
- [ ] Connect sums of independent disturbances to Gaussian emergence via CLT.

## Prerequisites

- 10.24 Normal Distribution.

---

## 1. The idea

The Normal distribution dominates nature and machine learning for two mathematical reasons:
1. **Central Limit Theorem**: Sums of many small independent random noise sources converge to a Gaussian.
2. **Maximum Entropy**: Among all continuous distributions with fixed mean and variance, the Gaussian has the **maximum entropy** (assumes the least additional structure).

---

## 2. Worked example

Summing 12 independent Uniform $U(-0.5, 0.5)$ variables creates a nearly indistinguishable standard normal $\mathcal{N}(0, 1)$ ($12 \times 1/12 = 1.0$).

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
# Sum of 12 uniforms has variance 1.0 and mean 0.0
x = np.sum(np.random.uniform(-0.5, 0.5, size=(10000, 12)), axis=1)
assert np.isclose(np.mean(x), 0.0, atol=0.05)
assert np.isclose(np.var(x), 1.0, atol=0.05)
```

---

## 4. The mistake people actually make

Assuming CLT applies when variables have infinite variance (e.g. Cauchy distribution sums do NOT become Gaussian).

---

## Check yourself

1. Which distribution maximizes entropy for a given mean and variance?
2. Why does sensor noise typically follow a Gaussian distribution?

<details>
<summary>Answers</summary>

1. The Normal (Gaussian) distribution.
2. Because sensor noise aggregates millions of microscopic independent thermal molecular collisions (CLT).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](26_The_Standard_Normal_and_ZScores.md)
