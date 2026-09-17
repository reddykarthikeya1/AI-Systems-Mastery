# Lesson 09.18: Reverse-Mode Differentiation

## Learning Objectives
- Trace reverse accumulation of adjoints: bar{x}_i = d(loss) / dx_i.
- Prove reverse mode computes all n parameter gradients in a single backward pass.

## Prerequisites
- 09.16 Computational Graphs.

---

## 1. The Core Idea
**Reverse-mode AD** stores intermediate values on a forward tape, then sweeps backwards computing the **adjoint** $\bar{v}_i = \frac{\partial L}{\partial v_i}$ for each node:
$$\bar{v}_i = \sum_{j \in \text{Children}(i)} \bar{v}_j \frac{\partial v_j}{\partial v_i}$$
Crucially, a **single reverse sweep** yields the exact gradient $\nabla_\mathbf{w} L$ with respect to all $D$ inputs, scaling in $O(1)$ evaluations regardless of $D$.

---

## 2. Mathematical Exposition & Worked Example
Let $L = \ln(x_1 x_2) + x_1^2$. At $(x_1, x_2) = (2, 3)$:
Forward: $v_1 = x_1 x_2 = 6$, $v_2 = \ln(v_1) \approx 1.7918$, $v_3 = x_1^2 = 4$, $L = v_2 + v_3 \approx 5.7918$.
Backward: $\bar{L} = 1.0$. $\bar{v}_2 = 1.0, \bar{v}_3 = 1.0$.
$\bar{v}_1 = \bar{v}_2 \frac{1}{v_1} = 1/6$.
$\bar{x}_1 = \bar{v}_1 x_2 + \bar{v}_3 (2 x_1) = (1/6)(3) + 1(4) = 0.5 + 4 = 4.5$.
Analytical: $\frac{\partial L}{\partial x_1} = \frac{1}{x_1} + 2x_1 = 0.5 + 4 = 4.5$.

---

## 3. Verify it in code

```python
import numpy as np
x1, x2 = 2.0, 3.0
v1 = x1 * x2
v2 = np.log(v1)
v3 = x1**2
L = v2 + v3

# Reverse pass
dL = 1.0
dv2 = dL
dv3 = dL
dv1 = dv2 * (1.0 / v1)
dx1 = dv1 * x2 + dv3 * (2.0 * x1)
dx2 = dv1 * x1

assert np.isclose(dx1, 4.5)
assert np.isclose(dx2, 1.0 / 3.0)
```

---

## 4. The mistake people actually make
Failing to store forward activations needed in backward pass, leading to redundant recomputation or memory leaks.

---

## Check yourself
1. Why is reverse-mode AD universally preferred in deep learning?
2. What is the memory trade-off in reverse-mode AD?

<details>
<summary>Answers</summary>

1. Because ML has scalar losses (m = 1) and millions of parameters (n >> 1), giving all gradients in one backward pass.
2. All forward activations must be cached in memory until backward propagation completes.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [19_Backpropagation_Is_ReverseMode_Chain_Rule.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\19_Backpropagation_Is_ReverseMode_Chain_Rule.md)
