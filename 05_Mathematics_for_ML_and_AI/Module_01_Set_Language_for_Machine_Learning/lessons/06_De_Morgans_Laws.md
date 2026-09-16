# Lesson 01.06 — De Morgan's Laws

> **Module 01:** Set Language for Machine Learning · Lesson 6 of 25

---

## What you will be able to do after this lesson

- [ ] Apply De Morgan's laws to rewrite a negated union or intersection.
- [ ] State what happens to the connective when a negation is distributed, and use it to simplify a filter condition.

## Prerequisites

- [Lesson 01.05](05_Complements_and_the_Universal_Set.md) - complements.

---

## 1. The idea

De Morgan's laws say how a complement distributes over union and intersection:

    (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ
    (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ

**The negation distributes, and the connective flips.** That second half is the
part people drop, and it is the whole content of the law.

Read the first in words: *not (in A or in B)* means *not in A, and not in B*.
That is obviously right once said aloud - to be outside both, you must be
outside each. And the second: *not (in A and in B)* means *outside at least one
of them*, which is a far weaker condition than being outside both.

Why it matters in practice: filters. "Rows that are not (fraudulent or
refunded)" is the same as "not fraudulent and not refunded". Getting this wrong
turns an `and` into an `or` and changes which rows you keep, without changing
anything that looks like a bug.

## 2. Worked example

`U = {1,...,8}`, `A = {1,2,3,4}`, `B = {3,4,5,6}`.

First law, left side:

    A ∪ B = {1,2,3,4,5,6}
    (A ∪ B)ᶜ = U \ {1,2,3,4,5,6} = {7, 8}

First law, right side:

    Aᶜ = {5,6,7,8},  Bᶜ = {1,2,7,8}
    Aᶜ ∩ Bᶜ = {7, 8}  ✓

Second law, left side:

    A ∩ B = {3,4}
    (A ∩ B)ᶜ = {1,2,5,6,7,8}

Second law, right side:

    Aᶜ ∪ Bᶜ = {5,6,7,8} ∪ {1,2,7,8} = {1,2,5,6,7,8}  ✓

Now the wrong version, to see how close it looks. Computing
`Aᶜ ∩ Bᶜ` for the *second* law gives `{7, 8}` - which agrees with the correct
answer on 7 and 8, and is missing four elements. It is a subset of the right
answer, never a superset, so a spot check on one element will often pass.

## 3. Verify it in code

```python
U = set(range(1, 9))
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

def complement(s):
    return U - s

# The two laws.
assert complement(A | B) == complement(A) & complement(B)
assert complement(A & B) == complement(A) | complement(B)

assert complement(A | B) == {7, 8}
assert complement(A & B) == {1, 2, 5, 6, 7, 8}

# The wrong version - distributing without flipping the connective.
wrong = complement(A) & complement(B)
assert wrong != complement(A & B)
assert wrong < complement(A & B), "the error under-selects; it is a strict subset"

# They hold for every pair of subsets, not just this one.
from itertools import combinations
universe = set(range(5))
for size_a in range(len(universe) + 1):
    for X in combinations(universe, size_a):
        for Y in combinations(universe, 2):
            X, Y = set(X), set(Y)
            assert universe - (X | Y) == (universe - X) & (universe - Y)
            assert universe - (X & Y) == (universe - X) | (universe - Y)
```

## 4. The mistake people actually make

**Distributing the negation and leaving the connective alone.**

Writing `not (a and b)` as `(not a) and (not b)` is the single most common
logic error in data filtering. It computes `not (a or b)` instead.

What makes it survive: the two agree whenever `a` and `b` have the same truth
value. They differ only in the mixed cases - one true, one false. So a filter
tested on rows that are either clearly good or clearly bad passes, and the rows
that are one-of-each are silently dropped.

In set terms the wrong answer is always a *subset* of the right one, so the
symptom is "we seem to be filtering out more than expected" - a quiet loss of
rows with no error, which usually gets blamed on the data.

If you are unsure, write the four-row truth table. It takes thirty seconds and
is not a matter of memory.

---

## Check yourself

1. Rewrite `not (x > 5 or x < 0)` without the outer negation.
2. `(A ∩ B)ᶜ` was computed as `Aᶜ ∩ Bᶜ`. Is the answer too large or too small, and why?
3. Why do the correct and incorrect forms agree on many test cases?

<details>
<summary>Answers</summary>

1. `x <= 5 and x >= 0`, i.e. `0 <= x <= 5`. The `or` becomes `and` and each comparison is negated.
2. Too small - it is a subset of the correct answer. Requiring an element to be outside *both* sets is stricter than requiring it to be outside *at least one*.
3. They differ only when the two conditions disagree with each other. Any test where both conditions are true, or both false, gives the same result under either form.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](05_Complements_and_the_Universal_Set.md) · [Module README](../README.md) · [Next →](07_Power_Sets_and_Counting_Subsets.md)
