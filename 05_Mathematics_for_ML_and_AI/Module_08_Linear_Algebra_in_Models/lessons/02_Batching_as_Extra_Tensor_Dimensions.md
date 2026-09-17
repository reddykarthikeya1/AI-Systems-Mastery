# Lesson 08.02 — Batching as Extra Tensor Dimensions

> **Module 08:** Linear Algebra in Models · Lesson 2 of 9

---

## What you will be able to do after this lesson

- [ ] Explain how batching transforms single-sample vector operations into high-throughput parallel matrix operations.
- [ ] Verify multi-dimensional tensor contractions and batch matrix multiplications with NumPy.

## Prerequisites

- 08.01 Linear Layer Matrix Multiplication.

---

## 1. The idea

Batching stacks $B$ independent samples into a single matrix $\mathbf{X} \in \mathbb{R}^{B \times d_{in}}$. Instead of evaluating $B$ separate matrix-vector products, the GPU performs one single General Matrix Multiply (GEMM):
$$\mathbf{Y} = \mathbf{X}\mathbf{W}^T + \mathbf{b}$$
For sequence models (transformers), an extra sequence length dimension $S$ is added, yielding 3D tensors $\mathbf{X} \in \mathbb{R}^{B \times S \times d}$ where matrix multiplication operates over trailing dimensions.

---

## 2. Worked example

Let batch size $B = 2$, sequence length $S = 3$, feature dimension $D = 4$, and projection dimension $D_{out} = 2$.
Input tensor shape: $(2, 3, 4)$.
Projection weight shape: $(2, 4)$.
Evaluating batched contraction over the last axis yields shape $(2, 3, 2)$. Each of the $2 \times 3 = 6$ token vectors undergoes an identical independent affine map.

---

## 3. Verify it in code

```python
import numpy as np

B, S, D_in, D_out = 2, 3, 4, 2
np.random.seed(42)
X = np.random.randn(B, S, D_in)
W = np.random.randn(D_out, D_in)
b = np.random.randn(D_out)

# Batched matrix multiplication: (B, S, D_in) @ (D_in, D_out) -> (B, S, D_out)
Y = X @ W.T + b
assert Y.shape == (B, S, D_out)

for b_idx in range(B):
    for s_idx in range(S):
        sample_vec = X[b_idx, s_idx]
        single_y = sample_vec @ W.T + b
        assert np.allclose(Y[b_idx, s_idx], single_y)
```

---

## 4. The mistake people actually make

**Collapsing batch and sequence dimensions incorrectly when reshaping.**

When reshaping tensors between $(B, S, D)$ and $(B \times S, D)$, transposing axes incorrectly mixes tokens across batch samples without triggering shape errors.

---

## Check yourself

1. If X has shape (16, 50, 768) and W has shape (256, 768), what is the shape of X @ W.T?
2. Does batching across dimension 0 introduce cross-sample information leakage in a linear layer?

<details>
<summary>Answers</summary>

1. The output shape is (16, 50, 256).
2. No. Each sample is processed independently; the matrix multiply is block-diagonal across the batch axis.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](03_Broadcasting_Rules_and_the_Silent_Bugs_They_Cause.md)
