# Lesson 01.07 — Power Sets and Counting Subsets

> **Module 01:** Set Language for Machine Learning · Lesson 7 of 25

---

## What you will be able to do after this lesson

- [ ] Construct the power set of a small set and state its size without enumerating it.
- [ ] Explain why exhaustive feature-subset search is infeasible, with a concrete number.

## Prerequisites

- [Lesson 01.03](03_Subsets_Supersets_and_the_Empty_Set.md) - subsets.

---

## 1. The idea

The **power set** of A, written `P(A)` or `2^A`, is the set of *all* subsets of
A - including `∅` and A itself.

For `A = {a, b}`:

    P(A) = { ∅, {a}, {b}, {a, b} }

Note that `P(A)` is a set whose members are sets. `{a} ∈ P(A)` is true;
`a ∈ P(A)` is false.

**Its size is `2^|A|`**, and the reason is worth internalising because it is the
standard counting argument. To build a subset you make one independent yes/no
decision per element: is it in? With n elements that is n independent binary
choices, so 2 × 2 × ... × 2 = 2ⁿ outcomes, and each outcome is a distinct
subset.

That correspondence is exact: subsets of an n-element set are in bijection with
n-bit binary strings. It is how you enumerate them in code, and it is why the
notation `2^A` is used at all.

The consequence for ML: "try every subset of features" is a power-set search.
With 20 features that is about a million models; with 50 it is 10^15.

## 2. Worked example

`A = {x, y, z}`, so `|A| = 3` and `|P(A)| = 2³ = 8`.

Enumerate by binary counting, one bit per element, in the order (x, y, z):

| Bits | Subset |
| :--- | :--- |
| 000 | ∅ |
| 001 | {z} |
| 010 | {y} |
| 011 | {y, z} |
| 100 | {x} |
| 101 | {x, z} |
| 110 | {x, y} |
| 111 | {x, y, z} |

Eight rows, matching 2³. Count the subsets by size: one of size 0, three of
size 1, three of size 2, one of size 3 - which are the binomial coefficients
1, 3, 3, 1, and they sum to 8.

Now the scale. 20 features gives 2²⁰ = 1,048,576 subsets. If fitting one model
takes a second, exhaustive search takes about 12 days. At 50 features it is
2⁵⁰ ≈ 1.1 × 10¹⁵ - around 35 million years.

## 3. Verify it in code

```python
from itertools import chain, combinations

def power_set(items):
    items = sorted(items)
    return [set(c) for n in range(len(items) + 1)
            for c in combinations(items, n)]

A = {"x", "y", "z"}
subsets = power_set(A)

assert len(subsets) == 2 ** len(A) == 8
assert set() in subsets            # the empty set is always a member
assert A in subsets                # so is the set itself
assert {"x", "y"} in subsets

# Members of a power set are SETS, not elements.
assert {"x"} in subsets
assert "x" not in subsets

# Sizes follow the binomial coefficients and sum to 2^n.
from math import comb
by_size = [sum(1 for s in subsets if len(s) == k) for k in range(len(A) + 1)]
assert by_size == [comb(3, k) for k in range(4)] == [1, 3, 3, 1]
assert sum(by_size) == 8

# The bijection with binary strings.
elements = sorted(A)
from_bits = {frozenset(e for i, e in enumerate(elements) if mask >> i & 1)
             for mask in range(2 ** len(elements))}
assert len(from_bits) == 8
assert from_bits == {frozenset(s) for s in subsets}

# Why exhaustive feature search does not scale.
assert 2 ** 20 == 1_048_576
assert 2 ** 50 > 10 ** 15
```

## 4. The mistake people actually make

**Treating exhaustive subset search as merely slow.**

"Try all feature combinations and keep the best" is a reasonable-sounding plan
that is not slow but *impossible*, and the difference matters. Slow gets fixed
with a bigger machine; 2⁵⁰ does not. Doubling your compute buys you exactly one
more feature.

The second, subtler error: even if you could run it, selecting the best of a
million models on a validation set overfits that set badly. With enough
candidates, something scores well by chance. The winner's validation score is
then an optimistic estimate of its true performance - which is why a held-out
test set must not be the thing you selected on.

The practical alternatives are greedy (forward or backward stepwise), or
regularisation that shrinks coefficients toward zero, both of which search a
tiny part of the power set on purpose.

---

## Check yourself

1. What is `|P(A)|` for `|A| = 6`? And `|P(P(A))|` for `|A| = 2`?
2. Is `∅ ∈ P(A)` true? Is `∅ ⊆ P(A)` true?
3. You add one feature to a 30-feature exhaustive search. By what factor does the work grow?

<details>
<summary>Answers</summary>

1. 2⁶ = 64. For the second: `|P(A)| = 4`, so `|P(P(A))| = 2⁴ = 16.
2. Both are true, for different reasons. `∅ ∈ P(A)` because the empty set is one of the subsets of A. `∅ ⊆ P(A)` because the empty set is a subset of every set, including this one.
3. It doubles. Each new feature adds one independent in/out decision, multiplying the number of subsets by 2.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](06_De_Morgans_Laws.md) · [Module README](../README.md) · [Next →](08_Cartesian_Products_and_Tuples.md)
