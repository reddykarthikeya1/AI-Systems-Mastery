# Lesson 01.08 — Cartesian Products and Tuples

> **Module 01:** Set Language for Machine Learning · Lesson 8 of 25

---

## What you will be able to do after this lesson

- [ ] Form the Cartesian product of two sets and compute its size.
- [ ] Describe a feature space as a product of per-feature value sets, and compute how many distinct points it contains.

## Prerequisites

- [Lesson 01.02](02_Set_Notation_Membership_and_Equality.md) - notation.

---

## 1. The idea

The **Cartesian product** `A × B` is the set of all ordered pairs with the first
component from A and the second from B:

    A × B = { (a, b) : a ∈ A, b ∈ B }

Its size is `|A| × |B|` - one pair for each independent choice of a and b.

The word **ordered** is doing work. `(a, b)` and `(b, a)` are different pairs,
and `A × B ≠ B × A` unless A and B are equal. This is the first structure in
this module where order matters, and it matters because a tuple's positions
carry meaning: the first slot is the age, the second is the income.

`ℝ²` is `ℝ × ℝ`, the plane. `ℝⁿ` is the n-fold product, and it is the set your
feature vectors live in. That is the connection this whole module is building
toward: **a feature space is a Cartesian product of per-feature value sets**,
and a dataset is a finite subset of it.

## 2. Worked example

`A = {1, 2}` (two values of a binary flag), `B = {red, green, blue}` (three
colours).

    A × B = { (1,red), (1,green), (1,blue), (2,red), (2,green), (2,blue) }

Size: `|A| × |B| = 2 × 3 = 6` ✓.

The product is not commutative. `B × A` contains `(red, 1)`, which is a
different object from `(1, red)`:

    (1, red) ∈ A × B  but  (1, red) ∉ B × A

Now three features: a binary flag (2 values), a colour (3 values), and a size
in {S, M, L} (3 values). The space of possible rows is

    2 × 3 × 3 = 18 distinct combinations.

A dataset of 1,000 rows over these three features must therefore contain
repeats - there are only 18 distinct points available. That is worth knowing
before you wonder why a model cannot separate them.

## 3. Verify it in code

```python
from itertools import product

A = {1, 2}
B = {"red", "green", "blue"}

AB = set(product(A, B))
assert len(AB) == len(A) * len(B) == 6
assert (1, "red") in AB

# Ordered pairs: the product is not commutative.
BA = set(product(B, A))
assert ("red", 1) in BA
assert ("red", 1) not in AB
assert AB != BA

# A three-feature space.
flag, colour, size = {0, 1}, {"red", "green", "blue"}, {"S", "M", "L"}
space = set(product(flag, colour, size))
assert len(space) == 2 * 3 * 3 == 18

# A dataset is a finite subset of the feature space.
dataset = [(1, "red", "S"), (0, "blue", "L"), (1, "red", "S")]
assert all(row in space for row in dataset)
assert len(set(dataset)) == 2, "1000 rows over 18 points must repeat"

# The product with the empty set is empty: no first component to choose.
assert set(product(A, set())) == set()
```

## 4. The mistake people actually make

**Assuming a product of one-hot encodings is the same size as the raw space.**

Three categorical features with 3, 4 and 5 levels describe `3 × 4 × 5 = 60`
distinct combinations. One-hot encoding them produces `3 + 4 + 5 = 12` columns -
a *sum*, not a product.

That is not a contradiction, and mixing the two up causes real confusion. The
12 columns span a space with far more than 60 points, but only 60 of them are
*valid*: exactly one entry per feature group may be 1. A linear model over those
12 columns cannot represent an interaction between colour and size, because it
has no parameter for the combination - only one per level.

If you need the interaction, you have to build the product feature explicitly,
and then you are back to 60 columns. The sum is cheap and additive; the product
is expressive and expensive. Knowing which one your encoding gave you is the
difference between a model that can express what you want and one that cannot.

---

## Check yourself

1. `|A| = 4`, `|B| = 0`. What is `|A × B|`?
2. Is `(2, 3) ∈ {1,2} × {2,3}`? Is `(3, 2)`?
3. Four categorical features with 2, 3, 3 and 10 levels. How many distinct rows are possible, and how many one-hot columns?

<details>
<summary>Answers</summary>

1. 0. There is no second component available, so no pairs can be formed.
2. `(2, 3)` is: 2 is in the first set and 3 in the second. `(3, 2)` is not: 3 is not a member of `{1, 2}`.
3. 2 × 3 × 3 × 10 = 180 distinct rows, and 2 + 3 + 3 + 10 = 18 one-hot columns. The first is a product, the second a sum.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](07_Power_Sets_and_Counting_Subsets.md) · [Module README](../README.md) · [Next →](09_Relations_as_Subsets_of_a_Product.md)
