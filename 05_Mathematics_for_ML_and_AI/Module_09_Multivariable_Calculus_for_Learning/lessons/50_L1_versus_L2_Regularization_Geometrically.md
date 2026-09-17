# Lesson 09.50: L1 versus L2 Regularization Geometrically

## Learning Objectives
- Compare L1 (diamond/cross-polytope) and L2 (hypersphere) constraint balls.
- Explain why the unconstrained loss contours intersect corners versus smooth faces.

## Prerequisites
- 09.02 Level Sets and Contour Plots.

---

## 1. The Core Idea
Regularized objectives $\min f(\mathbf{w}) + \lambda \|\mathbf{w}\|_p$ are equivalent to constrained problems $\min f(\mathbf{w})$ s.t. $\|\mathbf{w}\|_p \le C$.
- **$L_2$ ball**: A smooth sphere $\{\mathbf{w} : \sum w_i^2 \le C\}$. Contours of loss $f$ contact the sphere at arbitrary smooth tangent points, shrinking weights without zeroing them.
- **$L_1$ ball**: A sharp diamond $\{\mathbf{w} : \sum |w_i| \le C\}$. Contours almost always contact the sharp pointed vertices aligned with coordinate axes, driving weights to exact zeros.

---

## 2. Mathematical Exposition & Worked Example
In 2D, the $L_1$ ball has vertices at $(\pm C, 0)$ and $(0, \pm C)$. Any elliptical contour expanding outward has high geometric probability of making first contact at one of these 4 corner points.

---

## 3. Verify it in code

```python
import numpy as np
# Check L1 vs L2 norm of sparse vector vs dense vector with equal L2 norm
w_sparse = np.array([1.0, 0.0])
w_dense = np.array([1.0 / np.sqrt(2), 1.0 / np.sqrt(2)])

assert np.isclose(np.linalg.norm(w_sparse, 2), 1.0)
assert np.isclose(np.linalg.norm(w_dense, 2), 1.0)

l1_sparse = np.sum(np.abs(w_sparse))  # 1.0
l1_dense = np.sum(np.abs(w_dense))    # sqrt(2) ~ 1.414
assert l1_sparse < l1_dense
```

---

## 4. The mistake people actually make
Claiming L2 regularization produces sparse feature sets; only L1 regularization drives exact zeros.

---

## Check yourself
1. Why does L1 regularization drive weights to exact zeros?
2. What shape is the L1 unit ball in 2D?

<details>
<summary>Answers</summary>

1. Because the L1 ball has sharp corners on the coordinate axes where expanding loss contours first touch.
2. A diamond (rotated square with vertices on the axes).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [51_Why_L1_Produces_Sparsity.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\51_Why_L1_Produces_Sparsity.md)
