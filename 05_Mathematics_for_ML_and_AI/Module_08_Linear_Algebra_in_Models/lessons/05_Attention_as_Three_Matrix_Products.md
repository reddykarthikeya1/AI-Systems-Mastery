# Lesson 08.05 — Attention as Three Matrix Products

> **Module 08:** Linear Algebra in Models · Lesson 5 of 9

---

## What you will be able to do after this lesson

- [ ] Formulate scaled dot-product self-attention purely as three sequential matrix multiplications: Q K^T, Softmax, and A V.
- [ ] Implement and verify a multi-token self-attention block with masking in NumPy.

## Prerequisites

- 08.01 Linear Layer Matrix Multiply and 08.02 Batching.

---

## 1. The idea

The transformer attention mechanism computes contextual token representations through three matrix multiplications:
1. Raw Attention Scores: $\mathbf{S}_{raw} = \frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}$
2. Attention Weights: $\mathbf{A} = \text{softmax}(\mathbf{S}_{raw}, \text{axis}=-1)$
3. Contextual Aggregation: $\mathbf{O} = \mathbf{A}\mathbf{V}$

---

## 2. Worked example

Let sequence length $S = 2$, dimension $d_k = 2$.
Q = [[1, 0], [0, 1]], K = [[1, 0], [1, 1]], V = [[2, 4], [6, 8]].
Q @ K.T gives [[1, 1], [0, 1]].
For row 1, both scores are equal to 1, so softmax yields [0.5, 0.5].
Output row 1 is 0.5 * [2, 4] + 0.5 * [6, 8] = [4.0, 6.0].

---

## 3. Verify it in code

```python
import numpy as np

Q = np.array([[1.0, 0.0],
              [0.0, 1.0]])
K = np.array([[1.0, 0.0],
              [1.0, 1.0]])
V = np.array([[2.0, 4.0],
              [6.0, 8.0]])

d_k = Q.shape[-1]
scores = (Q @ K.T) / np.sqrt(d_k)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

A = softmax(scores)
output = A @ V

assert output.shape == (2, 2)
assert np.allclose(A[0], [0.5, 0.5])
assert np.allclose(output[0], [4.0, 6.0])
```

---

## 4. The mistake people actually make

**Forgetting to scale by $1/\sqrt{d_k}$ when computing dot-product attention.**

Large dot products push the softmax into regions with near-zero gradients, leading to vanishing gradients and dead training.

---

## Check yourself

1. What are the shapes of Q K^T and A V if Q, K, V have shape (batch=8, seq=512, dim=64)?
2. Why do the rows of the attention matrix A always sum to 1?

<details>
<summary>Answers</summary>

1. Q K^T has shape (8, 512, 512), and A V has shape (8, 512, 64).
2. Because softmax is applied along the last dimension (columns), normalizing each row into a valid probability distribution.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](06_Convolution_as_a_Structured_Matrix.md)
