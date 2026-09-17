# Lesson 09.26: First- and Second-Order Convexity Tests

## Learning Objectives
- Apply the first-order condition: f(y) >= f(x) + nabla f(x)^T (y - x).
- Apply the second-order condition: nabla^2 f(x) >= 0 (positive semidefinite everywhere).

## Prerequisites
- 09.25 Convex Functions Definition.

---

## 1. The Core Idea
For differentiable $f$:
- **First-Order Condition**: $f$ is convex iff the tangent plane is a global lower bound:
$$f(\mathbf{y}) \ge f(\mathbf{x}) + \nabla f(\mathbf{x})^T (\mathbf{y} - \mathbf{x}) \quad \forall \mathbf{x}, \mathbf{y}$$
- **Second-Order Condition**: $f$ is convex iff its Hessian is positive semidefinite everywhere:
$$\nabla^2 f(\mathbf{x}) \succeq 0 \quad \forall \mathbf{x}$$

---

## 2. Mathematical Exposition & Worked Example
For $f(\mathbf{x}) = \frac{1}{2} \mathbf{x}^T \mathbf{A} \mathbf{x}$ with symmetric $\mathbf{A}$: $\nabla^2 f(\mathbf{x}) = \mathbf{A}$.
$f$ is convex if and only if $\mathbf{A} \succeq 0$ (all eigenvalues $\lambda_i \ge 0$).

---

## 3. Verify it in code

```python
import numpy as np
A = np.array([[3.0, 1.0], [1.0, 2.0]])
eigvals = np.linalg.eigvalsh(A)
assert np.all(eigvals >= 0)  # A is PSD -> f is convex everywhere
```

---

## 4. The mistake people actually make
Testing the Hessian at only a single point; global convexity requires H >= 0 across the entire domain.

---

## Check yourself
1. What does the first-order convexity condition say about tangent hyperplanes?
2. What condition on the Hessian characterizes C^2 convex functions?

<details>
<summary>Answers</summary>

1. The tangent hyperplane at any point lies entirely on or below the graph of the function.
2. The Hessian is positive semidefinite everywhere (nabla^2 f >= 0).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [27_Strong_Convexity_and_Smoothness.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\27_Strong_Convexity_and_Smoothness.md)
