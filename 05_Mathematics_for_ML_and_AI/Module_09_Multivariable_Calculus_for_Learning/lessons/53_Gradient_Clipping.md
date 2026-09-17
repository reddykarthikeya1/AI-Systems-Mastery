# Lesson 09.53: Gradient Clipping

## Learning Objectives
- Implement global norm gradient clipping: g <- g * min(1, c / ||g||).
- Prevent catastrophic loss spikes in transformers and RNNs.

## Prerequisites
- 09.52 Vanishing and Exploding Gradients.

---

## 1. The Core Idea
**Global Norm Clipping** scales down the total parameter gradient vector if its $L_2$ norm exceeds a threshold $c$:
$$\mathbf{g} \leftarrow \begin{cases} \mathbf{g} & \text{if } \|\mathbf{g}\|_2 \le c \\ \frac{c}{\|\mathbf{g}\|_2} \mathbf{g} & \text{if } \|\mathbf{g}\|_2 > c \end{cases}$$
Crucially, this preserves the **exact direction** of the descent vector while capping the maximum step length, preventing catastrophic parameter updates from exploding gradients.

---

## 2. Mathematical Exposition & Worked Example
Clip threshold $c = 5.0$. Gradient $\mathbf{g} = [6.0, 8.0]^T \implies \|\mathbf{g}\| = 10.0 > 5.0$.
Scaling factor: $5.0 / 10.0 = 0.5$.
Clipped gradient: $\mathbf{g}_{\text{clipped}} = 0.5 \times [6.0, 8.0]^T = [3.0, 4.0]^T$. Norm is exactly $5.0$.

---

## 3. Verify it in code

```python
import numpy as np
g = np.array([6.0, 8.0])
c = 5.0
norm_g = np.linalg.norm(g)
if norm_g > c:
    g_clipped = g * (c / norm_g)
else:
    g_clipped = g

assert np.isclose(np.linalg.norm(g_clipped), 5.0)
assert np.allclose(g_clipped, np.array([3.0, 4.0]))
```

---

## 4. The mistake people actually make
Clipping each parameter tensor independently rather than clipping the global norm, which alters the relative direction of updates across layers.

---

## Check yourself
1. What is the key advantage of norm clipping over value clipping?
2. What does global norm clipping do if ||g|| <= c?

<details>
<summary>Answers</summary>

1. It preserves the exact mathematical direction of the gradient vector.
2. It leaves the gradient completely untouched.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [54_Numerical_Gradient_Checking.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\54_Numerical_Gradient_Checking.md)
