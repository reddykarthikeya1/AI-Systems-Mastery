# Lesson 08.07 — Embeddings as Lookup Into a Matrix

> **Module 08:** Linear Algebra in Models · Lesson 7 of 9

---

## What you will be able to do after this lesson

- [ ] Prove that embedding lookup is mathematically equivalent to multiplying a one-hot vector by an embedding matrix.
- [ ] Demonstrate token index indexing vs one-hot matrix multiplication in NumPy.

## Prerequisites

- 08.01 Linear Layer Matrix Multiply.

---

## 1. The idea

An embedding layer with weight matrix $\mathbf{E} \in \mathbb{R}^{V \times d}$ is formally a linear layer applied to a one-hot vector $\mathbf{e}_i$:
$$\mathbf{y} = \mathbf{e}_i^T \mathbf{E} = \mathbf{E}[i, :]$$
Because $\mathbf{e}_i$ has only a single 1 at index $i$, the matrix product selects row $i$ of $\mathbf{E}$. Hardware executes this as an O(1) memory lookup.

---

## 2. Worked example

Let vocabulary size V = 3, embedding dimension d = 2.
E has rows: [0.1, 0.2], [1.5, -0.5], [-2.0, 3.0].
For token ID 1, one-hot vector is [0, 1, 0].
e_1 @ E = [1.5, -0.5], matching E[1].

---

## 3. Verify it in code

```python
import numpy as np

E = np.array([
    [0.1,  0.2, -0.3],
    [1.0,  2.0,  3.0],
    [-1.0, 0.5,  0.2],
    [4.0, -2.0,  1.1]
])

token_id = 2
emb_lookup = E[token_id]

one_hot = np.zeros(4)
one_hot[token_id] = 1.0
emb_matmul = one_hot @ E

assert np.allclose(emb_lookup, emb_matmul)
assert np.allclose(emb_lookup, [-1.0, 0.5, 0.2])
```

---

## 4. The mistake people actually make

**Materializing one-hot vectors in memory for large vocabularies.**

When vocabulary size is V = 128,000, materializing one-hot vectors consumes gigabytes of memory storing zeros. Gathering rows directly by index avoids this overhead.

---

## Check yourself

1. Why is embedding lookup implemented as table gathering instead of matrix multiplication?
2. What is the mathematical relation between one-hot matrix multiplication and embedding lookup?

<details>
<summary>Answers</summary>

1. Because one-hot multiplication spends 99.99% of operations multiplying by zero; table lookup reads only the needed row in O(d) memory bandwidth.
2. They are mathematically identical: e_i^T E extracts exactly row i of E.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](08_Where_Numerical_Precision_Bites.md)
