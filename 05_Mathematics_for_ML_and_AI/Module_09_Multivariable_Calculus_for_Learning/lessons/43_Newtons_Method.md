# Lesson 09.43: Newton's Method

## Learning Objectives
- Formulate Newton-Raphson optimization: x_{t+1} = x_t - H^{-1} nabla f(x_t).
- Demonstrate quadratic convergence near local minima.

## Prerequisites
- 09.21 Second-Order Taylor Expansion.

---

## 1. The Core Idea
**Newton's Method** fits an osculating quadratic to the surface and jumps directly to its stationary point:
$$\mathbf{x}_{t+1} = \mathbf{x}_t - [\nabla^2 f(\mathbf{x}_t)]^{-1} \nabla f(\mathbf{x}_t)$$
Near a strict local minimum, Newton's method exhibits **quadratic convergence**: $\|\mathbf{x}_{t+1} - \mathbf{x}^*\| \le C \|\mathbf{x}_t - \mathbf{x}^*\|^2$, doubling the number of correct digits every single step!

---

## 2. Mathematical Exposition & Worked Example
For $f(x) = \frac{1}{4} x^4 - x$. $f'(x) = x^3 - 1$, $f''(x) = 3x^2$.
At $x_0 = 2.0$: $f'(2) = 7$, $f''(2) = 12$.
$x_1 = 2.0 - \frac{7}{12} = \frac{17}{12} \approx 1.4167$.
$x^* = 1.0$. Error drops from $1.0 \to 0.4167$ in 1 step.

---

## 3. Verify it in code

```python
import numpy as np
def step(x):
    return x - (x**3 - 1.0) / (3.0 * x**2)

x0 = 2.0
x1 = step(x0)
x2 = step(x1)
x3 = step(x2)
assert np.isclose(x1, 17.0 / 12.0)
assert abs(x2 - 1.0) < 0.12
assert abs(x3 - 1.0) < 0.02
```

---

## 4. The mistake people actually make
Applying pure Newton's method in regions where the Hessian is indefinite or negative definite, which causes it to jump toward local maxima.

---

## Check yourself
1. What is Newton's optimization update rule?
2. What is the order of convergence for Newton's method near a minimum?

<details>
<summary>Answers</summary>

1. x_{t+1} = x_t - H^{-1} * nabla f(x_t).
2. Quadratic convergence (doubles precision digits each iteration).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [44_QuasiNewton_Methods_and_LBFGS.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\44_QuasiNewton_Methods_and_LBFGS.md)
