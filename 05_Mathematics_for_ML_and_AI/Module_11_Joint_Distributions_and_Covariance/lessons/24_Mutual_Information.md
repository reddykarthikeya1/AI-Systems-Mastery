# Lesson 11.24 — Mutual Information

> **Module 11:** Joint Distributions and Covariance · Lesson 24 of 29

---

## What you will be able to do after this lesson

- [ ] Compute Mutual Information I(X; Y) = D_KL(P(X, Y) || P(X) P(Y)) = H(X) - H(X | Y).
- [ ] Detect non-linear dependence that correlation misses.

## Prerequisites

- 11.04 Independence and 11.07 Correlation Limits.

---

## 1. The idea

**Mutual Information (MI)** $I(X; Y) = \sum_{x,y} P(x, y) \log \frac{P(x, y)}{P(x)P(y)}$ measures total statistical dependence (linear AND non-linear). $I(X; Y) \ge 0$, with equality if and only if $X$ and $Y$ are strictly independent. It captures non-linear relationships that correlation completely overlooks.

---

## 2. Worked example

If $X \perp Y$, $P(x, y) = P(x)P(y) \implies \log(1) = 0 \implies I(X; Y) = 0$.

---

## 3. Verify it in code

```python
import numpy as np
# Independent joint
p_x = np.array([0.5, 0.5])
p_y = np.array([0.5, 0.5])
joint_indep = np.outer(p_x, p_y)
mi_indep = np.sum(joint_indep * np.log(joint_indep / np.outer(p_x, p_y)))
assert np.isclose(mi_indep, 0.0)

# Dependent joint (perfect correlation)
joint_dep = np.array([[0.5, 0.0], [0.0, 0.5]])
# MI = H(X) = - (0.5 log 0.5 + 0.5 log 0.5) = log(2)
mi_dep = np.sum(joint_dep[joint_dep > 0] * np.log(joint_dep[joint_dep > 0] / np.outer(p_x, p_y)[joint_dep > 0]))
assert np.isclose(mi_dep, np.log(2.0))
```

---

## 4. The mistake people actually make

Using correlation for feature selection when features have strong parabolic or sinusoidal dependencies.

---

## Check yourself

1. When is Mutual Information I(X; Y) equal to zero?
2. Does Mutual Information detect non-linear dependencies?

<details>
<summary>Answers</summary>

1. If and only if X and Y are strictly independent.
2. Yes, it captures all forms of statistical dependence.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](25_Simpsons_Paradox.md)
