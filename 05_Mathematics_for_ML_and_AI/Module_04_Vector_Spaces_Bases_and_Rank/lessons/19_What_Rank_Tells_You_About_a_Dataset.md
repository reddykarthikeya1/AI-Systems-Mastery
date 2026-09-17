# Lesson 04.19 — What Rank Tells You About a Dataset

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 19 of 21

---

## What you will be able to do after this lesson

- [ ] Interpret matrix rank as the true effective dimensionality of a feature matrix.
- [ ] Detect exact feature redundancy in datasets.

## Prerequisites

- 04.16 Rank of a Matrix.

---

## 1. The idea

In a dataset matrix $X \in \mathbb{R}^{N \times D}$ ($N$ samples, $D$ features), if $\text{rank}(X) = k < D$, there are $D - k$ features that are exact linear combinations of other features. Storing all $D$ features wastes memory and introduces non-identifiability in linear models.

---

## 2. Worked example

Features: $x_1 = \text{temp in Celsius}$, $x_2 = \text{temp in Fahrenheit} = 1.8 x_1 + 32$. Feature matrix has rank 2 (including bias column), not 3. One feature is completely redundant.

---

## 3. Verify it in code

```python
import numpy as np
N = 10
celsius = np.linspace(0, 100, N)
bias = np.ones(N)
fahrenheit = 1.8 * celsius + 32.0

X = np.column_stack([bias, celsius, fahrenheit])
assert X.shape == (N, 3)
assert np.linalg.matrix_rank(X) == 2  # Not 3!
```

---

## 4. The mistake people actually make

Training linear regression with raw and derived features that create exact rank deficiency, causing singular matrix crashes.

---

## Check yourself

1. If a dataset has 100 features but rank 20, how many features are redundant?
2. What happens to (X^T X)^(-1) when X is rank deficient?

<details>
<summary>Answers</summary>

1. 80 features.
2. It is undefined (singular matrix cannot be inverted).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](20_Multicollinearity_as_Near_Rank_Deficiency.md)
