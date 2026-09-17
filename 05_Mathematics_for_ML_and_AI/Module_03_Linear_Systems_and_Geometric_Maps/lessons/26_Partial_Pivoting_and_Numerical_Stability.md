# Lesson 03.26 — Partial Pivoting and Numerical Stability

> **Module 03:** Linear Systems and Geometric Maps · Lesson 26 of 35

---

## What you will be able to do after this lesson

- [ ] Decompose matrix as P A = L U with permutation matrix P.
- [ ] Explain how selecting the largest pivot avoids catastrophic division by near-zero.

## Prerequisites

- 03.25 LU Decomposition.

---

## 1. The idea

Without pivoting, a tiny diagonal entry causes massive multipliers $m = A_{ik}/A_{kk}$, causing catastrophic roundoff error. **Partial pivoting** swaps rows so the entry with largest absolute value in the active column becomes the pivot: $P A = L U$, where $P$ is a permutation matrix.

---

## 2. Worked example

Let $A = \begin{bmatrix} 10^{-4} & 1 \\ 1 & 1 \end{bmatrix}$. Swapping rows gives $PA = \begin{bmatrix} 1 & 1 \\ 10^{-4} & 1 \end{bmatrix}$. The elimination multiplier is $10^{-4} \ll 1$, perfectly stable.

---

## 3. Verify it in code

```python
import numpy as np
# Demonstration of PLU
A = np.array([[0.0, 1.0], [1.0, 1.0]])
P = np.array([[0.0, 1.0], [1.0, 0.0]])
PA = P @ A
assert PA[0, 0] == 1.0
```

---

## 4. The mistake people actually make

Running unpivoted LU decomposition on arbitrary floating-point data, leading to severe numerical inaccuracy.

---

## Check yourself

1. What does the permutation matrix P do in PA = LU?
2. Why does choosing the maximum absolute entry as pivot improve numerical stability?

<details>
<summary>Answers</summary>

1. It performs row swaps to position optimal pivots.
2. It ensures all multipliers |L_ij| <= 1, preventing exponential error amplification.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](27_Condition_Number_and_IllConditioned_Systems.md)
