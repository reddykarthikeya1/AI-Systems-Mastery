# Lesson 01.15 — Indexed Families and Big Unions

> **Module 01:** Set Language for Machine Learning · Lesson 15 of 25

---

## What you will be able to do after this lesson

- [ ] Read and evaluate an indexed union or intersection over a finite or infinite index set.
- [ ] Use an indexed family to express a per-group computation, and state what the union and intersection each mean there.

## Prerequisites

- [Lesson 01.04](04_Union_Intersection_and_Difference.md) - union and intersection.

---

## 1. The idea

When there are more than two sets, naming them A, B, C runs out. An **indexed
family** `{A_i}` for `i ∈ I` gives one set per index, and the index set I may be
finite or infinite.

    ⋃_{i ∈ I} A_i = { x : x ∈ A_i for at least one i }
    ⋂_{i ∈ I} A_i = { x : x ∈ A_i for every i }

The union is an "exists" and the intersection is a "for all" - which is exactly
the quantifier distinction, and it explains their edge behaviour: over an empty
index set the union is `∅` (nothing exists to witness membership) while the
intersection is everything (vacuously, no constraint is violated). The second is
why an intersection over no sets is usually left undefined in practice, or taken
relative to a universe.

De Morgan generalises unchanged:

    (⋃ A_i)ᶜ = ⋂ A_iᶜ
    (⋂ A_i)ᶜ = ⋃ A_iᶜ

This is the natural language for grouped data: with one set per group, the union
is "everything seen in any group" and the intersection is "present in every
group". A **nested** family, where `A_1 ⊇ A_2 ⊇ ...`, appears whenever a
threshold tightens - the sets shrink as the requirement rises.

## 2. Worked example

Let `A_i = { x ∈ ℤ : 0 ≤ x ≤ i }` for `i ∈ {1, 2, 3}`.

    A_1 = {0, 1}
    A_2 = {0, 1, 2}
    A_3 = {0, 1, 2, 3}

    ⋃ A_i = {0, 1, 2, 3}    (= A_3, since the family is increasing)
    ⋂ A_i = {0, 1}          (= A_1, for the same reason)

A nested family in the other direction: `B_i = { x ∈ ℝ : 0 < x < 1/i }`.

    B_1 = (0, 1),  B_2 = (0, 0.5),  B_3 = (0, 1/3), ...

What is `⋂_{i=1}^{∞} B_i`? A real number x is in the intersection only if
`0 < x < 1/i` for *every* i. But for any fixed `x > 0` there is an i with
`1/i < x`, so x fails at that index. Hence

    ⋂ B_i = ∅

Every individual `B_i` is non-empty, and the intersection of all of them is
empty. This surprises people, and it is the same phenomenon as a sequence of
shrinking confidence intervals collapsing to a point.

## 3. Verify it in code

```python
# Finite increasing family.
A = {i: set(range(0, i + 1)) for i in (1, 2, 3)}
assert A[1] == {0, 1} and A[3] == {0, 1, 2, 3}

union = set().union(*A.values())
intersection = set(A[1]).intersection(*A.values())
assert union == {0, 1, 2, 3} == A[3]
assert intersection == {0, 1} == A[1]

# Nested, shrinking family: the intersection empties out.
def B(i, grid):
    return {x for x in grid if 0 < x < 1 / i}

grid = [k / 1000 for k in range(1, 1001)]
assert B(1, grid) != set()
assert B(100, grid) != set()
common = set(grid)
for i in range(1, 2001):
    common &= B(i, grid)
assert common == set(), "every B_i is non-empty; their intersection is not"

# Generalised De Morgan over an indexed family.
U = set(range(10))
fam = [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}]
assert U - set().union(*fam) == set(U).intersection(*[U - s for s in fam])
assert U - set(fam[0]).intersection(*fam) == set().union(*[U - s for s in fam])

# Grouped data: union = seen anywhere, intersection = seen everywhere.
groups = {"jan": {"a", "b"}, "feb": {"b", "c"}, "mar": {"b", "d"}}
assert set().union(*groups.values()) == {"a", "b", "c", "d"}
assert set(groups["jan"]).intersection(*groups.values()) == {"b"}
```

## 4. The mistake people actually make

**Assuming an infinite intersection of non-empty sets is non-empty.**

Each `B_i = (0, 1/i)` contains infinitely many points, and their intersection is
empty. "All of these are non-empty, so something must be in all of them" is a
step that simply does not follow, and it fails for exactly the reason above: any
candidate `x > 0` is excluded by a large enough i.

Where this appears in practice: a filter chain that tightens a threshold at each
stage. Each stage keeps a healthy number of rows, and the composition keeps
none. Engineers look for a bug in the last stage; there is none, the pipeline is
simply asking for something no row satisfies.

The diagnostic is to log the surviving count at *every* stage rather than only
at the end. A count that goes 10,000 → 4,000 → 900 → 0 tells you immediately
that the emptiness is cumulative, not a fault in one filter.

---

## Check yourself

1. `A_i = {i, i+1}` for `i ∈ {1,2,3}`. Give the union and the intersection.
2. Why is `⋂_{i≥1} (0, 1/i) = ∅` even though every set in the family is non-empty?
3. In grouped data, what do the union and intersection of the per-group id sets represent?

<details>
<summary>Answers</summary>

1. Union `{1,2,3,4}`; intersection `∅`, since no single number is in all three (1,2 ∩ 2,3 ∩ 3,4 is empty).
2. For any candidate `x > 0` there is an i with `1/i < x`, so x is excluded at that index. No positive real survives every set, and 0 is excluded from all of them because the intervals are open.
3. The union is every id seen in at least one group; the intersection is the ids present in every group - the ones you can compare like-for-like across all of them.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](14_Images_and_Preimages.md) · [Module README](../README.md) · [Next →](16_Countable_versus_Uncountable_Sets.md)
