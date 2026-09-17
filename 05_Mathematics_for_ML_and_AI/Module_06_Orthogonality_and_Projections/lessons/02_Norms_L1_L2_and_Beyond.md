# Lesson 06.02 — Norms: L1, L2 and Beyond

> **Module 06:** Orthogonality and Projections · Lesson 2 of 18

---

## What you will be able to do after this lesson

- [ ] Distinguish L1 (Manhattan), L2 (Euclidean), and L-infinity norms.
- [ ] Connect L1 regularization to sparsity in Lasso regression.

## Prerequisites

- 06.01 The Dot Product.

---

## 1. The idea

A norm $\|\mathbf{x}\|$ maps vectors to non-negative lengths. $L_p = (\sum |x_i|^p)^{1/p}$. $L_1$ induces sparsity (sharp diamond unit ball), while $L_2$ penalizes large values smoothly (smooth circular unit ball).

---

## 2. Worked example

For $\mathbf{x} = [-3, 4]$: $L_1 = |-3| + |4| = 7$. $L_2 = \sqrt{(-3)^2 + 4^2} = 5$. $L_\infty = \max(|-3|, |4|) = 4$.

---

## 3. Verify it in code

```python
import numpy as np
x = np.array([-3.0, 4.0])
assert np.isclose(np.linalg.norm(x, ord=1), 7.0)
assert np.isclose(np.linalg.norm(x, ord=2), 5.0)
assert np.isclose(np.linalg.norm(x, ord=np.inf), 4.0)
```

---

## 4. The mistake people actually make

Using squared L2 norm when a proper metric distance is required (squared L2 violates triangle inequality).

---

## Check yourself

1. Why does L1 regularization produce sparse weights?
2. Which norm corresponds to max absolute coordinate?

<details>
<summary>Answers</summary>

1. Because the L1 ball has sharp corners on coordinate axes where level sets of loss first intersect.
2. The L-infinity norm.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](03_Angles_Cosine_Similarity_and_Correlation.md)
