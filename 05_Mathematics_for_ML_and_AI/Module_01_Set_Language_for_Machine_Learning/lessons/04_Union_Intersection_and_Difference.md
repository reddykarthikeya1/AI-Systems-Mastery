# Lesson 01.04 — Union, Intersection and Difference

> **Module 01:** Set Language for Machine Learning · Lesson 4 of 25

---

## What you will be able to do after this lesson

- [ ] Compute union, intersection, difference and symmetric difference by hand and in Python.
- [ ] Choose the right operation for a stated data question, such as 'which ids are in the new export but not the old'.

## Prerequisites

- [Lesson 01.03](03_Subsets_Supersets_and_the_Empty_Set.md) - subsets.

---

## 1. The idea

Four operations, each answering a different everyday question.

| Operation | Notation | Means | Python |
| :--- | :--- | :--- | :--- |
| Union | `A ∪ B` | in A, or B, or both | `A \| B` |
| Intersection | `A ∩ B` | in both | `A & B` |
| Difference | `A \ B` | in A but not B | `A - B` |
| Symmetric difference | `A △ B` | in exactly one | `A ^ B` |

The data questions they answer:

- *Every user we have seen, across both exports* - union.
- *Users present in both, so we can compare* - intersection.
- *Users the new export dropped* - `old \ new`.
- *Everything that changed in either direction* - symmetric difference.

Difference is the only one that is **not** symmetric: `A \ B` and `B \ A`
answer different questions, and confusing them is the most common error here.

Two identities worth knowing because they turn one operation into another:

    A △ B = (A \ B) ∪ (B \ A)
    A △ B = (A ∪ B) \ (A ∩ B)

## 2. Worked example

Yesterday's export `A = {1, 2, 3, 4}`; today's export `B = {3, 4, 5}`.

- `A ∪ B = {1, 2, 3, 4, 5}` - every id seen on either day. Size 5.
- `A ∩ B = {3, 4}` - present both days, so comparable. Size 2.
- `A \ B = {1, 2}` - disappeared from today's export.
- `B \ A = {5}` - new today.
- `A △ B = {1, 2, 5}` - everything that changed, in either direction.

Check the sizes against the inclusion-exclusion identity:

    |A ∪ B| = |A| + |B| - |A ∩ B| = 4 + 3 - 2 = 5 ✓

Subtracting the intersection is necessary because the two counts each include
3 and 4, so adding them counts those elements twice.

## 3. Verify it in code

```python
A = {1, 2, 3, 4}
B = {3, 4, 5}

assert A | B == {1, 2, 3, 4, 5}
assert A & B == {3, 4}
assert A - B == {1, 2}        # dropped
assert B - A == {5}           # added
assert A ^ B == {1, 2, 5}

# Difference is NOT symmetric; the others are.
assert A - B != B - A
assert A | B == B | A
assert A & B == B & A
assert A ^ B == B ^ A

# The two identities for symmetric difference.
assert A ^ B == (A - B) | (B - A)
assert A ^ B == (A | B) - (A & B)

# Inclusion-exclusion.
assert len(A | B) == len(A) + len(B) - len(A & B)
```

## 4. The mistake people actually make

**Adding two counts to get the size of a union.**

"We had 4,000 users in January and 3,000 in February, so 7,000 users." That is
`|A| + |B|`, and it is right only when `A ∩ B = ∅`. Anyone active in both
months is counted twice.

The correct figure is `|A ∪ B| = |A| + |B| - |A ∩ B|`, and the error is always
in the same direction: the naive sum is an **overcount**, never an undercount.
Reported as "monthly active users", it inflates the number quietly and
consistently, which is why it survives for quarters at a time.

The second common slip is reaching for `A - B` when the question was `B - A`.
Say the question out loud - *which ids are in the new file and missing from the
old* - and the order follows: the set you are looking *in* comes first.

---

## Check yourself

1. `A = {1,2,3}`, `B = {3,4}`. Give `A \ B` and `B \ A`.
2. A report says there were 500 users in week 1 and 600 in week 2, for 1,100 distinct users. What must be true for that to be correct, and what is the number otherwise?
3. Express `A ∩ B` using only union and difference.

<details>
<summary>Answers</summary>

1. `A \ B = {1, 2}` and `B \ A = {4}`. They are different sets, because difference is not symmetric.
2. It is correct only if no user appeared in both weeks, i.e. the intersection is empty. Otherwise the true count is 500 + 600 - |overlap|, which is smaller.
3. `A ∩ B = A \ (A \ B)`. Removing from A everything that is not in B leaves exactly the part of A that is in B.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](03_Subsets_Supersets_and_the_Empty_Set.md) · [Module README](../README.md) · [Next →](05_Complements_and_the_Universal_Set.md)
