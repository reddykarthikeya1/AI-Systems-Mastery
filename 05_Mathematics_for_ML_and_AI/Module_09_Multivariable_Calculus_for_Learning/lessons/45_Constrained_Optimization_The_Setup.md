# Lesson 09.45: Constrained Optimization: The Setup

## Learning Objectives
- Formulate standard constrained programs: min f(x) s.t. g_i(x) <= 0, h_j(x) = 0.
- Define the feasible region and active constraints.

## Prerequisites
- 09.25 Convex Functions Definition.

---

## 1. The Core Idea
A standard **constrained optimization problem** is formulated as:
$$\min_{\mathbf{x} \in \mathbb{R}^n} f(\mathbf{x}) \quad \text{subject to } g_i(\mathbf{x}) \le 0 \; (i=1,\dots,m), \quad h_j(\mathbf{x}) = 0 \; (j=1,\dots,p)$$
The **feasible region** $\mathcal{F}$ is the set of points satisfying all constraints simultaneously. An inequality constraint $g_i$ is **active** at $\mathbf{x}^*$ if $g_i(\mathbf{x}^*) = 0$.

---

## 2. Mathematical Exposition & Worked Example
Minimize $f(x, y) = x + y$ subject to $x^2 + y^2 \le 1$.
The feasible region $\mathcal{F}$ is the unit disc.
Since $\nabla f = [1, 1]^T \ne \mathbf{0}$, the minimum cannot lie in the interior; it must occur on the active boundary $x^2 + y^2 = 1$ at $(-1/\sqrt{2}, -1/\sqrt{2})$.

---

## 3. Verify it in code

```python
import numpy as np
pt = np.array([-1.0/np.sqrt(2.0), -1.0/np.sqrt(2.0)])
assert np.isclose(np.sum(pt**2), 1.0)  # On boundary (active)
assert np.isclose(np.sum(pt), -np.sqrt(2.0))
```

---

## 4. The mistake people actually make
Ignoring the constraint boundary and solving via unconstrained nabla f = 0, which often produces an infeasible point.

---

## Check yourself
1. What is an active constraint?
2. What is the feasible region of an optimization problem?

<details>
<summary>Answers</summary>

1. An inequality constraint g_i(x) <= 0 that holds with strict equality g_i(x*) = 0 at the optimum.
2. The intersection of all sets where all constraints are satisfied.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [46_Lagrange_Multipliers.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\46_Lagrange_Multipliers.md)
