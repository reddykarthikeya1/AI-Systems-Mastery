# Lesson 09.21: Second-Order Taylor Expansion

## Learning Objectives
- Formulate second-order multivariable Taylor expansion: f(x + Delta x) approx f(x) + g^T Delta x + (1/2) Delta x^T H Delta x.
- Model local curvature quadratically.

## Prerequisites
- 09.20 The Hessian Matrix.

---

## 1. The Core Idea
The **second-order Taylor approximation** of a smooth function $f$ near $\mathbf{x}_0$ incorporates both gradient $\mathbf{g}$ and Hessian $\mathbf{H}$:
$$f(\mathbf{x}_0 + \mathbf{h}) \approx f(\mathbf{x}_0) + \nabla f(\mathbf{x}_0)^T \mathbf{h} + \frac{1}{2} \mathbf{h}^T \nabla^2 f(\mathbf{x}_0) \mathbf{h}$$
The quadratic term $\frac{1}{2}\mathbf{h}^T \mathbf{H} \mathbf{h}$ captures the curvature (bend) of the surface.

---

## 2. Mathematical Exposition & Worked Example
Let $f(x, y) = \cos(x) + \cos(y)$. At $(0, 0)$: $f(0, 0) = 2$, $\mathbf{g} = [0, 0]^T$, $\mathbf{H} = \begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$.
Taylor expansion: $f(\mathbf{h}) \approx 2 + 0 + \frac{1}{2} [h_1, h_2] \begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} h_1 \\ h_2 \end{bmatrix} = 2 - \frac{1}{2}(h_1^2 + h_2^2)$.

---

## 3. Verify it in code

```python
import numpy as np
h = np.array([0.1, 0.2])
exact = np.cos(h[0]) + np.cos(h[1])
approx = 2.0 - 0.5 * (h[0]**2 + h[1]**2)
assert np.isclose(approx, 2.0 - 0.5 * 0.05)  # 1.975
assert np.isclose(exact, approx, atol=1e-3)
```

---

## 4. The mistake people actually make
Omission of the 1/2 factor before the quadratic Hessian term.

---

## Check yourself
1. What role does the Hessian play in the Taylor expansion?
2. What happens to the linear term at a critical point?

<details>
<summary>Answers</summary>

1. It accounts for local curvature and twisting in all directions.
2. The linear term vanishes because nabla f = 0.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [22_Critical_Points_and_Their_Classification.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\22_Critical_Points_and_Their_Classification.md)
