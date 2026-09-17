# Lesson 11.07 — Correlation and Its Limits

> **Module 11:** Joint Distributions and Covariance · Lesson 7 of 29

---

## What you will be able to do after this lesson

- [ ] Compute Pearson correlation rho = Cov(X, Y) / (sigma_X sigma_Y) in [-1, 1].
- [ ] Show that non-linear relationships can have rho = 0.

## Prerequisites

- 11.06 Covariance.

---

## 1. The idea

**Pearson correlation** $\rho_{X,Y} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y} \in [-1, 1]$ normalizes covariance into a scale-invariant metric. Crucial limitation: $\rho$ measures only **linear** association. Perfect non-linear deterministic functions (e.g. $Y = X^2$ for symmetric $X$) have $\rho = 0$!

---

## 2. Worked example

Let $X \in \{-1, 0, 1\}$ with equal probability, and $Y = X^2 \in \{1, 0, 1\}$. $\mathbb{E}[X] = 0$. $\mathbb{E}[XY] = (-1)(1) + 0 + (1)(1) = 0$. $\text{Cov}(X, Y) = 0 \implies \rho = 0$, yet $Y$ is 100% predictable from $X$!

---

## 3. Verify it in code

```python
import numpy as np
x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
y = x**2  # Deterministic non-linear relationship
corr = np.corrcoef(x, y)[0, 1]
assert np.isclose(corr, 0.0)
```

---

## 4. The mistake people actually make

Concluding that variables are independent because their correlation is zero. Zero correlation only rules out linear association.

---

## Check yourself

1. What is the range of Pearson correlation coefficient rho?
2. Can two variables have correlation 0 and yet be completely dependent?

<details>
<summary>Answers</summary>

1. Between -1.0 and +1.0.
2. Yes, if their relationship is non-linear (e.g. Y = X^2).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](08_Correlation_Is_Not_Causation_Concretely.md)
