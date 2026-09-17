# Lesson 09.40: Variance of the Stochastic Gradient

## Learning Objectives
- Compute the variance of mini-batch gradient estimates: Var(g_B) = sigma^2 / |B|.
- Analyze how gradient noise acts as implicit regularization.

## Prerequisites
- 09.39 Stochastic Gradient Descent.

---

## 1. The Core Idea
If individual sample gradients have covariance $\boldsymbol{\Sigma}$, a mini-batch of size $B$ drawn i.i.d. has covariance:
$$\text{Cov}(\mathbf{g}_B) = \frac{\boldsymbol{\Sigma}}{B}$$
Variance scales inversely with batch size. This stochastic noise behaves like Brownian motion, enabling parameters to escape sharp local minima and settle into flat, generalizable basins.

---

## 2. Mathematical Exposition & Worked Example
Single sample variance $\sigma^2 = 16.0$.
Batch size $B = 4 \implies \text{Var}(g_B) = 16 / 4 = 4.0$. Standard error $= \sqrt{4} = 2.0$.
Batch size $B = 64 \implies \text{Var}(g_B) = 16 / 64 = 0.25$. Standard error $= \sqrt{0.25} = 0.5$.

---

## 3. Verify it in code

```python
import numpy as np
sigma2 = 16.0
var_b4 = sigma2 / 4.0
var_b64 = sigma2 / 64.0

assert var_b4 == 4.0
assert var_b64 == 0.25
assert np.sqrt(var_b64) == 0.5
```

---

## 4. The mistake people actually make
Believing larger batch sizes always yield better generalization; extremely large batch sizes eliminate exploratory gradient noise, often causing models to overfit sharp minima.

---

## Check yourself
1. How does gradient variance scale with batch size B?
2. What beneficial effect does gradient noise provide during training?

<details>
<summary>Answers</summary>

1. Inversely proportional: Var(g_B) = sigma^2 / B.
2. It helps parameters escape narrow, sharp local minima and saddle points to find flat basins.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [41_MiniBatch_Size_and_the_Gradient_Noise_Scale.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\41_MiniBatch_Size_and_the_Gradient_Noise_Scale.md)
