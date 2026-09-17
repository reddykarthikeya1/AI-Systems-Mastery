# Lesson 09.10: Directional Derivatives

## Learning Objectives
- Compute the directional derivative D_v f = nabla f . v.
- Connect directional derivatives to line search updates in optimization.

## Prerequisites
- 09.08 The Gradient Vector.

---

## 1. The Core Idea
The **directional derivative** of $f$ at $\mathbf{x}$ in direction $\mathbf{v}$ ($\|\mathbf{v}\| = 1$) is:
$$D_\mathbf{v} f(\mathbf{x}) = \lim_{t \to 0} \frac{f(\mathbf{x} + t \mathbf{v}) - f(\mathbf{x})}{t} = \nabla f(\mathbf{x}) \cdot \mathbf{v}$$
It represents the slope of the 1D slice of $f$ along the ray $\mathbf{x} + t\mathbf{v}$.

---

## 2. Mathematical Exposition & Worked Example
For $f(x, y) = x^2 y$, $\nabla f = [2xy, x^2]^T$. At $(2, 1)$, $\nabla f = [4, 4]^T$. Direction $\mathbf{v} = [1/\sqrt{2}, 1/\sqrt{2}]^T$. $D_\mathbf{v} f = 4(1/\sqrt{2}) + 4(1/\sqrt{2}) = 8/\sqrt{2} = 4\sqrt{2} \approx 5.657$.

---

## 3. Verify it in code

```python
import numpy as np
g = np.array([4.0, 4.0])
v = np.array([1.0, 1.0]) / np.sqrt(2.0)
d_v = np.dot(g, v)
assert np.isclose(d_v, 4.0 * np.sqrt(2.0))
```

---

## 4. The mistake people actually make
Failing to normalize direction vector v to unit length before computing D_v f.

---

## Check yourself
1. How is a partial derivative df/dx_i related to directional derivatives?
2. What is D_v f if v is perpendicular to nabla f?

<details>
<summary>Answers</summary>

1. df/dx_i is the directional derivative along the unit basis vector e_i.
2. 0 (zero instantaneous change).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [11_Differentiability_versus_Existence_of_Partials.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\11_Differentiability_versus_Existence_of_Partials.md)
