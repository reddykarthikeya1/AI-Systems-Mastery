# Lesson 09.19: Backpropagation Is Reverse-Mode Chain Rule

## Learning Objectives
- Identify standard backprop as reverse-mode AD applied to layer tensors.
- Derive the weight and bias gradients for an affine layer y = W x + b.

## Prerequisites
- 09.18 Reverse-Mode Differentiation.

---

## 1. The Core Idea
**Backpropagation** is simply reverse-mode automatic differentiation specialized to neural networks with tensor variables.
For linear layer $\mathbf{y} = \mathbf{W}\mathbf{x} + \mathbf{b}$ and upstream gradient $\bar{\mathbf{y}} = \frac{\partial L}{\partial \mathbf{y}}$:
$$\frac{\partial L}{\partial \mathbf{W}} = \bar{\mathbf{y}} \mathbf{x}^T, \quad \frac{\partial L}{\partial \mathbf{b}} = \bar{\mathbf{y}}, \quad \frac{\partial L}{\partial \mathbf{x}} = \mathbf{W}^T \bar{\mathbf{y}}$$

---

## 2. Mathematical Exposition & Worked Example
Let $\mathbf{x} = [1, 2]^T$, $\mathbf{W} = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}$, $\mathbf{b} = [0, 0]^T$.
$\mathbf{y} = [4, 6]^T$. If loss $L = \frac{1}{2}\|\mathbf{y}\|^2$, $\bar{\mathbf{y}} = \mathbf{y} = [4, 6]^T$.
Then $\frac{\partial L}{\partial \mathbf{W}} = \begin{bmatrix} 4 \\ 6 \end{bmatrix} \begin{bmatrix} 1 & 2 \end{bmatrix} = \begin{bmatrix} 4 & 8 \\ 6 & 12 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np
x = np.array([1.0, 2.0])
W = np.array([[2.0, 1.0], [0.0, 3.0]])
y = W @ x
dL_dy = y  # from L = 0.5 * ||y||^2

dL_dW = np.outer(dL_dy, x)
dL_dx = W.T @ dL_dy

assert np.allclose(dL_dW, np.array([[4.0, 8.0], [6.0, 12.0]]))
assert np.allclose(dL_dx, np.array([8.0, 22.0]))
```

---

## 4. The mistake people actually make
Mixing up matrix transpose orientations: dL/dW is outer product (dL/dy) x^T, not x (dL/dy)^T.

---

## Check yourself
1. What is the gradient dL/dW for y = W x?
2. How is the gradient propagated to the preceding layer x?

<details>
<summary>Answers</summary>

1. dL/dW = (dL/dy) x^T.
2. dL/dx = W^T (dL/dy).

</details>

---

## Lesson checklist
- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

Next: [20_The_Hessian_Matrix.md](file:///c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\05_Mathematics_for_ML_and_AI\Module_09_Multivariable_Calculus_for_Learning\lessons\20_The_Hessian_Matrix.md)
