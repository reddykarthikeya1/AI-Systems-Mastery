# Lesson 11.28 — Stationary Distributions

> **Module 11:** Joint Distributions and Covariance · Lesson 28 of 29

---

## What you will be able to do after this lesson

- [ ] Compute stationary distribution pi = pi P.
- [ ] State conditions for ergodicity (irreducible, aperiodic).

## Prerequisites

- 11.27 Markov Chains and 05.12 Power Iteration.

---

## 1. The idea

A **stationary distribution** $\boldsymbol{\pi}$ satisfies $\boldsymbol{\pi} = \boldsymbol{\pi} P$ and $\sum \pi_i = 1$. For any irreducible, aperiodic (ergodic) Markov chain, regardless of initial state $\mathbf{p}_0$, the chain converges to $\boldsymbol{\pi}$ as $t \to \infty$.

---

## 2. Worked example

For $P = \begin{bmatrix} 0.8 & 0.2 \\ 0.4 & 0.6 \end{bmatrix}$: $\pi_1 = 0.8\pi_1 + 0.4\pi_2 \implies 0.2\pi_1 = 0.4\pi_2 \implies \pi_1 = 2\pi_2$. Since $\pi_1 + \pi_2 = 1$, $\boldsymbol{\pi} = [2/3, 1/3] \approx [0.667, 0.333]$.

---

## 3. Verify it in code

```python
import numpy as np
P = np.array([[0.8, 0.2], [0.4, 0.6]])
# Matrix power convergence
P_inf = np.linalg.matrix_power(P, 50)
pi = P_inf[0]
assert np.allclose(pi, [2.0/3.0, 1.0/3.0])
assert np.allclose(pi @ P, pi)
```

---

## 4. The mistake people actually make

Assuming periodic chains (e.g. deterministic cycle between 0 and 1) have a unique limiting distribution.

---

## Check yourself

1. What equation defines a stationary distribution pi for transition matrix P?
2. Does the starting distribution p_0 affect the asymptotic distribution of an ergodic Markov chain?

<details>
<summary>Answers</summary>

1. pi = pi P with sum pi_i = 1.
2. No, it converges to the unique stationary distribution pi regardless of p_0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](29_Module_Project_A_Gaussian_Mixture_Model_by_EM.md)
