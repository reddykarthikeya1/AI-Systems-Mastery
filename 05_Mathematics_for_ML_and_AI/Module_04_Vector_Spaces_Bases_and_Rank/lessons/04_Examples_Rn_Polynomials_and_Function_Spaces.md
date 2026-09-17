# Lesson 04.04 — Examples: Rn, Polynomials and Function Spaces

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 4 of 21

---

## What you will be able to do after this lesson

- [ ] Recognize polynomials P_n and continuous functions C[a, b] as vector spaces.
- [ ] Represent polynomial addition as vector addition of coefficients.

## Prerequisites

- 04.03 Vector Space Axioms.

---

## 1. The idea

Vector spaces extend far beyond $\mathbb{R}^n$. The set of polynomials of degree $\le n$ forms a vector space of dimension $n+1$, where vectors are polynomial coefficient lists. The set of continuous functions $C[a, b]$ is an infinite-dimensional vector space.

---

## 2. Worked example

Let $p(x) = 2 + 3x$ and $q(x) = 1 - x + 4x^2$. In degree-2 basis $\{1, x, x^2\}$, $\mathbf{p} = [2, 3, 0]^T$ and $\mathbf{q} = [1, -1, 4]^T$. Sum $p+q = [3, 2, 4]^T \implies 3 + 2x + 4x^2$.

---

## 3. Verify it in code

```python
import numpy as np
# Polynomial coefficients in ascending powers [c0, c1, c2]
p = np.array([2.0, 3.0, 0.0])
q = np.array([1.0, -1.0, 4.0])
pq_sum = p + q
assert np.allclose(pq_sum, [3.0, 2.0, 4.0])
```

---

## 4. The mistake people actually make

Restricting linear algebra intuition to physical 3D space rather than recognizing functions as vectors.

---

## Check yourself

1. What is the dimension of the space of polynomials of degree at most d?
2. Is the set of all continuous functions C[0, 1] finite dimensional?

<details>
<summary>Answers</summary>

1. d + 1.
2. No, it is infinite dimensional.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](05_Subspaces_and_How_to_Test_for_One.md)
