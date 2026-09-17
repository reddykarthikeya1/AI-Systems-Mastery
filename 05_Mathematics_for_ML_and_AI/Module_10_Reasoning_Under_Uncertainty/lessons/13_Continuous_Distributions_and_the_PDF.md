# Lesson 10.13 — Continuous Distributions and the PDF

> **Module 10:** Reasoning Under Uncertainty · Lesson 13 of 41

---

## What you will be able to do after this lesson

- [ ] Define Probability Density Function f(x) with P(a <= X <= b) = integral_a^b f(x) dx.
- [ ] Explain why P(X = c) = 0 for any single point in continuous distributions.

## Prerequisites

- 10.11 Random Variables and Integration.

---

## 1. The idea

For continuous random variables, the probability of hitting any exact point is zero: $P(X = c) = 0$. Probability is defined over intervals via the **Probability Density Function (PDF)**: $P(a \le X \le b) = \int_a^b f(x) dx$. Density $f(x)$ can exceed 1, provided $\int_{-\infty}^\infty f(x) dx = 1$.

---

## 2. Worked example

Uniform $U(0, 0.5)$: density is $f(x) = 1/(0.5 - 0) = 2.0 > 1$. Probability over $[0, 0.25]$ is $\int_0^{0.25} 2 dx = 0.5 \le 1$.

---

## 3. Verify it in code

```python
import numpy as np
# Uniform(0, 0.5) PDF value is 2.0
f_x = 2.0
prob_interval = f_x * (0.25 - 0.0)
assert prob_interval == 0.5
assert f_x > 1.0
```

---

## 4. The mistake people actually make

Claiming that a continuous density f(x) > 1 is impossible. Only discrete PMFs are capped at 1; PDFs represent density.

---

## Check yourself

1. What is P(X = 3.14159) for a continuous random variable?
2. What must the integral of a PDF over the entire real line equal?

<details>
<summary>Answers</summary>

1. Exactly zero.
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

[Module README](../README.md) · [Next →](14_The_Cumulative_Distribution_Function.md)
