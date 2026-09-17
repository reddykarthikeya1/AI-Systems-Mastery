# Lesson 09.29: Gradient Descent: The Update Rule

## Learning Objectives
- Formulate the gradient descent iteration: x_{t+1} = x_t - eta nabla f(x_t).
- Implement basic gradient descent on quadratic surfaces.

## Prerequisites
- 09.09 Why the Gradient Points Uphill.

---

## 1. The Core Idea
**Gradient descent** iteratively updates parameters along the negative gradient direction:
$$\mathbf{x}_{t+1} = \mathbf{x}_t - \eta \nabla f(\mathbf{x}_t)$$
where $\eta > 0$ is the learning rate (step size). For sufficiently small $\eta$, each step guarantees a local decrease in objective value: $f(\mathbf{x}_{t+1}) < f(\mathbf{x}_t)$ whenever $\nabla f(\mathbf{x}_t) \ne \mathbf{0}$.

---

## 2. Mathematical Exposition & Worked Example
For $f(x) = x^2$, $\nabla f(x) = 2x$. With $x_0 = 4.0$ and $\eta = 0.1$:
$x_1 = 4.0 - 0.1(2 \times 4.0) = 4.0 - 0.8 = 3.2$.
$x_2 = 3.2 - 0.1(2 \times 3.2) = 3.2 - 0.64 = 2.56$.

---

## 3. Verify it in code

```python
import numpy as np
x = 4.0
eta = 0.1
for _ in range(2):
    x = x - eta * (2.0 * x)
assert np.isclose(x, 2.56)
```

---

## 4. The mistake people actually make
Setting learning rate too high, causing gradient descent to oscillate and diverge exponentially.

---

## Check yourself
1. What is the update equation for standard gradient descent?
2. When does gradient descent stop moving?

<details>
<summary>Answers</summary>

1. x_{t+1} = x_t - eta * nabla f(x_t).
2. When nabla f(x_t) = 0 (at a stationary/critical point).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [30_Learning_Rate_and_Convergence.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\30_Learning_Rate_and_Convergence.md)
