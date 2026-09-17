# Lesson 09.09: Why the Gradient Points Uphill

## Learning Objectives
- Prove via Cauchy-Schwarz that nabla f points in the direction of steepest ascent.
- Deduce why gradient descent steps in the negative gradient direction -nabla f.

## Prerequisites
- 09.08 The Gradient Vector.

---

## 1. The Core Idea
For any unit direction $\mathbf{u}$ ($\|\mathbf{u}\| = 1$), the directional derivative is $D_\mathbf{u} f = \nabla f \cdot \mathbf{u} = \|\nabla f\| \|\mathbf{u}\| \cos \theta = \|\nabla f\| \cos \theta$.
This inner product is maximized when $\cos \theta = 1 \iff \mathbf{u} = \frac{\nabla f}{\|\nabla f\|}$ (steepest ascent) and minimized when $\cos \theta = -1 \iff \mathbf{u} = -\frac{\nabla f}{\|\nabla f\|}$ (**steepest descent**).

---

## 2. Mathematical Exposition & Worked Example
If $\nabla f = [3, 4]^T$, $\|\nabla f\| = 5$. The maximum rate of increase is $+5$ along direction $[0.6, 0.8]^T$. The steepest decrease is $-5$ along $[-0.6, -0.8]^T$.

---

## 3. Verify it in code

```python
import numpy as np
g = np.array([3.0, 4.0])
norm_g = np.linalg.norm(g)
u_max = g / norm_g
u_min = -g / norm_g

assert np.isclose(norm_g, 5.0)
assert np.isclose(np.dot(g, u_max), 5.0)
assert np.isclose(np.dot(g, u_min), -5.0)
```

---

## 4. The mistake people actually make
Believing gradient descent is globally optimal; steepest descent is strictly a local instantaneous property.

---

## Check yourself
1. Why is cos(theta) maximized at theta = 0?
2. What is the rate of change in a direction orthogonal to the gradient?

<details>
<summary>Answers</summary>

1. cos(0) = 1, achieving the upper Cauchy-Schwarz bound.
2. Zero, because cos(pi/2) = 0 (moving along the level set).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [10_Directional_Derivatives.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\10_Directional_Derivatives.md)
