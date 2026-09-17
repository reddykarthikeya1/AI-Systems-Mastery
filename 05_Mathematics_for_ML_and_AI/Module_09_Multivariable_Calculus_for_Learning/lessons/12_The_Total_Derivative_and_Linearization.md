# Lesson 09.12: The Total Derivative and Linearization

## Learning Objectives
- Construct first-order linear approximations: f(x + Delta x) approx f(x) + nabla f(x)^T Delta x.
- Compute tangent hyperplane equations.

## Prerequisites
- 09.08 The Gradient Vector.

---

## 1. The Core Idea
The **linearization** of $f: \mathbb{R}^n \to \mathbb{R}$ at $\mathbf{x}_0$ is the best affine approximation:
$$f(\mathbf{x}_0 + \Delta \mathbf{x}) \approx f(\mathbf{x}_0) + \nabla f(\mathbf{x}_0)^T \Delta \mathbf{x}$$
The graph of this affine function forms the **tangent hyperplane** to the graph of $f$ at $(\mathbf{x}_0, f(\mathbf{x}_0))$.

---

## 2. Mathematical Exposition & Worked Example
For $f(x, y) = x^2 + y^2$, at $(1, 2)$, $f(1, 2) = 5$ and $\nabla f(1, 2) = [2, 4]^T$. For step $\Delta \mathbf{x} = [0.01, -0.02]^T$:
$f_{\text{lin}} = 5 + [2, 4] \begin{bmatrix} 0.01 \\ -0.02 \end{bmatrix} = 5 + 0.02 - 0.08 = 4.94$.
Exact value: $1.01^2 + 1.98^2 = 1.0201 + 3.9204 = 4.9405$.

---

## 3. Verify it in code

```python
import numpy as np
x0 = np.array([1.0, 2.0])
dx = np.array([0.01, -0.02])
f_exact = np.sum((x0 + dx)**2)
f_lin = np.sum(x0**2) + np.dot(2.0 * x0, dx)

assert np.isclose(f_lin, 4.94)
assert np.isclose(f_exact, 4.9405)
assert np.isclose(abs(f_exact - f_lin), 0.0005)
```

---

## 4. The mistake people actually make
Using linearization for large Delta x outside the trust region where quadratic curvature dominates.

---

## Check yourself
1. What is the geometric meaning of the linearization of f: R^2 -> R?
2. What is the error bound of the linear approximation as ||Delta x|| -> 0?

<details>
<summary>Answers</summary>

1. The tangent plane at the evaluation point.
2. O(||Delta x||^2) for C^2 functions.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [13_The_Jacobian_Matrix.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\13_The_Jacobian_Matrix.md)
