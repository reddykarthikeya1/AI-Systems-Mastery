# Lesson 01.24 — Set Operations in NumPy and Pandas

> **Module 01:** Set Language for Machine Learning · Lesson 24 of 25

---

## What you will be able to do after this lesson

- [ ] Use NumPy's set routines and state the precondition `np.isin` and friends rely on.
- [ ] Choose between a Python set and a NumPy set operation based on the cost of each.

## Prerequisites

- [Lesson 01.04](04_Union_Intersection_and_Difference.md) - the four operations.

---

## 1. The idea

NumPy provides the same operations on arrays, with different performance and one
important precondition.

| Set idea | NumPy |
| :--- | :--- |
| `A ∪ B` | `np.union1d(a, b)` |
| `A ∩ B` | `np.intersect1d(a, b)` |
| `A \ B` | `np.setdiff1d(a, b)` |
| `A △ B` | `np.setxor1d(a, b)` |
| `x ∈ A` elementwise | `np.isin(x, a)` |
| distinct members | `np.unique(a)` |

**All of these return sorted, deduplicated arrays.** That is convenient and it
is also a trap: the result is not in the input's order, so using it to index
back into the original data silently reorders rows.

On cost. Python's `set` is a hash table: membership is `O(1)`, and building one
from n items is `O(n)`. NumPy's routines sort: `O(n log n)` to build, `O(log n)`
per lookup. For one membership test against a large array, a Python set is
faster. For elementwise testing of a whole array against another,
`np.isin` wins because the loop runs in C rather than in Python.

Pandas offers the same operations - `Series.isin`, `Index.union`,
`Index.difference` - on top of an index, and the same precondition applies:
results come back in index order, not original order.

## 2. Worked example

`a = [3, 1, 2, 3]`, `b = [2, 4]`.

    np.unique(a)        -> [1, 2, 3]       sorted, deduplicated
    np.union1d(a, b)    -> [1, 2, 3, 4]
    np.intersect1d(a,b) -> [2]
    np.setdiff1d(a, b)  -> [1, 3]          in a, not in b
    np.setxor1d(a, b)   -> [1, 3, 4]

Note `np.unique(a)` has length 3 while `a` has length 4 - the duplicate 3 is
collapsed, exactly as a set would.

**The ordering trap.** Suppose rows carry ids `[30, 10, 20]` with values
`[c, a, b]`, and you want the rows whose id is in `{10, 30}`.

    np.intersect1d([30,10,20], [10,30])  ->  [10, 30]

Use that result to look up values and you get `[a, c]` - sorted by id, not in
the original row order. The correct approach keeps the original order by masking:

    mask = np.isin(ids, [10, 30])   ->  [True, True, False]
    ids[mask]                       ->  [30, 10]    original order preserved

## 3. Verify it in code

```python
import numpy as np

a = np.array([3, 1, 2, 3])
b = np.array([2, 4])

assert list(np.unique(a)) == [1, 2, 3]
assert list(np.union1d(a, b)) == [1, 2, 3, 4]
assert list(np.intersect1d(a, b)) == [2]
assert list(np.setdiff1d(a, b)) == [1, 3]
assert list(np.setxor1d(a, b)) == [1, 3, 4]

# Results are sorted and deduplicated, NOT in input order.
ids = np.array([30, 10, 20])
picked = np.intersect1d(ids, np.array([10, 30]))
assert list(picked) == [10, 30], "sorted, not the original order"

# Masking preserves the original order - use this to select rows.
mask = np.isin(ids, [10, 30])
assert list(mask) == [True, True, False]
assert list(ids[mask]) == [30, 10]

values = np.array(["c", "a", "b"])
assert list(values[mask]) == ["c", "a"], "rows stay aligned with their ids"

# They agree with Python sets on membership, which is the point.
assert set(np.union1d(a, b).tolist()) == set(a.tolist()) | set(b.tolist())
assert set(np.setdiff1d(a, b).tolist()) == set(a.tolist()) - set(b.tolist())

# np.unique collapses duplicates exactly as a set does.
assert len(np.unique(a)) == len(set(a.tolist())) == 3

# Elementwise membership against a large array is where np.isin earns its place.
big = np.arange(100_000)
probe = np.array([5, 99_999, 100_000])
assert list(np.isin(probe, big)) == [True, True, False]
```

## 4. The mistake people actually make

**Using `np.intersect1d` to select rows and losing the row alignment.**

The returned array is sorted, so using it to rebuild a dataset reorders the rows
relative to every parallel array - labels, weights, timestamps - that was not
reordered with it. Features and labels silently stop corresponding.

There is no error. The model trains on mismatched pairs and the accuracy is
poor, which gets blamed on the features.

Use a boolean mask instead. `np.isin(ids, wanted)` returns an array the same
length and order as `ids`, and applying the same mask to every parallel array
keeps them aligned. The rule: **select with masks, not with set results**, when
order carries meaning.

A second trap in the same family: `np.unique` has a `return_index` argument that
gives the position of the first occurrence, and people reach for it to "undo"
the sorting. It works, and it is easier to read - and harder to get wrong - to
never leave the original order in the first place.

---

## Check yourself

1. What two things does `np.unique` do to its input?
2. Why can `np.intersect1d` break the correspondence between a feature array and a label array?
3. You need to keep rows whose id is in a set of 5,000 wanted ids, preserving order. What do you use?

<details>
<summary>Answers</summary>

1. Sorts it and removes duplicates. The result is a sorted array of the distinct values.
2. It returns a sorted array of the common values, not a selection in the original order. Using it to index one array but not the others leaves them misaligned, with no error.
3. `mask = np.isin(ids, wanted)` and then apply that same mask to every parallel array. The mask has the same length and order as the input, so alignment is preserved.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](23_Train_Validation_and_Test_as_a_Partition.md) · [Module README](../README.md) · [Next →](25_Module_Project_A_Dataset_Splitter_That_Cannot_Leak.md)
