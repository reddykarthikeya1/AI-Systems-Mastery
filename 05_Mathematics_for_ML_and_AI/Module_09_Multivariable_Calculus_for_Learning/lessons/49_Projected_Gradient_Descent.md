# Lesson 09.49: Projected Gradient Descent

## Learning Objectives
- Formulate Projected Gradient Descent (PGD): x_{t+1} = Pi_C(x_t - eta nabla f(x_t)).
- Implement projection operators for Euclidean balls and hypercubes (e.g. adversarial attacks).

## Prerequisites
- 09.45 Constrained Optimization: The Setup.

---

## 1. The Core Idea
**Projected Gradient Descent (PGD)** optimizes over a closed convex set $\mathcal{C}$ by taking an unconstrained gradient step followed by an orthogonal projection back onto $\mathcal{C}$:
$$\mathbf{x}_{t+1} = \Pi_{\mathcal{C}}(\mathbf{x}_t - \eta \nabla f(\mathbf{x}_t)), \quad \Pi_{\mathcal{C}}(\mathbf{z}) = \arg\min_{\mathbf{y} \in \mathcal{C}} \|\mathbf{y} - \mathbf{z}\|_2$$
Widely utilized in adversarial robustness (e.g., Madry's PGD attack bounded in an $L_\infty$ or $L_2$ perturbation ball).

---

## 2. Mathematical Exposition & Worked Example
Projection onto $L_\infty$ box $[-\epsilon, \epsilon]^D$ is elementwise clipping: $\Pi(z)_i = \text{clip}(z_i, -\epsilon, \epsilon)$.
For $\epsilon = 0.5$ and update $\mathbf{z} = [0.8, -0.3, 1.2]^T$:
$\Pi(\mathbf{z}) = [0.5, -0.3, 0.5]^T$.

---

## 3. Verify it in code

```python
import numpy as np
eps = 0.5
z = np.array([0.8, -0.3, 1.2])
projected = np.clip(z, -eps, eps)
assert np.allclose(projected, np.array([0.5, -0.3, 0.5]))
```

---

## 4. The mistake people actually make
Using PGD on non-convex constraint sets where the projection operator is non-unique or discontinuous.

---

## Check yourself
1. What is the update rule for Projected Gradient Descent?
2. What is the projection of a vector onto the L_inf ball of radius eps?

<details>
<summary>Answers</summary>

1. x_{t+1} = Pi_C(x_t - eta * nabla f(x_t)).
2. Elementwise clipping between -eps and +eps.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [50_L1_versus_L2_Regularization_Geometrically.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\50_L1_versus_L2_Regularization_Geometrically.md)
