# Lesson 01.05 — Complements and the Universal Set

> **Module 01:** Set Language for Machine Learning · Lesson 5 of 25

---

## What you will be able to do after this lesson

- [ ] Compute a complement relative to a stated universal set, and explain why the universe must be stated.
- [ ] Recognise that a complement is meaningless without a universe, and name a bug caused by assuming one.

## Prerequisites

- [Lesson 01.04](04_Union_Intersection_and_Difference.md) - the four operations.

---

## 1. The idea

The **complement** of A, written `Aᶜ` or `A'`, is everything not in A. The
obvious question is *everything in what*, and it has no default answer.

The **universal set** `U` is the collection everything is drawn from, and it
must be stated. Then:

    Aᶜ = U \ A

Change `U` and the complement changes completely. If `A = {1, 2}`:

- with `U = {1, 2, 3}`, `Aᶜ = {3}`
- with `U = {1, ..., 10}`, `Aᶜ = {3, 4, 5, 6, 7, 8, 9, 10}`
- with `U = ℤ`, `Aᶜ` is infinite

This is not pedantry. In machine learning the universe is usually "the classes
the model knows about" or "the ids in the catalogue", and it is exactly the
thing that changes between training and production.

Three facts that follow immediately:

    (Aᶜ)ᶜ = A          complementing twice returns you to A
    A ∪ Aᶜ = U         every element is in one or the other
    A ∩ Aᶜ = ∅         and never both

## 2. Worked example

A recommender knows the catalogue `U = {a, b, c, d, e}`. A user has watched
`W = {b, d}`.

The candidates to recommend are the ones they have not watched:

    Wᶜ = U \ W = {a, c, e}

Now the catalogue grows: `U' = {a, b, c, d, e, f}`. The user's watched set is
unchanged, but the complement is not:

    Wᶜ = {a, c, e, f}

Nothing about the user changed. The recommendable set changed because the
universe did - which is the correct behaviour, and it is only correct because
the universe was stated explicitly rather than inferred from the data on hand.

Check the two laws: `W ∪ Wᶜ = {a, b, c, d, e} = U` ✓, and
`W ∩ Wᶜ = ∅` ✓.

## 3. Verify it in code

```python
U = {"a", "b", "c", "d", "e"}
W = {"b", "d"}

complement = U - W
assert complement == {"a", "c", "e"}

# The two defining laws.
assert W | complement == U
assert W & complement == set()

# Complementing twice is the identity.
assert U - (U - W) == W

# Change the universe and the complement changes with it.
U2 = U | {"f"}
assert U2 - W == {"a", "c", "e", "f"}
assert U - W != U2 - W, "a complement is meaningless without its universe"

# A set must be inside the universe for any of this to behave.
assert W <= U
```

## 4. The mistake people actually make

**Inferring the universe from whatever data happens to be loaded.**

A model is trained on the classes present in the training file and, at
inference, is asked about a class that file did not contain. Code that computes
"the classes we do not predict" as `set(all_seen) - set(predicted)` silently
uses a universe that is *the union of what turned up*, not the real label set.

The symptom is a complement that shrinks or grows between runs for no reason
anybody can trace, because it depends on which shard was loaded.

The fix is to make the universe an explicit input - a declared label list, a
catalogue table - rather than something derived. When someone says "the
complement of A", the first question is always "inside which universe", and if
the code cannot answer it, that is the bug.

---

## Check yourself

1. `A = {2, 4}`. Give `Aᶜ` for `U = {1,2,3,4}` and for `U = {2,4}`.
2. Why is `A ∩ Aᶜ = ∅` true for every A and every universe?
3. A pipeline computes 'unseen categories' as `set(batch_categories) - set(seen)`. What silently changes this answer between runs?

<details>
<summary>Answers</summary>

1. `{1, 3}` and `∅` respectively. In the second case A is the whole universe, so its complement is empty.
2. An element of the intersection would have to be in A and also not in A, which is impossible. So the intersection has no members.
3. The universe is taken from `batch_categories`, which depends on which rows are in the current batch. A category absent from this batch is treated as if it does not exist. The universe should be the declared catalogue, not the batch.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](04_Union_Intersection_and_Difference.md) · [Module README](../README.md) · [Next →](06_De_Morgans_Laws.md)
