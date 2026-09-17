# Lesson 11.14 — The Tower Property

> **Module 11:** Joint Distributions and Covariance · Lesson 14 of 29

---

## What you will be able to do after this lesson

- [ ] State the Tower Property (Law of Total Expectation): E[E[Y | X]] = E[Y].
- [ ] Simplify complex expectations by conditioning.

## Prerequisites

- 11.13 Conditional Expectation.

---

## 1. The idea

The **Tower Property** (Law of Iterated Expectations):
$$\mathbb{E}[\mathbb{E}[Y \mid X]] = \mathbb{E}[Y]$$
Taking the average over all subgroups recovers the grand overall population average. This allows solving intractable expectations by conditioning on an intermediate variable.

---

## 2. Worked example

Let group $X=0$ have mean 10 (size 60%) and group $X=1$ have mean 20 (size 40%). Grand mean: $\mathbb{E}[Y] = 0.6(10) + 0.4(20) = 6 + 8 = 14$.

---

## 3. Verify it in code

```python
import numpy as np
e_y_x0 = 10.0
e_y_x1 = 20.0
p_x0 = 0.6
p_x1 = 0.4
grand_mean = p_x0 * e_y_x0 + p_x1 * e_y_x1
assert np.isclose(grand_mean, 14.0)
```

---

## 4. The mistake people actually make

Averaging subgroup means without weighting by subgroup population sizes.

---

## Check yourself

1. What is E[E[Y | X]] equal to?
2. Why is the Tower Property called iterated expectations?

<details>
<summary>Answers</summary>

1. E[Y].
2. Because it evaluates expectations in stages: first taking expectation over Y given X, then over X.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](15_Conditional_Variance_and_Its_Decomposition.md)
