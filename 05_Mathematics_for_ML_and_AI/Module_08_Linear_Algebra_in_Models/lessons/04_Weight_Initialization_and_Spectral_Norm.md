# Lesson 08.04 — Weight Initialization and Spectral Norm

> **Module 08:** Linear Algebra in Models · Lesson 4 of 9

---

## What you will be able to do after this lesson

- [ ] Derive Xavier/Glorot variance scaling to preserve activation variance across deep linear layers.
- [ ] Compute the spectral norm of a weight matrix using SVD and power iteration in NumPy.

## Prerequisites

- 05.01 Eigenvalues and SVD singular values.

---

## 1. The idea

In deep networks, activations $\mathbf{x}^{(l+1)} = \mathbf{W}^{(l)}\mathbf{x}^{(l)}$ undergo repeated matrix multiplications.
The **spectral norm** $\|\mathbf{W}\|_2 = \sigma_{\max}(\mathbf{W})$ is the largest singular value of $\mathbf{W}$. It defines the exact Lipschitz constant of the linear map: $\|\mathbf{W}\mathbf{x}\| \le \sigma_{\max} \|\mathbf{x}\|$. Spectral normalization divides $\mathbf{W}$ by $\sigma_{\max}$ to guarantee numerical stability.

---

## 2. Worked example

Consider a $2 \times 2$ diagonal weight matrix with entries 3.0 and 0.5.
The singular values are $\sigma_1 = 3.0$ and $\sigma_2 = 0.5$.
The spectral norm is 3.0.
Normalizing by $\sigma_{\max}$ produces a matrix with singular values 1.0 and 1/6.

---

## 3. Verify it in code

```python
import numpy as np

W = np.array([[3.0, 0.0],
              [0.0, 0.5]])

singular_values = np.linalg.svd(W, compute_uv=False)
spectral_norm = singular_values[0]
assert np.isclose(spectral_norm, 3.0)

W_spectral = W / spectral_norm
assert np.isclose(np.linalg.svd(W_spectral, compute_uv=False)[0], 1.0)
```

---

## 4. The mistake people actually make

**Initializing weights with uniform random values without scaling by $1/\sqrt{d_{in}}$.**

In a layer with $d_{in} = 1024$, standard unit variance weights cause output variance to scale by 1024 at each layer, rapidly overflowing float16 into inf/NaN.

---

## Check yourself

1. What is the mathematical definition of the spectral norm of a matrix W?
2. Why is spectral normalization used in deep networks?

<details>
<summary>Answers</summary>

1. The spectral norm is the maximum singular value of W, representing the supremum of ||W x|| / ||x|| for non-zero vectors x.
2. It bounds the Lipschitz constant of the network layer to at most 1, preventing exploding activations and gradients.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](05_Attention_as_Three_Matrix_Products.md)
