# Lesson 05.12 — Power Iteration and How PageRank Works

> **Module 05:** Spectral Thinking and Diagonalization · Lesson 12 of 13

---

## What you will be able to do after this lesson

- [ ] Implement power iteration to compute dominant eigenvalue and eigenvector.
- [ ] Explain PageRank as finding the stationary eigenvector of a Markov transition matrix.

## Prerequisites

- 05.08 Matrix Powers and 05.11 Spectral Theorem.

---

## 1. The idea

Power iteration computes the dominant eigenvector of $A$. Starting from a random vector $\mathbf{b}_0$, it repeatedly computes $\mathbf{b}_{k+1} = \frac{A\mathbf{b}_k}{\|A\mathbf{b}_k\|}$. By the Perron-Frobenius theorem, for a positive stochastic matrix, the dominant eigenvalue is $\lambda_1 = 1$, and its eigenvector is the stationary distribution $\mathbf{p} = M\mathbf{p}$ (PageRank).

---

## 2. Worked example

Let $M = \begin{bmatrix} 0.8 & 0.3 \\ 0.2 & 0.7 \end{bmatrix}$ (columns sum to 1). Dominant eigenvalue is 1.0. Stationary vector satisfies $0.8 p_1 + 0.3 p_2 = p_1 \implies 0.3 p_2 = 0.2 p_1 \implies p_1 / p_2 = 3/2$. Normalized: $\mathbf{p} = [0.6, 0.4]^T$.

---

## 3. Verify it in code

```python
import numpy as np

M = np.array([[0.8, 0.3], [0.2, 0.7]])

# Power iteration
b = np.array([0.5, 0.5])
for _ in range(50):
    b = M @ b
    b = b / np.sum(b)

assert np.allclose(b, [0.6, 0.4], atol=1e-5)
assert np.allclose(M @ b, b)
```

---

## 4. The mistake people actually make

Failing to normalize at each iteration, which causes exponential numerical overflow or underflow.

---

## Check yourself

1. What governs the rate of convergence of power iteration?
2. What is the dominant eigenvalue of a column-stochastic matrix?

<details>
<summary>Answers</summary>

1. The ratio |lambda_2 / lambda_1|: smaller ratios converge faster.
2. It is always exactly 1.0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](13_Module_Project_Spectral_Clustering_From_Scratch.md)
