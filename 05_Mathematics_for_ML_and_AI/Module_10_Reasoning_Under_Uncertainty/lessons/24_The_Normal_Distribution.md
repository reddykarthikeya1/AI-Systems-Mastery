# Lesson 10.24 — The Normal Distribution

> **Module 10:** Reasoning Under Uncertainty · Lesson 24 of 41

---

## What you will be able to do after this lesson

- [ ] Formulate Gaussian PDF: 1/(sigma sqrt(2 pi)) exp(-(x - mu)^2 / (2 sigma^2)).
- [ ] Verify 68-95-99.7 empirical rule.

## Prerequisites

- 10.13 Continuous PDF.

---

## 1. The idea

The **Normal (Gaussian) distribution** $\mathcal{N}(\mu, \sigma^2)$ is symmetric and bell-shaped. The **68-95-99.7 rule**:
- 68.27% within $\mu \pm 1\sigma$.
- 95.45% within $\mu \pm 2\sigma$.
- 99.73% within $\mu \pm 3\sigma$.

---

## 2. Worked example

For $\mu = 100, \sigma = 15$, 95% of observations fall between $100 \pm 30 = [70, 130]$.

---

## 3. Verify it in code

```python
import numpy as np
from math import erf
def norm_cdf(x):
    return 0.5 * (1.0 + erf(x / np.sqrt(2.0)))

# 68-95-99.7 verification
p1 = norm_cdf(1.0) - norm_cdf(-1.0)
p2 = norm_cdf(2.0) - norm_cdf(-2.0)
p3 = norm_cdf(3.0) - norm_cdf(-3.0)

assert np.isclose(p1, 0.6827, atol=1e-3)
assert np.isclose(p2, 0.9545, atol=1e-3)
assert np.isclose(p3, 0.9973, atol=1e-3)
```

---

## 4. The mistake people actually make

Assuming real-world heavy-tailed financial returns follow a Normal distribution, dramatically underestimating tail risk.

---

## Check yourself

1. What percentage of values fall within 2 standard deviations of the mean in a Gaussian?
2. What parameters define a normal distribution?

<details>
<summary>Answers</summary>

1. Approximately 95.45%.
2. The mean mu (location) and variance sigma^2 (scale).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](25_Why_the_Normal_Appears_Everywhere.md)
