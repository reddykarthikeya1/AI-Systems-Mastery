# Lesson 12.05 — The Standard Error

> **Module 12:** Statistical Estimation from Samples · Lesson 5 of 22

---

## What you will be able to do after this lesson

- [ ] Compute standard error of the mean SE = s / sqrt(n).
- [ ] Explain why doubling precision requires quadrupling the sample size.

## Prerequisites

- 12.04 The Sampling Distribution.

---

## 1. The idea

The **Standard Error (SE)** is the standard deviation of the sampling distribution: $\text{SE}(\bar{X}) = \frac{\sigma}{\sqrt{n}}$. Because of the square root $\sqrt{n}$, reducing estimation error by half requires $4\times$ as much data.

---

## 2. Worked example

Sample has standard deviation $s = 10$, $n = 100$. $\text{SE} = 10 / \sqrt{100} = 1.0$. To get $\text{SE} = 0.5$, $n$ must increase to $400$.

---

## 3. Verify it in code

```python
import numpy as np
s = 10.0
n1 = 100
se1 = s / np.sqrt(n1)
assert np.isclose(se1, 1.0)
n2 = 400
se2 = s / np.sqrt(n2)
assert np.isclose(se2, 0.5)
```

---

## 4. The mistake people actually make

Reporting sample standard deviation s (spread of individuals) instead of standard error s/sqrt(n) (precision of mean).

---

## Check yourself

1. How much larger must sample size n be to reduce standard error by a factor of 10?
2. What does standard error measure?

<details>
<summary>Answers</summary>

1. 100 times larger (10^2).
2. The variability and precision of an estimator across repeated samples.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](06_The_Method_of_Moments.md)
