# Lesson 10.28 — The Beta Distribution

> **Module 10:** Reasoning Under Uncertainty · Lesson 28 of 41

---

## What you will be able to do after this lesson

- [ ] Define Beta(alpha, beta) on support [0, 1]: f(x) = x^(alpha-1) (1-x)^(beta-1) / B(alpha, beta).
- [ ] Interpret alpha and beta as pseudo-counts in Bayesian learning.

## Prerequisites

- 10.13 Continuous PDF.

---

## 1. The idea

The **Beta distribution** is the canonical continuous distribution over probabilities $p \in [0, 1]$. Its parameters $\alpha, \beta > 0$ behave as pseudo-counts: $\alpha - 1$ prior successes and $\beta - 1$ prior failures. $\mathbb{E}[X] = \frac{\alpha}{\alpha + \beta}$.

---

## 2. Worked example

$\text{Beta}(1, 1)$ is the uniform distribution $U(0, 1)$. $\text{Beta}(5, 5)$ is symmetric around $0.5$. $\text{Beta}(10, 2)$ concentrates near $10/12 \approx 0.833$.

---

## 3. Verify it in code

```python
import numpy as np
alpha, beta = 10.0, 2.0
mean = alpha / (alpha + beta)
assert np.isclose(mean, 10.0 / 12.0)
```

---

## 4. The mistake people actually make

Setting alpha or beta to 0, which violates parameter support (alpha, beta > 0).

---

## Check yourself

1. What is the support domain of the Beta distribution?
2. What does Beta(1, 1) simplify to?

<details>
<summary>Answers</summary>

1. The interval [0, 1].
2. The standard Uniform distribution U(0, 1).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](29_The_Gamma_Distribution.md)
