# Lesson 09.22: Critical Points and Their Classification

## Learning Objectives
- Define critical (stationary) points: nabla f(x*) = 0.
- Classify critical points as local minima, local maxima, or saddle points.

## Prerequisites
- 09.21 Second-Order Taylor Expansion.

---

## 1. The Core Idea
A point $\mathbf{x}^*$ is a **critical point** if $\nabla f(\mathbf{x}^*) = \mathbf{0}$.
Near $\mathbf{x}^*$, the first-order change is zero: $f(\mathbf{x}^* + \mathbf{h}) - f(\mathbf{x}^*) \approx \frac{1}{2} \mathbf{h}^T \mathbf{H} \mathbf{h}$.
The classification depends entirely on the signs of the eigenvalues of the Hessian $\mathbf{H}$.

---

## 2. Mathematical Exposition & Worked Example
$f(x, y) = x^2 - y^2$. $\nabla f = [2x, -2y]^T = \mathbf{0} \implies (x, y) = (0, 0)$ is the unique critical point.
Hessian is $\begin{bmatrix} 2 & 0 \\ 0 & -2 \end{bmatrix}$. Along $x$-axis ($h_2 = 0$), $f$ curves upward ($+2 h_1^2$). Along $y$-axis ($h_1 = 0$), $f$ curves downward ($-2 h_2^2$). Thus $(0, 0)$ is a **saddle point**.

---

## 3. Verify it in code

```python
import numpy as np
H = np.array([[2.0, 0.0], [0.0, -2.0]])
eigvals = np.linalg.eigvalsh(H)
assert np.any(eigvals > 0) and np.any(eigvals < 0)  # Saddle point
```

---

## 4. The mistake people actually make
Assuming every point where nabla f = 0 is a local minimum (saddle points abound in high dimensions).

---

## Check yourself
1. What condition defines a critical point?
2. What type of critical point has eigenvalues of mixed signs in its Hessian?

<details>
<summary>Answers</summary>

1. The gradient vector is zero: nabla f(x*) = 0.
2. A saddle point.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [23_The_Second_Derivative_Test_in_Rn.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\23_The_Second_Derivative_Test_in_Rn.md)
