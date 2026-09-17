# Lesson 09.55: Automatic Differentiation Pitfalls

## Learning Objectives
- Identify non-differentiable points in ReLU, max pooling, and argmax.
- Handle subgradients and silent zero-gradient bugs in computational graphs.

## Prerequisites
- 09.18 Reverse-Mode Differentiation.

---

## 1. The Core Idea
Autograd engines handle non-differentiable operations via **subgradients**. For $\text{ReLU}(x) = \max(0, x)$, convention sets $\frac{d}{dx}\text{ReLU}(0) = 0$ or $0.5$.
Key pitfalls:
1. **Dying ReLUs**: If $x < 0$, gradient is permanently zero.
2. **Discrete operations**: Operations like $\text{argmax}$ or $\text{round}$ have zero gradients almost everywhere, preventing gradient flow (requiring Gumbel-Softmax or straight-through estimators).

---

## 2. Mathematical Exposition & Worked Example
If an input to ReLU is $-2.5$, the activation is $0$ and backward gradient is $0.0 \times \bar{y} = 0.0$. If a neuron's bias causes all inputs in a batch to be negative, its gradient is zero and it can never recover.

---

## 3. Verify it in code

```python
import numpy as np
def relu_backward(x, grad_out):
    return grad_out * (x > 0).astype(float)

x = np.array([-2.0, 0.5, 3.0])
grad_out = np.array([1.0, 1.0, 1.0])
grad_in = relu_backward(x, grad_out)

assert np.allclose(grad_in, np.array([0.0, 1.0, 1.0]))
```

---

## 4. The mistake people actually make
Using torch.argmax in a loss function and wondering why backpropagation reports None or zeros for parameter gradients.

---

## Check yourself
1. What is a subgradient of ReLU at x = 0?
2. Why can't argmax be directly trained with gradient descent?

<details>
<summary>Answers</summary>

1. Any value in the interval [0, 1] (standard frameworks choose 0.0).
2. Because its derivative is zero everywhere (piecewise constant), providing zero learning signal.

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [56_Line_Search_and_Trust_Regions.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\56_Line_Search_and_Trust_Regions.md)
