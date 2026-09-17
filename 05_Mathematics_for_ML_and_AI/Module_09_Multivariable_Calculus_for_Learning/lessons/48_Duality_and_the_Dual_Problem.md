# Lesson 09.48: Duality and the Dual Problem

## Learning Objectives
- Define the Lagrange dual function: g(lambda, nu) = inf_x L(x, lambda, nu).
- Understand weak duality (d* <= p*) and strong duality (Slater's condition).

## Prerequisites
- 09.47 The KKT Conditions.

---

## 1. The Core Idea
The **Lagrange dual function** is defined as the infimum of the Lagrangian:
$$g(\boldsymbol{\lambda}, \boldsymbol{\nu}) = \inf_{\mathbf{x}} \mathcal{L}(\mathbf{x}, \boldsymbol{\lambda}, \boldsymbol{\nu})$$
- **Weak Duality**: $g(\boldsymbol{\lambda}, \boldsymbol{\nu}) \le p^*$ for all feasible multipliers (the dual always lower-bounds primal optimal value).
- **Strong Duality**: $d^* = p^*$ (zero duality gap). Guaranteed for convex problems satisfying **Slater's condition** (existence of a strictly feasible point).

---

## 2. Mathematical Exposition & Worked Example
For primal $\min x^2$ subject to $x \ge 2$ ($2 - x \le 0$). Primal optimum $p^* = 4$.
$\mathcal{L}(x, \lambda) = x^2 + \lambda(2 - x)$.
Infimum over $x$: $2x - \lambda = 0 \implies x = \lambda/2$.
Dual function: $g(\lambda) = (\lambda/2)^2 + \lambda(2 - \lambda/2) = 2\lambda - \lambda^2/4$.
Maximize $g(\lambda)$ for $\lambda \ge 0$: $g'(\lambda) = 2 - \lambda/2 = 0 \implies \lambda^* = 4$.
$d^* = g(4) = 8 - 4 = 4$.
Since $d^* = p^* = 4$, strong duality holds!

---

## 3. Verify it in code

```python
import numpy as np
def g(lam):
    return 2.0 * lam - (lam**2) / 4.0

lam_opt = 4.0
d_star = g(lam_opt)
p_star = 4.0
assert d_star == p_star  # Zero duality gap
```

---

## 4. The mistake people actually make
Assuming strong duality holds for non-convex problems without verifying constraint qualifications.

---

## Check yourself
1. What is weak duality?
2. What condition guarantees strong duality (zero duality gap) in convex optimization?

<details>
<summary>Answers</summary>

1. The dual optimum is always less than or equal to the primal optimum: d* <= p*.
2. Slater's condition (convex problem with at least one strictly feasible interior point).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [49_Projected_Gradient_Descent.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\49_Projected_Gradient_Descent.md)
