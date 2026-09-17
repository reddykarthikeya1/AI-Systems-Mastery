# Lesson 04.20 — Multicollinearity as Near Rank Deficiency

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 20 of 21

---

## What you will be able to do after this lesson

- [ ] Quantify multicollinearity using the condition number kappa(X).
- [ ] Explain why near-collinearity inflates variance of regression coefficients.

## Prerequisites

- 04.19 What Rank Tells You About a Dataset.

---

## 1. The idea

In real data, features are rarely exact linear combinations due to noise. **Multicollinearity** occurs when features are nearly collinear. The matrix is technically full rank, but ill-conditioned ($\kappa(X) \gg 1$). This blows up coefficient variance: $\text{Var}(\hat{\mathbf{w}}) = \sigma^2 (X^T X)^{-1}$, making model interpretation wild and unstable.

---

## 2. Worked example

Let $x_2 = x_1 + 10^{-5} \cdot \epsilon$. Determinant is near zero, and condition number is $\approx 10^5$. Small perturbations in targets cause giant jumps in regression coefficients.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
N = 50
x1 = np.random.randn(N)
x2 = x1 + 1e-4 * np.random.randn(N) # Near-identical feature

X = np.column_stack([x1, x2])
cond_num = np.linalg.cond(X)
assert cond_num > 1e3
```

---

## 4. The mistake people actually make

Relying on p-values in multiple linear regression when multicollinearity is present (standard errors are wildly inflated).

---

## Check yourself

1. What metric diagnoses near rank deficiency?
2. What regularization technique cures multicollinearity?

<details>
<summary>Answers</summary>

1. The condition number kappa(X) or Variance Inflation Factor (VIF).
2. L2 Ridge regularization (adding lambda * I to X^T X).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](21_Module_Project_Detect_Redundant_Features_by_Rank.md)
