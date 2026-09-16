# Lesson 01.03 — Subsets, Supersets and the Empty Set

> **Module 01:** Set Language for Machine Learning · Lesson 3 of 25

---

## What you will be able to do after this lesson

- [ ] Decide whether `A ⊆ B` holds, and distinguish `⊆` from `⊂` and from `∈`.
- [ ] Explain why the empty set is a subset of every set, using the definition rather than an appeal to convention.

## Prerequisites

- [Lesson 01.02](02_Set_Notation_Membership_and_Equality.md) - membership and equality.

---

## 1. The idea

`A ⊆ B` - *A is a subset of B* - means every member of A is also a member of B.

Two distinctions that cause real confusion:

**Subset versus proper subset.** `A ⊂ B` (proper) means `A ⊆ B` *and* `A ≠ B`.
Every set is a subset of itself; no set is a proper subset of itself. Some
authors use `⊂` to mean plain subset, so when it matters, write `⊆` and `⊊`.

**Subset versus membership.** `∈` relates an *element* to a set; `⊆` relates a
*set* to a set. `1 ∈ {1, 2}` is true. `1 ⊆ {1, 2}` is not even well formed -
1 is not a set. `{1} ⊆ {1, 2}` is true, and `{1} ∈ {1, 2}` is false, because
the members of `{1, 2}` are the numbers 1 and 2, not the set `{1}`.

**The empty set is a subset of everything.** `∅ ⊆ A` for every A. This follows
from the definition rather than from convention: the claim "every member of ∅
is a member of A" has no counterexample, because ∅ has no members to serve as
one. A statement with no possible counterexample is true - *vacuously* true.

## 2. Worked example

Let `A = {1, 2}`, `B = {1, 2, 3}`, `C = {1, 2}`.

- `A ⊆ B`? Check each member of A: 1 ∈ B ✓, 2 ∈ B ✓. So yes.
- `A ⊂ B`? Yes, since `A ⊆ B` and `A ≠ B` (3 is in B and not A).
- `A ⊆ C`? Every member of A is in C ✓. So yes.
- `A ⊂ C`? No - `A = C`, so it is not a *proper* subset.
- `B ⊆ A`? 3 ∈ B but 3 ∉ A, so no. One counterexample settles it.

And the two directions together give a useful fact:
`A ⊆ B and B ⊆ A` exactly when `A = B`. That is how you *prove* two sets equal
when you cannot simply list them.

## 3. Verify it in code

```python
A, B, C = {1, 2}, {1, 2, 3}, {1, 2}

assert A <= B          # subset
assert A < B           # proper subset
assert A <= C
assert not (A < C)     # equal, so not proper
assert not (B <= A)    # 3 is the counterexample

# Two-directional containment IS equality.
assert (A <= C and C <= A) == (A == C)

# Membership and subset are different relations.
assert 1 in B
assert {1} <= B
assert {1} not in B    # the members of B are numbers, not sets

# The empty set is a subset of every set, vacuously.
for some_set in (set(), {0}, {1, 2, 3}):
    assert set() <= some_set
assert all(x in {1, 2} for x in set())   # no members, so nothing can fail
```

## 4. The mistake people actually make

**Reading vacuous truth as a bug.**

`all(x in B for x in set())` returns `True`, and so does `all([])`. The first
time you see it, it looks like the code silently skipped the check.

It did not. "Every element of the empty collection has property P" is true
because falsifying it requires producing an element that fails, and there are
none. The same convention makes `∅ ⊆ A` true, makes the base case of induction
work, and makes `all()` associative.

Where it actually bites: a validation loop over an empty list reports success.
If "the data satisfied every rule" and "there was no data" should be treated
differently, you have to test for emptiness separately - the quantifier will
not do it for you, and it is not wrong to refuse.

---

## Check yourself

1. Is `{1, 2} ⊆ {1, 2}` true? Is `{1, 2} ⊂ {1, 2}` true?
2. Explain the difference between `{1} ∈ {{1}, 2}` and `{1} ⊆ {1, 2}`.
3. Prove `∅ ⊆ {7}` from the definition.

<details>
<summary>Answers</summary>

1. The first is true - every set is a subset of itself. The second is false, because a proper subset must also be unequal.
2. `{1} ∈ {{1}, 2}` is true: the set `{1}` is literally one of the two members. `{1} ⊆ {1, 2}` is also true, but for a different reason: every member of `{1}` (namely 1) is a member of `{1, 2}`. The first is about being an element, the second about containment.
3. The definition requires every member of ∅ to be a member of `{7}`. ∅ has no members, so there is no member that could fail the requirement, and the statement holds vacuously.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](02_Set_Notation_Membership_and_Equality.md) · [Module README](../README.md) · [Next →](04_Union_Intersection_and_Difference.md)
