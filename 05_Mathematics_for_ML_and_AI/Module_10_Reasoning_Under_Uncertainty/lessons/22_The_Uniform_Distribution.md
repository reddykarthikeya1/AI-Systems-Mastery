# Lesson 10.22 — The Uniform Distribution

> **Module 10:** Reasoning Under Uncertainty · Lesson 22 of 41

---

## What you will be able to do after this lesson

- [ ] Define Uniform U(a, b) PDF f(x) = 1/(b-a).
- [ ] Compute mean (a+b)/2 and variance (b-a)^2 / 12.

## Prerequisites

- 10.13 Continuous PDF.

---

## 1. The idea

The continuous **Uniform distribution** $U(a, b)$ assigns constant probability density $f(x) = \frac{1}{b-a}$ over $[a, b]$. It represents maximum ignorance (maximum entropy) over a bounded interval. $\mathbb{E}[X] = \frac{a+b}{2}$, $\text{Var}(X) = \frac{(b-a)^2}{12}$.

---

## 2. Worked example

For $U(0, 10)$: mean is 5.0, variance is $10^2 / 12 = 100/12 \approx 8.333$.

---

## 3. Verify it in code

```python
import numpy as np
a, b = 0.0, 10.0
mean = (a + b) / 2.0
var = (b - a)**2 / 12.0
assert np.isclose(mean, 5.0)
assert np.isclose(var, 100.0 / 12.0)
```

---

## 4. The mistake people actually make

Assuming standard pseudorandom generators like `np.random.rand()` generate discrete integers rather than continuous floats in [0, 1).

---

## Check yourself

1. What is the variance of a standard uniform U(0, 1)?
2. What distribution maximizes entropy on a bounded interval?

<details>
<summary>Answers</summary>

1. 1/12.
2. The Uniform distribution.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](23_The_Exponential_Distribution_and_Memorylessness.md)
