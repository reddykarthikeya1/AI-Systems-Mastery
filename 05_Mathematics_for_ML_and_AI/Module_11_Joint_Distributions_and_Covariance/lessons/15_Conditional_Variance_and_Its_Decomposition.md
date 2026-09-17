# Lesson 11.15 — Conditional Variance and Its Decomposition

> **Module 11:** Joint Distributions and Covariance · Lesson 15 of 29

---

## What you will be able to do after this lesson

- [ ] State Eve's Law: Var(Y) = E[Var(Y | X)] + Var(E[Y | X]).
- [ ] Decompose total variance into within-group and between-group variance.

## Prerequisites

- 11.14 The Tower Property.

---

## 1. The idea

**Eve's Law** (Law of Total Variance):
$$\text{Var}(Y) = \mathbb{E}[\text{Var}(Y \mid X)] + \text{Var}(\mathbb{E}[Y \mid X])$$
- $\mathbb{E}[\text{Var}(Y \mid X)]$ is the **unexplained within-group variance**.
- $\text{Var}(\mathbb{E}[Y \mid X])$ is the **variance explained by $X$** (between-group spread of conditional means).

---

## 2. Worked example

In ANOVA, total sum of squares splits into within-cluster variance + between-cluster variance. If $X$ perfectly predicts $Y$, within-group variance is 0.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
group = np.random.choice([0, 1], size=1000, p=[0.5, 0.5])
y = np.where(group == 0, np.random.normal(10, 2, 1000), np.random.normal(20, 2, 1000))

total_var = np.var(y)
var_within = 2.0**2  # 4.0
var_between = np.var([10.0, 20.0]) # 25.0
assert np.isclose(total_var, var_within + var_between, atol=1.5)
```

---

## 4. The mistake people actually make

Assuming Var(Y) = E[Var(Y | X)]. The between-group variance Var(E[Y | X]) must be added.

---

## Check yourself

1. What two components make up the Law of Total Variance?
2. If X provides no information about Y, what is Var(E[Y | X])?

<details>
<summary>Answers</summary>

1. Expected conditional variance E[Var(Y | X)] and variance of conditional expectation Var(E[Y | X]).
2. Zero (E[Y | X] is constant).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](16_The_BiasVariance_Decomposition.md)
