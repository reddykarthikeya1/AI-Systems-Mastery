# Lesson 11.08 — Correlation Is Not Causation, Concretely

> **Module 11:** Joint Distributions and Covariance · Lesson 8 of 29

---

## What you will be able to do after this lesson

- [ ] Identify confounding variables that induce spurious correlation.
- [ ] Explain why observational regression coefficients fail to predict intervention effects.

## Prerequisites

- 11.07 Correlation and Its Limits.

---

## 1. The idea

Statistical correlation between $X$ and $Y$ can arise from three distinct causal structures:
1. $X \to Y$ ($X$ causes $Y$).
2. $Y \to X$ ($Y$ causes $X$).
3. $X \leftarrow Z \to Y$ ($Z$ is a **confounder** causing both).
Observational models cannot distinguish these without randomized controlled trials or causal graphs.

---

## 2. Worked example

Ice cream sales ($X$) and drownings ($Y$) have high correlation ($\rho = 0.9$) because Summer heat ($Z$) causes both. Intervening to ban ice cream does not save lives.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
N = 1000
temp = np.random.uniform(20, 35, N) # Confounder Z
ice_cream = 10 * temp + np.random.randn(N) * 5
drownings = 2 * temp + np.random.randn(N) * 2

# High spurious correlation
corr = np.corrcoef(ice_cream, drownings)[0, 1]
assert corr > 0.8
```

---

## 4. The mistake people actually make

Interpreting positive model feature weights as causal levers in policy decisions without controlling for confounders.

---

## Check yourself

1. What third variable creates spurious correlation between two unrelated variables?
2. What gold-standard experimental design breaks confounding?

<details>
<summary>Answers</summary>

1. A common cause (confounder).
2. Randomized controlled trials (A/B testing).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](09_The_Covariance_Matrix.md)
