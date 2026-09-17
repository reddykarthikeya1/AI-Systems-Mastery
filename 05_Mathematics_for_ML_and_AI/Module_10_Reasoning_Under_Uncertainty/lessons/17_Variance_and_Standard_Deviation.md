# Lesson 10.17 — Variance and Standard Deviation

> **Module 10:** Reasoning Under Uncertainty · Lesson 17 of 41

---

## What you will be able to do after this lesson

- [ ] Compute Var(X) = E[(X - mu)^2] = E[X^2] - (E[X])^2.
- [ ] Verify scaling rule Var(c X) = c^2 Var(X).

## Prerequisites

- 10.15 Expected Value.

---

## 1. The idea

**Variance** measures spread around the mean: $\text{Var}(X) = \mathbb{E}[(X - \mu)^2] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2$. **Standard deviation** $\sigma = \sqrt{\text{Var}(X)}$ restores the original units of measurement. Scaling rule: $\text{Var}(cX + d) = c^2 \text{Var}(X)$.

---

## 2. Worked example

Fair die: $\mathbb{E}[X] = 3.5$. $\mathbb{E}[X^2] = \frac{1}{6}(1+4+9+16+25+36) = 91/6 \approx 15.167$. $\text{Var}(X) = 91/6 - (7/2)^2 = 91/6 - 49/4 = 35/12 \approx 2.917$.

---

## 3. Verify it in code

```python
import numpy as np
faces = np.arange(1, 7)
probs = np.full(6, 1.0 / 6.0)
e_x = np.sum(faces * probs)
e_x2 = np.sum((faces**2) * probs)
var_x = e_x2 - e_x**2
assert np.isclose(var_x, 35.0 / 12.0)
# Var(2X) == 4 Var(X)
assert np.isclose(np.sum(((2 * faces)**2) * probs) - (2 * e_x)**2, 4.0 * var_x)
```

---

## 4. The mistake people actually make

Claiming Var(c X) = c Var(X). Scaling factor c must be squared: c^2.

---

## Check yourself

1. What is Var(c X + d) in terms of Var(X)?
2. Can variance ever be negative?

<details>
<summary>Answers</summary>

1. c^2 Var(X) (additive constants do not affect spread).
2. Never; variance is an expected square, so Var(X) >= 0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](18_Moments_and_Moment_Generating_Functions.md)
