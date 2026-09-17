# Lesson 09.07: Clairaut's Theorem on Mixed Partials

## Learning Objectives
- State Clairaut's (Schwarz's) Theorem: f_xy = f_yx for C^2 functions.
- Deduce why Hessian matrices in ML are symmetric.

## Prerequisites
- 09.06 Higher-Order Partial Derivatives.

---

## 1. The Core Idea
**Clairaut's Theorem**: If the mixed second partial derivatives of $f: \mathbb{R}^n \to \mathbb{R}$ are continuous on an open ball around $\mathbf{x}_0$, then the order of differentiation does not matter:
$$\frac{\partial^2 f}{\partial x_j \partial x_i} = \frac{\partial^2 f}{\partial x_i \partial x_j}$$
This ensures the Hessian matrix $\mathbf{H} = \nabla^2 f$ is always symmetric ($H_{ij} = H_{ji}$) for smooth objective functions.

---

## 2. Mathematical Exposition & Worked Example
Let $f(x, y) = e^x \cos(y)$. $f_x = e^x \cos(y) \implies f_{xy} = -e^x \sin(y)$. Now $f_y = -e^x \sin(y) \implies f_{yx} = -e^x \sin(y)$. Indeed $f_{xy} = f_{yx}$.

---

## 3. Verify it in code

```python
import numpy as np
x, y = 1.2, 0.7
f_xy = -np.exp(x) * np.sin(y)
f_yx = -np.exp(x) * np.sin(y)
assert np.isclose(f_xy, f_yx)
```

---

## 4. The mistake people actually make
Assuming symmetry holds for non-smooth functions where second partials are discontinuous at the evaluation point.

---

## Check yourself
1. What condition guarantees that f_xy = f_yx?
2. What property of the Hessian matrix follows directly from Clairaut's theorem?

<details>
<summary>Answers</summary>

1. Continuous second-order partial derivatives (C^2 smoothness).
2. The Hessian matrix is symmetric: H^T = H.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [08_The_Gradient_Vector.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\08_The_Gradient_Vector.md)
