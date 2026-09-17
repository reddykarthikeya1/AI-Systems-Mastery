# Lesson 09.51: Why L1 Produces Sparsity

## Learning Objectives
- Derive the soft-thresholding operator: S_lambda(w) = sign(w) max(0, |w| - lambda).
- Demonstrate exact feature selection mathematically.

## Prerequisites
- 09.50 L1 versus L2 Regularization Geometrically.

---

## 1. The Core Idea
For the 1D objective $f(w) = \frac{1}{2}(w - z)^2 + \lambda |w|$, the exact analytical minimizer is given by the **soft-thresholding operator**:
$$w^* = \mathcal{S}_\lambda(z) = \text{sign}(z) \max(0, |z| - \lambda) = \begin{cases} z - \lambda & \text{if } z > \lambda \\ 0 & \text{if } |z| \le \lambda \\ z + \lambda & \text{if } z < -\lambda \end{cases}$$
Whenever $|z| \le \lambda$, the parameter is snapped to exact zero.

---

## 2. Mathematical Exposition & Worked Example
With threshold $\lambda = 0.5$:
- For $z = 0.3$: $|0.3| \le 0.5 \implies w^* = 0.0$ (sparsified).
- For $z = 1.2$: $w^* = 1.2 - 0.5 = 0.7$.
- For $z = -0.9$: $w^* = -0.9 + 0.5 = -0.4$.

---

## 3. Verify it in code

```python
import numpy as np
def soft_threshold(z, lam):
    return np.sign(z) * np.maximum(0.0, np.abs(z) - lam)

assert soft_threshold(0.3, 0.5) == 0.0
assert np.isclose(soft_threshold(1.2, 0.5), 0.7)
assert np.isclose(soft_threshold(-0.9, 0.5), -0.4)
```

---

## 4. The mistake people actually make
Trying to differentiate |w| at w = 0 using standard derivatives (requires subgradient calculus).

---

## Check yourself
1. What is the soft-thresholding operator formula?
2. What happens to a parameter whose unregularized value satisfies |z| <= lambda?

<details>
<summary>Answers</summary>

1. sign(z) * max(0, |z| - lambda).
2. It is set to exactly 0.0.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [52_Vanishing_and_Exploding_Gradients.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\52_Vanishing_and_Exploding_Gradients.md)
