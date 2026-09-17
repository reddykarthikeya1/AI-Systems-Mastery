# Lesson 04.03 — The Vector Space Axioms

> **Module 04:** Vector Spaces, Bases and Rank · Lesson 3 of 21

---

## What you will be able to do after this lesson

- [ ] State the 8 vector space axioms (closure, associativity, identity, inverse, distributivity).
- [ ] Verify vector space properties on numerical arrays.

## Prerequisites

- 04.02 Vector Addition and Scalar Multiplication.

---

## 1. The idea

A **vector space** $V$ over field $\mathbb{R}$ is a set closed under addition and scalar multiplication satisfying 8 axioms: commutativity, associativity, zero element $\mathbf{0}$, additive inverse $-\mathbf{v}$, distributivity over scalars and vectors, and unit scalar multiplication.

---

## 2. Worked example

In $\mathbb{R}^2$, the zero vector is $[0, 0]^T$. For any $\mathbf{v} = [x, y]^T$, $\mathbf{v} + \mathbf{0} = [x+0, y+0]^T = \mathbf{v}$, and $\mathbf{v} + (-\mathbf{v}) = \mathbf{0}$.

---

## 3. Verify it in code

```python
import numpy as np
v = np.array([3.5, -2.1])
zero = np.zeros(2)
assert np.allclose(v + zero, v)
assert np.allclose(v + (-v), zero)
# Distributivity: c * (u + v) == c * u + c * v
u = np.array([1.0, 4.0])
c = 3.0
assert np.allclose(c * (u + v), c * u + c * v)
```

---

## 4. The mistake people actually make

Assuming any set of tuples forms a vector space without checking closure under addition and scalar multiplication.

---

## Check yourself

1. What must every vector space contain?
2. If a set does not contain the zero vector, can it be a vector space?

<details>
<summary>Answers</summary>

1. The zero vector (additive identity).
2. No, containing the zero vector is an essential axiom.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](04_Examples_Rn_Polynomials_and_Function_Spaces.md)
