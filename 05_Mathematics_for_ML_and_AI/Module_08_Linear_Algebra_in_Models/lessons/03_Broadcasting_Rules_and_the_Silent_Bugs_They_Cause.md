# Lesson 08.03 — Broadcasting Rules and the Silent Bugs They Cause

> **Module 08:** Linear Algebra in Models · Lesson 3 of 9

---

## What you will be able to do after this lesson

- [ ] State the two universal broadcasting rules and predict the resulting output shape of binary operations.
- [ ] Identify and debug silent 1D vs 2D column-vector broadcasting bugs.

## Prerequisites

- Tensor dimensions and array indexing.

---

## 1. The idea

Broadcasting allows arithmetic operations between arrays of different shapes without copying data in memory.
1. Alignment: Shapes are aligned from right to left (trailing dimensions first).
2. Compatibility: Two dimensions are compatible if they are equal, or one of them is 1. If one array has fewer dimensions, prepending 1s extends its shape.

---

## 2. Worked example

Adding a 2D column vector of shape $(3, 1)$ to a 1D vector of length 3:
Array A shape $(3, 1)$, Array B shape $(3,)$.
During addition $A + B$, B is aligned as $(1, 3)$.
Both stretch to $(3, 3)$, creating an outer sum matrix of 9 elements instead of an elementwise vector!

---

## 3. Verify it in code

```python
import numpy as np

a = np.array([[10], [20], [30]])  # Shape (3, 1)
b = np.array([1, 2, 3])            # Shape (3,)

buggy_sum = a + b
assert buggy_sum.shape == (3, 3)

correct_sum = a + b[:, np.newaxis]
assert correct_sum.shape == (3, 1)
assert np.allclose(correct_sum, np.array([[11], [22], [33]]))
```

---

## 4. The mistake people actually make

**Subtracting model predictions of shape (N, 1) from targets of shape (N,).**

In regression loss computation, broadcasting creates an (N, N) matrix of all pairwise squared differences instead of N elementwise errors, silently skewing gradients.

---

## Check yourself

1. What is the broadcasted shape of array X of shape (4, 1, 8) and array Y of shape (2, 8)?
2. Why does PyTorch emit a warning when computing MSELoss on shapes (N, 1) and (N,)?

<details>
<summary>Answers</summary>

1. The shape is (4, 2, 8). Y is aligned as (1, 2, 8), and the size-1 dimensions stretch to 4 and 2.
2. Because broadcasting expands the inputs to an (N, N) matrix of all pairwise squared differences instead of N elementwise errors.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](04_Weight_Initialization_and_Spectral_Norm.md)
