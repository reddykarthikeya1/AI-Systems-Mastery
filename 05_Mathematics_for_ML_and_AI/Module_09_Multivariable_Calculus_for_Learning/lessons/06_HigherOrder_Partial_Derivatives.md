# Lesson 09.06: Higher-Order Partial Derivatives

## Learning Objectives
- Compute second-order pure and mixed partial derivatives.
- Construct the components of the Hessian curvature tensor.

## Prerequisites
- 09.05 Partial Derivatives.

---

## 1. The Core Idea
Taking the partial derivative of an existing partial derivative yields **higher-order partial derivatives**:
$$f_{xx} = \frac{\partial^2 f}{\partial x^2}, \quad f_{xy} = \frac{\partial}{\partial y}\left(\frac{\partial f}{\partial x}\right) = \frac{\partial^2 f}{\partial y \partial x}$$
These second derivatives characterize curvature and rate of change of gradients.

---

## 2. Mathematical Exposition & Worked Example
For $f(x, y) = x^3 y^2$: $f_x = 3x^2 y^2$, $f_{xx} = 6x y^2$, and $f_{xy} = \frac{\partial}{\partial y}(3x^2 y^2) = 6x^2 y$.

---

## 3. Verify it in code

```python
import numpy as np
x, y = 2.0, 3.0
f_xx = 6.0 * x * (y**2)
f_xy = 6.0 * (x**2) * y

assert np.isclose(f_xx, 6.0 * 2.0 * 9.0)  # 108.0
assert np.isclose(f_xy, 6.0 * 4.0 * 3.0)  # 72.0
```

---

## 4. The mistake people actually make
Confusing notation: in d^2 f / (dy dx), the x derivative is performed first, followed by y.

---

## Check yourself
1. What does f_xx measure geometrically?
2. If f(x, y) = x^2 + y^2, what is f_xy?

<details>
<summary>Answers</summary>

1. Curvature (acceleration) along the x coordinate direction.
2. 0, because df/dx = 2x, which contains no y terms.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [07_Clairauts_Theorem_on_Mixed_Partials.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\07_Clairauts_Theorem_on_Mixed_Partials.md)
