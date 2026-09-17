# Lesson 09.20: The Hessian Matrix

## Learning Objectives
- Define the Hessian matrix H of second partial derivatives.
- Explain why the Hessian is symmetric for C^2 objective functions.

## Prerequisites
- 09.07 Clairaut's Theorem on Mixed Partials.

---

## 1. The Core Idea
The **Hessian matrix** $\mathbf{H} \in \mathbb{R}^{n \times n}$ of $f: \mathbb{R}^n \to \mathbb{R}$ contains all pairwise second partial derivatives:
$$H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}, \quad \mathbf{H} = \nabla^2 f(\mathbf{x})$$
By Clairaut's theorem, $\mathbf{H}$ is symmetric ($\mathbf{H} = \mathbf{H}^T$) whenever second derivatives are continuous.

---

## 2. Mathematical Exposition & Worked Example
For $f(x, y) = x^3 - 3xy + 2y^2$:
$\nabla f = [3x^2 - 3y, -3x + 4y]^T$.
$f_{xx} = 6x$, $f_{xy} = -3$, $f_{yx} = -3$, $f_{yy} = 4$.
At $(x, y) = (2, 1)$: $\mathbf{H} = \begin{bmatrix} 12 & -3 \\ -3 & 4 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
def hessian(x, y):
    return np.array([[6.0 * x, -3.0], [-3.0, 4.0]])

H = hessian(2.0, 1.0)
assert np.allclose(H, np.array([[12.0, -3.0], [-3.0, 4.0]]))
assert np.allclose(H, H.T)  # Symmetry
```

---

## 4. The mistake people actually make
Attempting to instantiate full D x D Hessians for billion-parameter models; memory footprint scales as O(D^2) (petabytes).

---

## Check yourself
1. What is the memory size of a float32 Hessian for a 1-billion parameter LLM?
2. Is the Hessian of any smooth function always symmetric?

<details>
<summary>Answers</summary>

1. 4 bytes * 10^18 = 4 Exabytes (infeasible to materialize).
2. Yes, by Clairaut's Theorem on continuous mixed partials.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [21_SecondOrder_Taylor_Expansion.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\21_SecondOrder_Taylor_Expansion.md)
