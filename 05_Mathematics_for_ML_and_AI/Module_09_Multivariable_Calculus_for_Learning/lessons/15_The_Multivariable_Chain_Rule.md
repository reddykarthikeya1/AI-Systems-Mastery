# Lesson 09.15: The Multivariable Chain Rule

## Learning Objectives
- State the multivariable chain rule as matrix multiplication of Jacobians.
- Sum over intermediate computational paths.

## Prerequisites
- 09.13 The Jacobian Matrix.

---

## 1. The Core Idea
For composite maps $\mathbf{z} = \mathbf{g}(\mathbf{y})$ and $\mathbf{y} = \mathbf{f}(\mathbf{x})$:
$$\mathbf{J}_{\mathbf{g} \circ \mathbf{f}}(\mathbf{x}) = \mathbf{J}_\mathbf{g}(\mathbf{f}(\mathbf{x})) \mathbf{J}_\mathbf{f}(\mathbf{x})$$
For scalar $z = f(x_1(t), x_2(t), \dots, x_n(t))$: $\frac{dz}{dt} = \sum_{i=1}^n \frac{\partial f}{\partial x_i} \frac{dx_i}{dt} = \nabla f \cdot \frac{d\mathbf{x}}{dt}$.

---

## 2. Mathematical Exposition & Worked Example
Let $z = x^2 + y^2$ with $x = r \cos \theta, y = r \sin \theta$. $\frac{\partial z}{\partial r} = \frac{\partial z}{\partial x} \frac{\partial x}{\partial r} + \frac{\partial z}{\partial y} \frac{\partial y}{\partial r} = 2x(\cos \theta) + 2y(\sin \theta) = 2r \cos^2 \theta + 2r \sin^2 \theta = 2r$.

---

## 3. Verify it in code

```python
import numpy as np
r, theta = 3.0, np.pi / 4.0
x = r * np.cos(theta)
y = r * np.sin(theta)
dz_dx = 2.0 * x
dz_dy = 2.0 * y
dx_dr = np.cos(theta)
dy_dr = np.sin(theta)

dz_dr = dz_dx * dx_dr + dz_dy * dy_dr
assert np.isclose(dz_dr, 2.0 * r)
```

---

## 4. The mistake people actually make
Summing only a single path and omitting alternative parallel dependency paths in the chain rule.

---

## Check yourself
1. How do Jacobians compose under function composition?
2. If z depends on x through two paths u and v, what is dz/dx?

<details>
<summary>Answers</summary>

1. By standard matrix multiplication: J_(g o f) = J_g * J_f.
2. (dz/du)(du/dx) + (dz/dv)(dv/dx).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [16_Computational_Graphs.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\16_Computational_Graphs.md)
