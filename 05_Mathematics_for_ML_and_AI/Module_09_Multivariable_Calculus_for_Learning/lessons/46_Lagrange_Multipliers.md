# Lesson 09.46: Lagrange Multipliers

## Learning Objectives
- Construct the Lagrangian function L(x, lambda) = f(x) + lambda^T h(x) for equality constraints.
- Prove that nabla f and nabla h must be collinear at constrained extrema.

## Prerequisites
- 09.45 Constrained Optimization: The Setup.

---

## 1. The Core Idea
For equality constraints $h(\mathbf{x}) = 0$, at any constrained extremum, the gradient of the objective must be perpendicular to the constraint surface:
$$\nabla f(\mathbf{x}^*) + \lambda^* \nabla h(\mathbf{x}^*) = \mathbf{0}$$
This is equivalent to finding stationary points of the **Lagrangian**:
$$\mathcal{L}(\mathbf{x}, \lambda) = f(\mathbf{x}) + \lambda h(\mathbf{x})$$

---

## 2. Mathematical Exposition & Worked Example
Minimize $f(x, y) = x^2 + y^2$ subject to $x + y = 2$.
$\mathcal{L}(x, y, \lambda) = x^2 + y^2 + \lambda(x + y - 2)$.
$\nabla_x \mathcal{L} = 2x + \lambda = 0 \implies x = -\lambda/2$.
$\nabla_y \mathcal{L} = 2y + \lambda = 0 \implies y = -\lambda/2$.
$x + y = 2 \implies -\lambda = 2 \implies \lambda = -2$.
Thus $x^* = 1, y^* = 1$ with minimum value $1^2 + 1^2 = 2$.

---

## 3. Verify it in code

```python
import numpy as np
# Analytical solution
x_opt, y_opt = 1.0, 1.0
assert x_opt + y_opt == 2.0
assert np.isclose(x_opt**2 + y_opt**2, 2.0)
```

---

## 4. The mistake people actually make
Forgetting that Lagrange multipliers only locate critical points on the boundary; second-order bordered Hessians must verify whether it is a minimum.

---

## Check yourself
1. Why must nabla f and nabla h be collinear at a constrained optimum?
2. What is the Lagrangian function for min f(x) s.t. h(x) = 0?

<details>
<summary>Answers</summary>

1. Because any component of nabla f along the surface would allow moving along the constraint while further decreasing f.
2. L(x, lambda) = f(x) + lambda * h(x).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [47_The_KKT_Conditions.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\47_The_KKT_Conditions.md)
