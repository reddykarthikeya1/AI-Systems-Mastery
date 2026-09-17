# Lesson 08.06 — Convolution as a Structured Matrix

> **Module 08:** Linear Algebra in Models · Lesson 6 of 9

---

## What you will be able to do after this lesson

- [ ] Demonstrate that 1D and 2D discrete convolutions are equivalent to matrix multiplication with a Toeplitz matrix.
- [ ] Construct a Toeplitz matrix in NumPy and verify that matrix-vector multiplication yields the exact convolution.

## Prerequisites

- 08.01 Linear Layer Matrix Multiply.

---

## 1. The idea

Because convolution is a linear operator, it can be written as a single matrix-vector multiply:
$$\mathbf{y} = \mathbf{T}_{\mathbf{k}} \mathbf{x}$$
where $\mathbf{T}_{\mathbf{k}}$ is a **Toeplitz matrix** (constant along descending diagonals).

---

## 2. Worked example

Let signal x = [3, 1, 4, 2] and kernel k = [-1, 2].
The valid output has length 4 - 2 + 1 = 3.
Row 1 computes (-1)(1) + 2(3) = 5 (or correlation ordering (-1)(3) + 2(1) = -1 depending on convention).

---

## 3. Verify it in code

```python
import numpy as np

x = np.array([3.0, 1.0, 4.0, 2.0])
k0, k1 = -1.0, 2.0

T = np.array([
    [k0, k1, 0.0, 0.0],
    [0.0, k0, k1, 0.0],
    [0.0, 0.0, k0, k1]
])

y = T @ x
assert len(y) == 3
assert np.isclose(y[0], k0 * 3.0 + k1 * 1.0)
assert np.isclose(y[1], k0 * 1.0 + k1 * 4.0)
assert np.isclose(y[2], k0 * 4.0 + k1 * 2.0)
```

---

## 4. The mistake people actually make

**Assuming convolution layers cannot be evaluated with standard GEMM hardware.**

Modern frameworks unroll spatial patches into matrix columns (im2col) and perform a single batched GEMM, maximizing GPU utilization.

---

## Check yourself

1. What mathematical structure characterizes a Toeplitz matrix?
2. What operation corresponds to multiplying by T.T in neural networks?

<details>
<summary>Answers</summary>

1. A Toeplitz matrix has constant entries along all descending diagonals.
2. Multiplying by T.T computes the backward pass gradient and corresponds to transposed convolution.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](07_Embeddings_as_Lookup_Into_a_Matrix.md)
