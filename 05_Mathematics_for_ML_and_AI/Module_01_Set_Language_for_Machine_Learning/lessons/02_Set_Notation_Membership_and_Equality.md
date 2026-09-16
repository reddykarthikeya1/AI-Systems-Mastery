# Lesson 01.02 — Set Notation, Membership and Equality

> **Module 01:** Set Language for Machine Learning · Lesson 2 of 25

---

## What you will be able to do after this lesson

- [ ] Read and write the notation `x ∈ A`, `A = B`, and `|A|`, and translate each into a line of Python.
- [ ] Explain why set equality is decided by membership rather than by construction or order.

## Prerequisites

- [Lesson 01.01](01_Why_Sets_Are_the_Vocabulary_of_ML.md) - what a set is.

---

## 1. The idea

Four pieces of notation carry most of the weight.

| Notation | Read as | Python |
| :--- | :--- | :--- |
| `x ∈ A` | x is a member of A | `x in A` |
| `x ∉ A` | x is not a member of A | `x not in A` |
| `A = B` | A and B have exactly the same members | `A == B` |
| `\|A\|` | the size, or *cardinality*, of A | `len(A)` |

Sets are written in two ways, and you will meet both constantly:

- **Roster form** lists the members: `A = {2, 4, 6}`.
- **Set-builder form** states the rule: `A = {x ∈ ℕ : x is even and x < 7}`.

The colon is read "such that". Set-builder form is what a list comprehension
is: `{x for x in range(7) if x % 2 == 0}` is the same statement in Python.

The definition of equality is worth stating precisely, because it is the thing
people get wrong: `A = B` exactly when every member of A is a member of B and
every member of B is a member of A. Nothing about how the sets were built
matters.

## 2. Worked example

Let `A = {x ∈ ℤ : 0 ≤ x < 6 and x is even}` and `B = {4, 0, 2}`.

Expand A by the rule. The integers from 0 to 5 are 0, 1, 2, 3, 4, 5; the even
ones are 0, 2, 4. So `A = {0, 2, 4}`.

Is `A = B`? Check both directions:

- every member of A is in B: 0 ∈ B ✓, 2 ∈ B ✓, 4 ∈ B ✓
- every member of B is in A: 4 ∈ A ✓, 0 ∈ A ✓, 2 ∈ A ✓

Both hold, so `A = B`, even though one was written by a rule and the other by
listing, and the listing was out of order.

`|A| = 3`, and `3 ∉ A` because 3 is not even.

## 3. Verify it in code

```python
A = {x for x in range(6) if x % 2 == 0}   # set-builder form
B = {4, 0, 2}                             # roster form, different order

assert A == {0, 2, 4}
assert A == B, "how a set was built has no bearing on what it is"

# membership
assert 2 in A
assert 3 not in A

# cardinality
assert len(A) == 3

# Equality is two-directional containment, which is what `==` checks.
assert all(x in B for x in A) and all(x in A for x in B)

# The empty set has no members and size zero.
empty = set()
assert len(empty) == 0
assert 0 not in empty          # careful: 0 is a value, not "nothing"
```

## 4. The mistake people actually make

**Writing `{}` for the empty set in Python.**

In mathematics `{}` and `∅` both mean the empty set. In Python `{}` is an empty
**dictionary**, not an empty set. The empty set is `set()`.

This is not a style point. `{}` is falsy and has `len() == 0`, so a check like
`if not candidates:` behaves identically and the mistake hides. It surfaces
later, when something calls `.add()` and gets `AttributeError`, or when a
`|` union silently does something else entirely.

A related slip: `{0}` is a set containing the number zero, and it is *not*
empty. `|{0}| = 1`. Confusing "contains nothing" with "contains zero" is the
same error that makes `if x:` the wrong test for `x = 0`.

---

## Check yourself

1. Write `{x ∈ ℤ : 1 ≤ x ≤ 10 and x divisible by 3}` in roster form.
2. Is `{1, 2, 3} = {3, 2, 1, 1}`? Justify from the definition.
3. What is `len({})` in Python, and why is that answer misleading?

<details>
<summary>Answers</summary>

1. `{3, 6, 9}`.
2. Yes. Every member of the left is a member of the right and vice versa. The repeated 1 and the different order are both irrelevant to membership.
3. It is 0 - but `{}` is an empty dict, not an empty set. The length agrees with the empty set by coincidence, which is exactly what makes the bug hard to spot. Use `set()`.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](01_Why_Sets_Are_the_Vocabulary_of_ML.md) · [Module README](../README.md) · [Next →](03_Subsets_Supersets_and_the_Empty_Set.md)
