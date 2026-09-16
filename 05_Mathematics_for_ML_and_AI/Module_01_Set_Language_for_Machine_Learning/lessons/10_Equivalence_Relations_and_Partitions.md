# Lesson 01.10 — Equivalence Relations and Partitions

> **Module 01:** Set Language for Machine Learning · Lesson 10 of 25

---

## What you will be able to do after this lesson

- [ ] Recognise an equivalence relation and construct the partition it induces.
- [ ] Explain the correspondence between equivalence relations and partitions, and use it to reason about grouped data.

## Prerequisites

- [Lesson 01.09](09_Relations_as_Subsets_of_a_Product.md) - relations and their properties.

---

## 1. The idea

A relation that is reflexive, symmetric **and** transitive is an **equivalence
relation**. It is the formal version of "is the same as, for our purposes".

Its importance comes from a theorem that is easy to state and constantly used:

> **An equivalence relation on A partitions A, and every partition of A comes
> from exactly one equivalence relation.**

A **partition** of A is a collection of non-empty subsets - the *blocks* - that
are pairwise disjoint and whose union is A. Every element is in exactly one
block.

The blocks are the **equivalence classes**: `[a] = { x ∈ A : x R a }`, the set
of everything equivalent to a.

This is why `GROUP BY` works. Grouping rows by a key is choosing the equivalence
relation "has the same key", and the groups it produces are guaranteed to cover
every row exactly once. That guarantee is the theorem, and it is what lets you
sum within groups and know the totals add back to the whole.

## 2. Worked example

`A = {0,1,2,3,4,5}` and `a R b` when `a` and `b` have the same remainder mod 3.

**Reflexive:** a has the same remainder as itself ✓.
**Symmetric:** if a and b share a remainder then so do b and a ✓.
**Transitive:** if a ≡ b and b ≡ c then a ≡ c ✓.

So it is an equivalence relation. The classes:

    [0] = {0, 3}     remainder 0
    [1] = {1, 4}     remainder 1
    [2] = {2, 5}     remainder 2

Check the partition properties:

- non-empty: all three have 2 elements ✓
- pairwise disjoint: `{0,3} ∩ {1,4} = ∅`, and so on ✓
- union is A: `{0,3} ∪ {1,4} ∪ {2,5} = {0,1,2,3,4,5}` ✓

Note `[0] = [3]` - the class is the same set whichever member you name it by.
That is a consequence of symmetry and transitivity, and it is why a group has
no privileged representative.

## 3. Verify it in code

```python
A = set(range(6))

def classes(domain, key):
    blocks = {}
    for x in sorted(domain):
        blocks.setdefault(key(x), set()).add(x)
    return list(blocks.values())

blocks = classes(A, lambda x: x % 3)
assert sorted(map(sorted, blocks)) == [[0, 3], [1, 4], [2, 5]]

# The three partition properties.
assert all(b for b in blocks), "no block is empty"
for i, b1 in enumerate(blocks):
    for b2 in blocks[i + 1:]:
        assert b1 & b2 == set(), "blocks are pairwise disjoint"
assert set().union(*blocks) == A, "the blocks cover A"

# Every element is in exactly one block.
for x in A:
    assert sum(1 for b in blocks if x in b) == 1

# A class has no privileged representative: [0] == [3].
same_mod_3 = lambda a, b: a % 3 == b % 3
assert {x for x in A if same_mod_3(x, 0)} == {x for x in A if same_mod_3(x, 3)}

# This is exactly what GROUP BY guarantees: the group totals reconstruct the whole.
values = {0: 5, 1: 2, 2: 7, 3: 1, 4: 4, 5: 3}
assert sum(sum(values[x] for x in b) for b in blocks) == sum(values.values())
```

## 4. The mistake people actually make

**Grouping by a key that is not well defined, and expecting a partition.**

`GROUP BY email` looks like an equivalence relation, and it is - as long as
every row has exactly one email. The moment emails are missing, or a row has
several, the relation stops partitioning: a `NULL` key may form its own group,
be dropped, or be treated as equal to other `NULL`s depending on the engine.

The result is that the groups no longer cover the data exactly once, and the
guarantee you were relying on - that per-group sums reconstruct the total -
quietly fails. The totals come out low and nothing reports it.

The check is one line and worth running whenever a grouped aggregate matters:
the sum over groups must equal the sum over all rows. If it does not, the
grouping key is not partitioning your data, and the fix is to decide explicitly
what the missing and multi-valued cases mean before aggregating.

---

## Check yourself

1. Is 'lives in the same city' an equivalence relation? Is 'lives within 10 km of'?
2. How many blocks does 'same remainder mod 5' induce on the integers?
3. Your per-group totals sum to less than the overall total. What does that tell you about the grouping key?

<details>
<summary>Answers</summary>

1. The first is: reflexive, symmetric and transitive. The second is reflexive and symmetric but not transitive - A can be within 10 km of B and B of C while A and C are 19 km apart.
2. Five - one for each possible remainder 0, 1, 2, 3, 4.
3. That it is not partitioning the data: some rows fall into no group, most commonly because the key is missing or null. A partition must cover every element exactly once.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](09_Relations_as_Subsets_of_a_Product.md) · [Module README](../README.md) · [Next →](11_Functions_as_Special_Relations.md)
