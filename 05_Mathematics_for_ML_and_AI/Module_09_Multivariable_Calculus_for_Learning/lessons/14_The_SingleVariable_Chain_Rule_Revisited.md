# Lesson 09.14: The Single-Variable Chain Rule Revisited

## Learning Objectives
- Review the 1D chain rule d/dx (f(g(x))) = f'(g(x)) g'(x).
- Formulate chain rule as multiplication of local linear sensitivities.

## Prerequisites
- 09.05 Partial Derivatives.

---

## 1. The Core Idea
In composition $y = f(u)$ where $u = g(x)$, the instantaneous rate of change of $y$ with respect to $x$ is the product of rates:
$$\frac{dy}{dx} = \frac{dy}{du} \frac{du}{dx}$$
This fundamental multiplicative rule underpins all automatic differentiation and backpropagation algorithms.

---

## 2. Mathematical Exposition & Worked Example
Let $y = \sigma(u) = \frac{1}{1 + e^{-u}}$ and $u = w x + b$. Then $\frac{dy}{du} = \sigma(u)(1 - \sigma(u))$ and $\frac{du}{dw} = x$.
Thus $\frac{dy}{dw} = \sigma(u)(1 - \sigma(u)) x$.

---

## 3. Verify it in code

```python
import numpy as np
w, x, b = 2.0, 1.5, -1.0
u = w * x + b  # 2.0
sig = 1.0 / (1.0 + np.exp(-u))
dy_du = sig * (1.0 - sig)
du_dw = x
dy_dw = dy_du * du_dw

# Numerical finite difference check
h = 1e-7
u_h = (w + h) * x + b
sig_h = 1.0 / (1.0 + np.exp(-u_h))
num_dy_dw = (sig_h - sig) / h
assert np.isclose(dy_dw, num_dy_dw, atol=1e-5)
```

---

## 4. The mistake people actually make
Forgetting to evaluate the outer derivative at the intermediate activation value g(x).

---

## Check yourself
1. What is d/dx sin(x^2)?
2. Why is the chain rule multiplicative?

<details>
<summary>Answers</summary>

1. 2x cos(x^2).
2. Because linear scaling factors compound by multiplication: (dy/du) * (du/dx).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [15_The_Multivariable_Chain_Rule.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\15_The_Multivariable_Chain_Rule.md)
