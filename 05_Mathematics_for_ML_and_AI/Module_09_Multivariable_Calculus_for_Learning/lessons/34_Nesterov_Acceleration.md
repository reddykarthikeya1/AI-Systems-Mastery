# Lesson 09.34: Nesterov Acceleration

## Learning Objectives
- Formulate Nesterov Accelerated Gradient (NAG): evaluate gradient at lookahead point x_t - beta v_t.
- Understand Nesterov's optimal O(1/T^2) first-order convergence bound.

## Prerequisites
- 09.33 Momentum.

---

## 1. The Core Idea
**Nesterov Accelerated Gradient (NAG)** computes the gradient not at the current position, but at the **lookahead point** projected by momentum:
$$\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \eta \nabla f(\mathbf{x}_t - \beta \mathbf{v}_t), \quad \mathbf{x}_{t+1} = \mathbf{x}_t - \mathbf{v}_{t+1}$$
This lookahead acts as an anticipatory brake: if momentum is carrying the parameters uphill, the future gradient immediately applies corrective deceleration.

---

## 2. Mathematical Exposition & Worked Example
Let $f(x) = \frac{1}{2} x^2$. At $x = 1.0$, $v = 0.5$, $\beta = 0.8$, $\eta = 0.1$.
Lookahead: $x_{\text{look}} = 1.0 - 0.8(0.5) = 0.6$.
$\nabla f(x_{\text{look}}) = 0.6$.
$v_{\text{next}} = 0.8(0.5) + 0.1(0.6) = 0.40 + 0.06 = 0.46$.
$x_{\text{next}} = 1.0 - 0.46 = 0.54$.

---

## 3. Verify it in code

```python
import numpy as np
x, v = 1.0, 0.5
beta, eta = 0.8, 0.1
x_look = x - beta * v
g_look = x_look
v_next = beta * v + eta * g_look
x_next = x - v_next

assert np.isclose(x_look, 0.6)
assert np.isclose(v_next, 0.46)
assert np.isclose(x_next, 0.54)
```

---

## 4. The mistake people actually make
Evaluating the gradient at current position x_t instead of lookahead point x_t - beta * v_t.

---

## Check yourself
1. What is the key difference between Polyak momentum and Nesterov momentum?
2. What is the theoretical convergence rate of NAG on convex smooth objectives?

<details>
<summary>Answers</summary>

1. NAG evaluates gradients at the lookahead position x_t - beta * v_t rather than x_t.
2. O(1 / T^2), which is mathematically optimal for first-order black-box optimization.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [35_AdaGrad.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\35_AdaGrad.md)
