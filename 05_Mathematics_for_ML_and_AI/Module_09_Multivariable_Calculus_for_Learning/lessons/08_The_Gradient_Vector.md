# Lesson 09.08: The Gradient Vector

## Learning Objectives
- Define the gradient vector nabla f as the column vector of all first partial derivatives.
- Compute gradients analytically and numerically.

## Prerequisites
- 09.05 Partial Derivatives.

---

## 1. The Core Idea
The **gradient** of a scalar field $f: \mathbb{R}^n \to \mathbb{R}$ is the vector of all its partial derivatives:
$$\nabla f(\mathbf{x}) = \begin{bmatrix} \frac{\partial f}{\partial x_1} & \frac{\partial f}{\partial x_2} & \cdots & \frac{\partial f}{\partial x_n} \end{bmatrix}^T \in \mathbb{R}^n$$
It encapsulates the complete linear sensitivity of $f$ in every coordinate direction.

---

## 2. Mathematical Exposition & Worked Example
For $f(x_1, x_2) = x_1^2 + 3 x_1 x_2 + 5 x_2^2$: $\nabla f = [2x_1 + 3x_2, 3x_1 + 10x_2]^T$. At $(1, 2)$, $\nabla f(1, 2) = [2(1) + 3(2), 3(1) + 10(2)]^T = [8, 23]^T$.

---

## 3. Verify it in code

```python
import numpy as np
def grad_f(x):
    return np.array([2.0*x[0] + 3.0*x[1], 3.0*x[0] + 10.0*x[1]])

pt = np.array([1.0, 2.0])
g = grad_f(pt)
assert np.allclose(g, np.array([8.0, 23.0]))
```

---

## 4. The mistake people actually make
Treating the gradient as a scalar or forgetting to evaluate partial derivatives at the specific operating point.

---

## Check yourself
1. If f: R^n -> R, what is the dimensionality of nabla f?
2. What is nabla f for f(x) = (1/2) x^T A x with symmetric A?

<details>
<summary>Answers</summary>

1. R^n (same dimension as the parameter space).
2. nabla f = A x.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [09_Why_the_Gradient_Points_Uphill.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\09_Why_the_Gradient_Points_Uphill.md)
