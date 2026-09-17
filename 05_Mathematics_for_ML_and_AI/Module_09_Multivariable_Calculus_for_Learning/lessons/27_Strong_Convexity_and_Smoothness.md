# Lesson 09.27: Strong Convexity and Smoothness

## Learning Objectives
- Define mu-strong convexity: nabla^2 f >= mu I (quadratic lower bowl).
- Define L-smoothness: ||nabla f(x) - nabla f(y)|| <= L ||x - y|| (quadratic upper bowl).

## Prerequisites
- 09.26 First- and Second-Order Convexity Tests.

---

## 1. The Core Idea
A function is **$\mu$-strongly convex** and **$L$-smooth** if its curvature is strictly sandwiched:
$$\mu \mathbf{I} \preceq \nabla^2 f(\mathbf{x}) \preceq L \mathbf{I} \quad \forall \mathbf{x}$$
Geometrically:
$$f(\mathbf{x}) + \nabla f(\mathbf{x})^T \mathbf{h} + \frac{\mu}{2}\|\mathbf{h}\|^2 \le f(\mathbf{x} + \mathbf{h}) \le f(\mathbf{x}) + \nabla f(\mathbf{x})^T \mathbf{h} + \frac{L}{2}\|\mathbf{h}\|^2$$
The ratio $\kappa = L / \mu$ is the **condition number** of the optimization problem.

---

## 2. Mathematical Exposition & Worked Example
For $f(x) = \frac{1}{2} x^T \begin{bmatrix} 10 & 0 \\ 0 & 2 \end{bmatrix} x$, $\mu = 2$ and $L = 10$.
Condition number $\kappa = 10 / 2 = 5$.

---

## 3. Verify it in code

```python
import numpy as np
H = np.array([[10.0, 0.0], [0.0, 2.0]])
eigvals = np.linalg.eigvalsh(H)
mu = np.min(eigvals)
L = np.max(eigvals)
kappa = L / mu

assert mu == 2.0
assert L == 10.0
assert kappa == 5.0
```

---

## 4. The mistake people actually make
Confusing smoothness in calculus (differentiability C^infinity) with L-smoothness in optimization (Lipschitz continuous gradients).

---

## Check yourself
1. What is the condition number kappa of an objective function?
2. What happens to optimization when kappa is very large?

<details>
<summary>Answers</summary>

1. kappa = L / mu (ratio of maximum to minimum curvature).
2. Conditioning is poor; gradient descent oscillates violently across narrow ravines.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [28_Jensens_Inequality.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\28_Jensens_Inequality.md)
