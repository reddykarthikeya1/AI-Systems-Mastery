# Lesson 09.33: Momentum

## Learning Objectives
- Formulate Polyak's classical heavy-ball momentum: v_{t+1} = beta v_t + eta nabla f(x_t).
- Explain how momentum dampens orthogonal oscillations in ill-conditioned ravines.

## Prerequisites
- 09.29 Gradient Descent: The Update Rule.

---

## 1. The Core Idea
**Polyak Momentum** simulates a heavy particle with friction rolling down the loss surface:
$$\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \eta \nabla f(\mathbf{x}_t), \quad \mathbf{x}_{t+1} = \mathbf{x}_t - \mathbf{v}_{t+1}$$
Typical $\beta \in [0.9, 0.99]$. Momentum cancels out high-frequency oscillating gradients across narrow canyon walls while accumulating velocity along the shallow downhill valley floor.

---

## 2. Mathematical Exposition & Worked Example
Constant gradient $g = 2.0$, $\eta = 0.1$, $\beta = 0.9$.
$v_1 = 0.1(2.0) = 0.2$.
$v_2 = 0.9(0.2) + 0.1(2.0) = 0.18 + 0.2 = 0.38$.
Terminal steady-state velocity: $v_\infty = \frac{\eta g}{1 - \beta} = \frac{0.2}{0.1} = 2.0$ ($10\times$ speedup).

---

## 3. Verify it in code

```python
import numpy as np
beta = 0.9
eta = 0.1
g = 2.0
v = 0.0
for _ in range(100):
    v = beta * v + eta * g
assert np.isclose(v, (eta * g) / (1.0 - beta), atol=1e-3)
assert np.isclose(v, 2.0, atol=1e-3)
```

---

## 4. The mistake people actually make
Setting momentum beta too close to 1 without reducing eta, causing severe overshoot and spiraling out of minima.

---

## Check yourself
1. What is the effective velocity multiplier in steady state for momentum beta = 0.9?
2. How does momentum help navigate narrow ill-conditioned ravines?

<details>
<summary>Answers</summary>

1. 1 / (1 - beta) = 1 / 0.1 = 10x.
2. It averages out oscillating cross-canyon gradients while reinforcing forward movement along the floor.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [34_Nesterov_Acceleration.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\34_Nesterov_Acceleration.md)
