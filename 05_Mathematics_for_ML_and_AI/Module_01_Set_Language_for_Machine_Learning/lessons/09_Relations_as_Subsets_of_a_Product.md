# Lesson 01.09 — Relations as Subsets of a Product

> **Module 01:** Set Language for Machine Learning · Lesson 9 of 25

---

## What you will be able to do after this lesson

- [ ] Define a relation as a subset of a Cartesian product and give an example from data.
- [ ] Test a relation for reflexivity, symmetry and transitivity.

## Prerequisites

- [Lesson 01.08](08_Cartesian_Products_and_Tuples.md) - Cartesian products.

---

## 1. The idea

A **relation** from A to B is any subset of `A × B`. That is the whole
definition: a relation is a set of pairs, and a pair is in it exactly when the
relation holds.

Write `a R b` for `(a, b) ∈ R`.

This is more general than it first looks. A join key, a "follows" edge in a
social graph, a "is a prerequisite for" link between lessons, and the ordering
`≤` are all relations - all just sets of pairs.

When `A = B` we call R a relation *on* A, and three properties become askable:

| Property | Means | In symbols |
| :--- | :--- | :--- |
| Reflexive | everything relates to itself | `a R a` for all a |
| Symmetric | direction does not matter | `a R b ⟹ b R a` |
| Transitive | it chains | `a R b and b R c ⟹ a R c` |

These are not decorations. "Is the same user as" should be all three, and if
your identity-resolution code produces a relation that is not transitive - A
matches B, B matches C, A does not match C - then "the set of records for one
user" is not well defined, and different code paths will disagree about it.

## 2. Worked example

`A = {1, 2, 3}` and `R = {(1,1), (2,2), (3,3), (1,2), (2,1)}`.

**Reflexive?** Need `(a,a)` for every a: `(1,1)` ✓, `(2,2)` ✓, `(3,3)` ✓. Yes.

**Symmetric?** Check each pair with distinct components: `(1,2)` is present and
so is `(2,1)` ✓. Yes.

**Transitive?** Check every chain. `(1,2)` and `(2,1)` give a chain 1→2→1, so we
need `(1,1)` - present ✓. `(2,1)` and `(1,2)` need `(2,2)` - present ✓. The
reflexive pairs chain trivially. Yes.

Now break it: `S = {(1,2), (2,3)}`. There is a chain 1→2→3, so transitivity
demands `(1,3)`, which is absent. S is not transitive. It is also not reflexive
(no `(1,1)`) and not symmetric (no `(2,1)`).

## 3. Verify it in code

```python
A = {1, 2, 3}
R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}

def reflexive(rel, domain):
    return all((a, a) in rel for a in domain)

def symmetric(rel):
    return all((b, a) in rel for (a, b) in rel)

def transitive(rel):
    return all((a, d) in rel
               for (a, b) in rel for (c, d) in rel if b == c)

assert reflexive(R, A)
assert symmetric(R)
assert transitive(R)

S = {(1, 2), (2, 3)}
assert not reflexive(S, A)
assert not symmetric(S)
assert not transitive(S), "1->2 and 2->3 chain, but (1,3) is absent"

# A relation really is just a subset of the product.
from itertools import product
assert R <= set(product(A, A))

# "Strictly less than" on a small set: transitive, not reflexive, not symmetric.
less = {(a, b) for a in A for b in A if a < b}
assert transitive(less)
assert not reflexive(less, A)
assert not symmetric(less)
```

## 4. The mistake people actually make

**Assuming a similarity rule is transitive when it is a threshold.**

Identity resolution often uses "these two records match if their similarity
exceeds 0.9". That relation is reflexive and symmetric, and it is almost never
transitive: A can be 0.91 similar to B, B 0.91 similar to C, and A only 0.85
similar to C.

The consequence is that "the group of records belonging to one person" is not
well defined. Depending on the order you merge in, you get different clusters -
and two runs of the same pipeline on the same data can disagree.

Nothing errors. You get plausible clusters that are unstable, and the
instability is blamed on the data rather than on the relation.

The fix is to decide what you want explicitly: either take the **transitive
closure** (merge anything connected by a chain, which can over-merge into one
giant cluster) or use a clustering algorithm that optimises a global objective
rather than chaining pairwise decisions. Both are defensible. Chaining a
non-transitive relation and hoping is not.

---

## Check yourself

1. Is `≤` on the integers reflexive, symmetric, transitive?
2. `R = {(1,2), (2,1)}` on `{1,2}`. Which of the three properties hold?
3. Why does a non-transitive 'same entity' relation make cluster membership ambiguous?

<details>
<summary>Answers</summary>

1. Reflexive (a ≤ a) and transitive (a ≤ b ≤ c implies a ≤ c), but not symmetric (1 ≤ 2 does not give 2 ≤ 1).
2. Symmetric only. It is not reflexive - `(1,1)` and `(2,2)` are absent - and not transitive, since 1→2→1 requires `(1,1)`.
3. Because membership then depends on the order in which pairs are merged: A-B and B-C merging into one group implies A and C are together, which the relation itself never asserted. Different orders give different groups.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](08_Cartesian_Products_and_Tuples.md) · [Module README](../README.md) · [Next →](10_Equivalence_Relations_and_Partitions.md)
