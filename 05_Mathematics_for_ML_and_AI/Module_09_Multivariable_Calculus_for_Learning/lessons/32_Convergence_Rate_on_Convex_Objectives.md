# Lesson 09.32: Convergence Rate on Convex Objectives

## Learning Objectives
- State convergence rates: O(1/T) for convex L-smooth functions, O((1 - mu/L)^T) for strongly convex functions.
- Analyze sublinear versus linear (geometric) convergence.

## Prerequisites
- 09.31 Lipschitz Gradients and the Safe Step Size.

---

## 1. The Core Idea
Optimization rates under step size $\eta = 1/L$:
1. **Convex + $L$-smooth**: $f(\mathbf{x}_T) - f^* \le \frac{L \|\mathbf{x}_0 - \mathbf{x}^*\|^2}{2T} = O\left(\frac{1}{T}\right)$ (**sublinear**).
2. **$\mu$-strongly convex + $L$-smooth**: $\|\mathbf{x}_T - \mathbf{x}^*\|^2 \le \left(1 - \frac{\mu}{L}\right)^T \|\mathbf{x}_0 - \mathbf{x}^*\|^2$ (**linear/exponential** convergence).

---

## 2. Mathematical Exposition & Worked Example
With condition number $\kappa = L/\mu = 20$: factor is $1 - 1/20 = 0.95$.
After $T = 50$ iterations, error factor is $0.95^{50} \approx 0.0769$ (over $92\%$ reduction).

---

## 3. Verify it in code

```python
import numpy as np
kappa = 20.0
factor = 1.0 - 1.0 / kappa
err_50 = factor**50
assert np.isclose(err_50, 0.0769449985)
```

---

## 4. The mistake people actually make
Confusing 'linear convergence' with polynomial O(T); in numerical optimization, linear convergence means error decreases geometrically like C * r^T with r < 1.

---

## Check yourself
1. What is the convergence rate of gradient descent on a general convex L-smooth function?
2. What convergence rate is achieved under strong convexity?

<details>
<summary>Answers</summary>

1. O(1 / T).
2. Linear (geometric) rate: O((1 - mu/L)^T).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [33_Momentum.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\33_Momentum.md)
