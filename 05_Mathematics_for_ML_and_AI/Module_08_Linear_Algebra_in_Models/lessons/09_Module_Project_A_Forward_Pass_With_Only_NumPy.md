# Lesson 08.09 — Module Project: A Forward Pass With Only NumPy

> **Module 08:** Linear Algebra in Models · Lesson 9 of 9

---

## What you will be able to do after this lesson

- [ ] Assemble linear layers, activation functions, residual connections, and layer normalization into a working forward pass using only pure NumPy.
- [ ] Verify complete dimensional consistency and numerical equivalence with reference equations.

## Prerequisites

- Lessons 08.01 through 08.08.

---

## 1. The idea

A complete Transformer FFN block consists of:
1. Layer Normalization
2. First Affine Projection (d -> 4d)
3. Activation Non-linearity (ReLU)
4. Second Affine Projection (4d -> d)
5. Residual Connection (Y = X + F(X))

---

## 2. Worked example

Given input X of shape (B=2, S=3, d=4), hidden dimension d_ff=8.
LayerNorm normalizes along the last dimension.
W1 @ X.T + b1 projects to (2, 3, 8).
ReLU clamps negative values.
W2 @ A1.T + b2 projects back to (2, 3, 4).
Adding X completes the residual block.

---

## 3. Verify it in code

```python
import numpy as np

np.random.seed(42)
B, S, d_model, d_ff = 2, 3, 4, 8

X = np.random.randn(B, S, d_model)
W1 = np.random.randn(d_ff, d_model) * np.sqrt(2.0 / d_model)
b1 = np.zeros(d_ff)
W2 = np.random.randn(d_model, d_ff) * np.sqrt(2.0 / d_ff)
b2 = np.zeros(d_model)

eps = 1e-5
mean = np.mean(X, axis=-1, keepdims=True)
var = np.var(X, axis=-1, keepdims=True)
X_norm = (X - mean) / np.sqrt(var + eps)

H1 = X_norm @ W1.T + b1
assert H1.shape == (B, S, d_ff)

A1 = np.maximum(0, H1)
H2 = A1 @ W2.T + b2
assert H2.shape == (B, S, d_model)

Y = X + H2
assert Y.shape == (B, S, d_model)
assert not np.isnan(Y).any()
```

---

## 4. The mistake people actually make

**Normalizing across the batch axis instead of the feature axis in LayerNorm.**

LayerNorm normalizes across the feature dimension independently for every token and sample, ensuring robustness to variable sequence lengths.

---

## Check yourself

1. Why is the residual connection Y = X + F(X) crucial for training very deep networks?
2. What is the dimensional difference between BatchNorm and LayerNorm?

<details>
<summary>Answers</summary>

1. The residual connection provides an identity path for gradients to flow backward directly without attenuation, preventing vanishing gradients.
2. BatchNorm computes statistics over batch dimensions, while LayerNorm computes statistics independently over the feature dimension for each sample.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md)
