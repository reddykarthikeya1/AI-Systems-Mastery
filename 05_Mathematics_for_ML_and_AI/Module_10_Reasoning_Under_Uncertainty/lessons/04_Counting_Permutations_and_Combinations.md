# Lesson 10.04 — Counting: Permutations and Combinations

> **Module 10:** Reasoning Under Uncertainty · Lesson 4 of 41

---

## What you will be able to do after this lesson

- [ ] Compute permutations P(n, k) = n! / (n-k)! and combinations C(n, k) = n! / (k! (n-k)!).
- [ ] Calculate discrete uniform probabilities by counting.

## Prerequisites

- Basic combinatorics.

---

## 1. The idea

When outcomes in $\Omega$ are equally likely, $P(E) = |E| / |\Omega|$.
- **Permutations** (order matters): $P(n, k) = \frac{n!}{(n-k)!}$.
- **Combinations** (order does not matter): $\binom{n}{k} = \frac{n!}{k!(n-k)!}$.

---

## 2. Worked example

Choosing 2 items from 4 $\{A, B, C, D\}$: $\binom{4}{2} = \frac{4 \times 3}{2 \times 1} = 6$. The pairs are AB, AC, AD, BC, BD, CD.

---

## 3. Verify it in code

```python
import numpy as np
from math import comb, perm
assert comb(4, 2) == 6
assert perm(4, 2) == 12
assert perm(4, 2) == comb(4, 2) * 2
```

---

## 4. The mistake people actually make

Using permutations when combinations are required (e.g. counting subsets without order).

---

## Check yourself

1. Does order matter in combinations C(n, k)?
2. How many ways can 5 objects be ordered?

<details>
<summary>Answers</summary>

1. No, combinations count unordered subsets.
2. 5! = 120 ways.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](05_Conditional_Probability.md)
