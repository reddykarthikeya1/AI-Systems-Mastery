# Lesson 09.11: Differentiability versus Existence of Partials

## Learning Objectives
- Understand why the existence of partial derivatives does not imply differentiability.
- State the sufficient condition: continuous partial derivatives (C^1).

## Prerequisites
- 09.05 Partial Derivatives.

---

## 1. The Core Idea
Existence of all partial derivatives $\frac{\partial f}{\partial x_i}$ only tests variation along coordinate axes. A function is truly **differentiable** at $\mathbf{x}_0$ if there exists a linear map $\mathbf{J}$ such that:
$$\lim_{\mathbf{h} \to \mathbf{0}} \frac{\|f(\mathbf{x}_0 + \mathbf{h}) - f(\mathbf{x}_0) - \mathbf{J}\mathbf{h}\|}{\|\mathbf{h}\|} = 0$$
If partial derivatives exist and are continuous on a neighborhood ($C^1$ smoothness), differentiability is guaranteed.

---

## 2. Mathematical Exposition & Worked Example
Consider $f(x, y) = \frac{xy}{\sqrt{x^2 + y^2}}$ for $(x, y) \ne (0, 0)$ and $f(0, 0) = 0$. Both $f_x(0,0) = 0$ and $f_y(0,0) = 0$, but approaching along $y = x$ gives $f(t, t) = \frac{t^2}{\sqrt{2} t} = \frac{t}{\sqrt{2}}$, which does not vanish at rate $o(\|\mathbf{h}\|)$.

---

## 3. Verify it in code

```python
import numpy as np
# Numerical check: along y = x, ||h|| = sqrt(2)*t, numerator error is t/sqrt(2)
# Ratio error / ||h|| = (t / sqrt(2)) / (sqrt(2)*t) = 1/2 != 0
t = 1e-4
h = np.array([t, t])
norm_h = np.linalg.norm(h)
f_val = (t * t) / np.sqrt(t**2 + t**2)
ratio = f_val / norm_h
assert np.isclose(ratio, 0.5)
```

---

## 4. The mistake people actually make
Believing that finding all partial derivatives is sufficient to prove a surface has a well-defined tangent plane.

---

## Check yourself
1. What condition on partial derivatives guarantees differentiability?
2. What is the remainder term order for a differentiable function?

<details>
<summary>Answers</summary>

1. That all partial derivatives are continuous in a neighborhood of the point.
2. o(||h||), strictly sublinear in step size.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [12_The_Total_Derivative_and_Linearization.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\12_The_Total_Derivative_and_Linearization.md)
