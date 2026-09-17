# Lesson 09.13: The Jacobian Matrix

## Learning Objectives
- Define the Jacobian matrix J in R^(m x n) for vector-valued maps f: R^n -> R^m.
- Compute Jacobians of neural layer mappings and coordinate transformations.

## Prerequisites
- 09.05 Partial Derivatives.

---

## 1. The Core Idea
For a vector-valued function $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$, the **Jacobian matrix** $\mathbf{J} \in \mathbb{R}^{m \times n}$ gathers all first partial derivatives:
$$J_{ij} = \frac{\partial f_i}{\partial x_j}, \quad \mathbf{J} = \begin{bmatrix} \nabla f_1^T \\ \vdots \\ \nabla f_m^T \end{bmatrix}$$
It describes the best local linear mapping: $\mathbf{f}(\mathbf{x} + \mathbf{h}) \approx \mathbf{f}(\mathbf{x}) + \mathbf{J} \mathbf{h}$.

---

## 2. Mathematical Exposition & Worked Example
Polar to Cartesian $\mathbf{f}(r, \theta) = [r \cos \theta, r \sin \theta]^T$.
$\mathbf{J} = \begin{bmatrix} \cos \theta & -r \sin \theta \\ \sin \theta & r \cos \theta \end{bmatrix}$. At $(r, \theta) = (2, 0)$: $\mathbf{J} = \begin{bmatrix} 1 & 0 \\ 0 & 2 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
r, theta = 2.0, 0.0
J = np.array([
    [np.cos(theta), -r * np.sin(theta)],
    [np.sin(theta),  r * np.cos(theta)]
])
expected = np.array([[1.0, 0.0], [0.0, 2.0]])
assert np.allclose(J, expected)
```

---

## 4. The mistake people actually make
Transposing the Jacobian dimensions (it has m rows for m outputs and n columns for n inputs).

---

## Check yourself
1. What are the dimensions of the Jacobian of f: R^100 -> R^10?
2. If f: R^n -> R is a scalar field, what is its Jacobian?

<details>
<summary>Answers</summary>

1. 10 rows by 100 columns (10 x 100).
2. A 1 x n row vector (the transpose of the gradient).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [14_The_SingleVariable_Chain_Rule_Revisited.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\14_The_SingleVariable_Chain_Rule_Revisited.md)
