# Lesson 08.01 — A Linear Layer Is a Matrix Multiply

> **Module 08:** Linear Algebra in Models · Lesson 1 of 9

---

## What you will be able to do after this lesson

- [ ] Express a dense neural network layer mathematically as y = x W^T + b and compute it by hand.
- [ ] Verify the affine transformation dimensions and forward pass using pure NumPy.

## Prerequisites

- Matrix multiplication and inner products (Modules 03 and 04).

---

## 1. The idea

In modern deep learning frameworks (PyTorch, JAX, TensorFlow), the fundamental building block of multilayer perceptrons and transformer feed-forward blocks is the **linear layer** (or fully connected layer).

Mathematically, given an input feature vector $\mathbf{x} \in \mathbb{R}^{d_{in}}$, weight matrix $\mathbf{W} \in \mathbb{R}^{d_{out} \times d_{in}}$, and bias vector $\mathbf{b} \in \mathbb{R}^{d_{out}}$, the layer computes the affine transformation:
$$\mathbf{y} = \mathbf{W}\mathbf{x} + \mathbf{b}$$

When inputs are row vectors $\mathbf{x} \in \mathbb{R}^{1 \times d_{in}}$ (or batched matrices $\mathbf{X} \in \mathbb{R}^{B \times d_{in}}$), the standard framework convention represents the forward pass as:
$$\mathbf{Y} = \mathbf{X}\mathbf{W}^T + \mathbf{b}$$
where the bias $\mathbf{b}$ broadcasts across the batch dimension $B$.

---

## 2. Worked example

Let the input dimension be $d_{in} = 3$ and output dimension be $d_{out} = 2$.

Input vector:
$$\mathbf{x} = \begin{bmatrix} 1.0 & 2.0 & 0.5 \end{bmatrix}$$

Weight matrix $\mathbf{W}$ of shape $(2, 3)$:
$$\mathbf{W} = \begin{bmatrix} 0.5 & -1.0 & 2.0 \\ 1.5 & 0.0 & -0.5 \end{bmatrix}$$

Bias vector $\mathbf{b}$ of shape $(2,)$:
$$\mathbf{b} = \begin{bmatrix} 0.1 & -0.2 \end{bmatrix}$$

Computing $\mathbf{x} \mathbf{W}^T$:
$$y_1 = (1.0)(0.5) + (2.0)(-1.0) + (0.5)(2.0) + 0.1 = 0.5 - 2.0 + 1.0 + 0.1 = -0.4$$
$$y_2 = (1.0)(1.5) + (2.0)(0.0) + (0.5)(-0.5) - 0.2 = 1.5 + 0.0 - 0.25 - 0.2 = 1.05$$

Resulting output $\mathbf{y} = \begin{bmatrix} -0.4 & 1.05 \end{bmatrix}$.

---

## 3. Verify it in code

```python
import numpy as np

# 1. Inputs, weights, bias
x = np.array([[1.0, 2.0, 0.5]])  # Shape (1, 3)
W = np.array([[0.5, -1.0, 2.0],
              [1.5,  0.0, -0.5]]) # Shape (2, 3)
b = np.array([0.1, -0.2])        # Shape (2,)

# 2. Forward pass: Y = X @ W.T + b
y = x @ W.T + b

# 3. Verify exact numerical outputs
expected_y = np.array([[-0.4, 1.05]])
assert np.allclose(y, expected_y, atol=1e-7), f"Got {y}, expected {expected_y}"
assert y.shape == (1, 2)

# Verify component-wise dot products
assert np.isclose(np.dot(x[0], W[0]) + b[0], -0.4)
assert np.isclose(np.dot(x[0], W[1]) + b[1], 1.05)
```

---

## 4. The mistake people actually make

**Transposing weights inconsistently between row-vector and column-vector notations.**

In mathematical textbooks, vectors are usually columns ($\mathbf{y} = \mathbf{W}\mathbf{x}$). In deep learning software, datasets are ordered with sample indices first (rows $\mathbf{X}$ of shape $(B, D)$), so PyTorch stores weights as $(d_{out}, d_{in})$ and computes $\mathbf{X}\mathbf{W}^T + \mathbf{b}$. A frequent beginner bug is computing `x @ W` without transposition, leading to runtime dimension mismatch errors.

---

## Check yourself

1. If an input batch has shape (32, 128) and the weight matrix has shape (64, 128), what is the shape of the output Y after X @ W.T + b?
2. Why do deep learning frameworks store weights as (out_features, in_features) instead of (in_features, out_features)?

<details>
<summary>Answers</summary>

1. The output shape is (32, 64). The inner dimension 128 is contracted, and the batch dimension 32 and feature dimension 64 are preserved.
2. Storing weights as (out_features, in_features) enables BLAS routines to compute each output neuron dot product along contiguous memory rows.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Batching_as_Extra_Tensor_Dimensions.md)
