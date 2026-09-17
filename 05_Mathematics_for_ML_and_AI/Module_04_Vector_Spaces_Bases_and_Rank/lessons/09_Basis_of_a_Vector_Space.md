# Lesson 04.09 — Basis of a Vector Space

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 9 of 21

---

## What you will be able to do after this lesson

- [ ] Define a basis as a minimal spanning set and maximal linearly independent set.
- [ ] Verify whether a candidate set forms a basis for R^n.

## Prerequisites

- 04.06 Span and 04.07 Linear Independence.

---

## 1. The idea

A set of vectors $\mathcal{B} = \{\mathbf{v}_1, \dots, \mathbf{v}_n\}$ is a **basis** for vector space $V$ if:
1. $\mathcal{B}$ is linearly independent.
2. $\text{span}(\mathcal{B}) = V$.
Every vector $\mathbf{x} \in V$ can be expressed uniquely as a linear combination of basis vectors.

---

## 2. Worked example

In $\mathbb{R}^2$, the standard basis is $\mathbf{e}_1 = [1, 0]^T, \mathbf{e}_2 = [0, 1]^T$. An alternative basis is $\mathbf{b}_1 = [1, 1]^T, \mathbf{b}_2 = [1, -1]^T$. Any $\mathbf{x} = [x, y]^T$ uniquely decomposes as $\frac{x+y}{2}\mathbf{b}_1 + \frac{x-y}{2}\mathbf{b}_2$.

---

## 3. Verify it in code

```python
import numpy as np
b1 = np.array([1.0, 1.0])
b2 = np.array([1.0, -1.0])
B = np.column_stack([b1, b2])

# Invertible B confirms linearly independent and spanning (valid basis)
assert np.linalg.matrix_rank(B) == 2
assert not np.isclose(np.linalg.det(B), 0.0)
```

---

## 4. The mistake people actually make

Assuming a vector space has only one basis. Every non-trivial vector space has infinitely many different bases.

---

## Check yourself

1. Can a basis contain redundant vectors?
2. Is the representation of a vector in a given basis unique?

<details>
<summary>Answers</summary>

1. No, a basis is by definition a minimal spanning set.
2. Yes, coordinates in a given basis are strictly unique.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](10_Dimension_and_Why_It_Is_Well_Defined.md)
