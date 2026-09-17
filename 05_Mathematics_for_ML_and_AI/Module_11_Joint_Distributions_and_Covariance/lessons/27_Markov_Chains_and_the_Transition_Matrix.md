# Lesson 11.27 — Markov Chains and the Transition Matrix

> **Module 11:** Joint Distributions and Covariance · Lesson 27 of 29

---

## What you will be able to do after this lesson

- [ ] Define Markov property: P(X_t+1 | X_t, ..., X_0) = P(X_t+1 | X_t).
- [ ] Multiply state distribution vector by transition matrix P.

## Prerequisites

- 11.03 Conditional Distributions.

---

## 1. The idea

A **Markov Chain** satisfies the memoryless Markov property: the future depends only on the present, not the past. Its dynamics are governed by transition matrix $P_{ij} = P(X_{t+1} = j \mid X_t = i)$. Row vectors evolve as $\mathbf{p}_{t+1} = \mathbf{p}_t P$.

---

## 2. Worked example

Weather model: Sunny ($0$) or Rainy ($1$). $P = \begin{bmatrix} 0.8 & 0.2 \\ 0.4 & 0.6 \end{bmatrix}$. If today is Sunny ($[1, 0]$), tomorrow is $[0.8, 0.2]$. Day after tomorrow is $[0.8, 0.2] P = [0.72, 0.28]$.

---

## 3. Verify it in code

```python
import numpy as np
P = np.array([[0.8, 0.2], [0.4, 0.6]])
p0 = np.array([1.0, 0.0])
p1 = p0 @ P
p2 = p1 @ P
assert np.allclose(p1, [0.8, 0.2])
assert np.allclose(p2, [0.72, 0.28])
assert np.allclose(np.sum(P, axis=1), [1.0, 1.0])
```

---

## 4. The mistake people actually make

Transposing the transition matrix convention (row stochastic where rows sum to 1 vs column stochastic).

---

## Check yourself

1. What is the Markov property?
2. What must each row of a row-stochastic transition matrix sum to?

<details>
<summary>Answers</summary>

1. The future state is conditionally independent of past history given the current state.
2. Exactly 1.0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](28_Stationary_Distributions.md)
