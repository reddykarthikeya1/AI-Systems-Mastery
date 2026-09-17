# Lesson 06.05 — Orthogonal Complements

> **Module 06:** Orthogonality and Projections · Lesson 5 of 18

---

## What you will be able to do after this lesson

- [ ] Define orthogonal complement V_perp = {x : x . v = 0 for all v in V}.
- [ ] Decompose R^n into V direct sum V_perp.

## Prerequisites

- 06.04 Orthogonality and Subspaces (Module 04).

---

## 1. The idea

For subspace $V \subseteq \mathbb{R}^n$, its **orthogonal complement** $V^\perp$ consists of all vectors orthogonal to every vector in $V$. $\dim(V) + \dim(V^\perp) = n$, and every $\mathbf{x} \in \mathbb{R}^n$ uniquely decomposes as $\mathbf{x} = \mathbf{v} + \mathbf{v}^\perp$.

---

## 2. Worked example

In $\mathbb{R}^3$, let $V = \text{span}([0, 0, 1]^T)$ (z-axis). Then $V^\perp$ is the xy-plane $\text{span}([1, 0, 0]^T, [0, 1, 0]^T)$. For $\mathbf{x} = [2, 3, 5]^T$, $\mathbf{v} = [0, 0, 5]^T$ and $\mathbf{v}^\perp = [2, 3, 0]^T$.

---

## 3. Verify it in code

```python
import numpy as np
x = np.array([2.0, 3.0, 5.0])
v = np.array([0.0, 0.0, 5.0])
v_perp = np.array([2.0, 3.0, 0.0])
assert np.allclose(x, v + v_perp)
assert np.isclose(np.dot(v, v_perp), 0.0)
```

---

## 4. The mistake people actually make

Thinking V and V_perp can share non-zero vectors. Their intersection is strictly {0}.

---

## Check yourself

1. What is the intersection of a subspace V and its orthogonal complement V_perp?
2. What is dim(V) + dim(V_perp) in R^n?

<details>
<summary>Answers</summary>

1. Only the zero vector: V cap V_perp = {0}.
2. Exactly n.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](06_Projection_Onto_a_Line.md)
