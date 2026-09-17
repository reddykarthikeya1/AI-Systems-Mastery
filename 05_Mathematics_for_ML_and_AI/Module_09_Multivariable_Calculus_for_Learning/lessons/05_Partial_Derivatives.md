# Lesson 09.05: Partial Derivatives

## Learning Objectives
- Define partial derivatives as limits of difference quotients holding all other variables constant.
- Compute partial derivatives of loss functions with respect to specific weights.

## Prerequisites
- 09.01 Functions of Several Variables.

---

## 1. The Core Idea
The **partial derivative** $\frac{\partial f}{\partial x_i}$ measures the instantaneous rate of change of $f$ along the coordinate axis $x_i$, holding all other variables $x_j$ ($j \ne i$) strictly fixed:
$$\frac{\partial f}{\partial x_i}(\mathbf{x}) = \lim_{h \to 0} \frac{f(\mathbf{x} + h \mathbf{e}_i) - f(\mathbf{x})}{h}$$

---

## 2. Mathematical Exposition & Worked Example
For $f(x, y) = 3x^2 y + \sin(y)$: $\frac{\partial f}{\partial x} = 6xy$ (treating $y$ as a constant). At $(x, y) = (2, 3)$, $\frac{\partial f}{\partial x} = 6(2)(3) = 36$.

---

## 3. Verify it in code

```python
import numpy as np
def f(x, y):
    return 3.0 * x**2 * y + np.sin(y)

x, y = 2.0, 3.0
h = 1e-7
num_df_dx = (f(x + h, y) - f(x, y)) / h
exact_df_dx = 6.0 * x * y

assert np.isclose(exact_df_dx, 36.0)
assert np.isclose(num_df_dx, exact_df_dx, atol=1e-4)
```

---

## 4. The mistake people actually make
Accidentally differentiating variables held constant instead of treating them as numerical constants.

---

## Check yourself
1. What is d/dx (x * y^3)?
2. In a neural network with 10 weights, how many first-order partial derivatives exist?

<details>
<summary>Answers</summary>

1. y^3.
2. 10 partial derivatives (one per parameter).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [06_HigherOrder_Partial_Derivatives.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\06_HigherOrder_Partial_Derivatives.md)
