# Lesson 01.25 — Module Project: A Dataset Splitter That Cannot Leak

> **Module 01:** Set Language for Machine Learning · Lesson 25 of 25

---

## What you will be able to do after this lesson

- [ ] Implement a splitter that partitions by a grouping key and proves the partition properties.
- [ ] Write the assertions that would have caught each of the leakage modes covered in this module.

## Prerequisites

- [Lesson 01.23](23_Train_Validation_and_Test_as_a_Partition.md) - splits as partitions.
- [Lesson 01.10](10_Equivalence_Relations_and_Partitions.md) - partitions.

---

## 1. The idea

The module project: a splitter that **cannot** leak, because it checks the
properties rather than assuming them.

Everything in this module shows up:

| Lesson | Used for |
| :--- | :--- |
| 01, 04 | intersection as the leakage test |
| 10 | the split is a partition induced by a grouping key |
| 11, 12 | the group key is a function; leakage is it failing to be injective on blocks |
| 23 | the unit of independence, and chronological order |

The specification:

1. Group rows by a key, partition the **groups**, then collect their rows.
2. Assert exhaustiveness: every row appears in exactly one split.
3. Assert disjointness at the **group** level, not the row level.
4. Support an optional time column, and when given, assert the split is
   chronological.
5. Fail loudly. A splitter that returns a bad split quietly is worse than one
   that raises.

The full reference implementation lives in
[`project_solution/`](../project_solution); this lesson builds the core and its
proofs.

## 2. Worked example

Nine rows, three users, with timestamps.

    row:  0  1  2  3  4  5  6  7  8
    user: a  a  b  b  b  c  c  c  c
    time: 1  2  3  4  5  6  7  8  9

**Group split, 2 users train / 1 user test.** Partition users first:
`{a, b}` train, `{c}` test. Collect rows: train = 0-4 (5 rows), test = 5-8
(4 rows).

Check the three conditions:

- exhaustive: `{0..4} ∪ {5..8} = {0..8}` ✓
- rows disjoint: `∅` ✓
- **users disjoint**: `{a,b} ∩ {c} = ∅` ✓

Chronological? `max(train times) = 5 < 6 = min(test times)` ✓ - here the users
happen to be ordered in time, so the group split is also chronological.

Now `{a, c}` train and `{b}` test. Groups are still disjoint, rows still
partition - but `max(train time) = 9 > 3 = min(test time)`. Training contains
rows from after the test period. Valid as a group split, invalid as a temporal
one, and only an explicit check distinguishes them.

## 3. Verify it in code

```python
def group_split(rows, key, fractions=(0.7, 0.3), time=None):
    """Partition by GROUP, then collect rows. Raises if any property fails."""
    groups = sorted({key(r) for r in rows})
    cut = round(len(groups) * fractions[0])
    train_groups, test_groups = set(groups[:cut]), set(groups[cut:])

    train = [r for r in rows if key(r) in train_groups]
    test = [r for r in rows if key(r) in test_groups]

    if set(train) | set(test) != set(rows):
        raise ValueError("split is not exhaustive")
    if set(train) & set(test):
        raise ValueError("rows appear in both splits")
    if {key(r) for r in train} & {key(r) for r in test}:
        raise ValueError("a group appears in both splits")
    if time is not None and train and test:
        if max(time(r) for r in train) >= min(time(r) for r in test):
            raise ValueError("split is not chronological")
    return train, test


rows = list(range(9))
user = {0: "a", 1: "a", 2: "b", 3: "b", 4: "b", 5: "c", 6: "c", 7: "c", 8: "c"}
stamp = {r: r + 1 for r in rows}

train, test = group_split(rows, key=user.get, fractions=(0.67, 0.33))
assert train == [0, 1, 2, 3, 4] and test == [5, 6, 7, 8]
assert {user[r] for r in train} & {user[r] for r in test} == set()
assert set(train) | set(test) == set(rows)

# It is also chronological here, so the temporal check passes.
group_split(rows, key=user.get, fractions=(0.67, 0.33), time=stamp.get)

# A row-level split that leaks a group is rejected.
def naive_split(rows, at):
    return rows[:at], rows[at:]

bad_train, bad_test = naive_split(rows, 3)
assert set(bad_train) & set(bad_test) == set(), "rows disjoint..."
assert {user[r] for r in bad_train} & {user[r] for r in bad_test} == {"b"}, "...group leaked"

# And a non-chronological group split is rejected when a time column is given.
reordered = {0: "a", 1: "a", 2: "c", 3: "c", 4: "c", 5: "c", 6: "b", 7: "b", 8: "b"}
try:
    group_split(rows, key=reordered.get, fractions=(0.67, 0.33), time=stamp.get)
    raise AssertionError("should have rejected a non-chronological split")
except ValueError as exc:
    assert "chronological" in str(exc)
```

## 4. The mistake people actually make

**Writing the splitter correctly and never asserting the properties.**

Every leakage bug in this module passed a visual inspection. The row counts were
right, the fractions were right, nothing raised. What was missing was a check
that the intended property actually held.

The three assertions cost almost nothing and each catches a distinct failure:

```python
assert set(train) | set(test) == set(rows)                       # nothing dropped
assert units(train) & units(test) == set()                       # no group leaked
assert max(t(r) for r in train) < min(t(r) for r in test)        # no future leaked
```

The habit worth taking from this module: when code is supposed to establish a
property, assert the property rather than inspecting the code that establishes
it. Set operations make these properties one-liners, which is the practical
reason to have learned the vocabulary at all.

And keep the failure loud. A splitter that logs a warning and returns a leaking
split will have that warning filtered out of the logs within a week.

---

## Check yourself

1. Which single assertion distinguishes a valid group split from a row split that happens to look fine?
2. Why must the split be performed on groups before rows are collected, rather than fixing a row split afterwards?
3. Your group split passes all three checks but the model still scores suspiciously well. Name two leaks that none of these assertions would catch.

<details>
<summary>Answers</summary>

1. `units(train) & units(test) == set()` - the intersection taken over group ids rather than row indices. A row split always passes the row-level version.
2. Because repairing a row split requires moving whole groups anyway, and doing it afterwards changes the split sizes unpredictably. Partitioning the groups first makes the property true by construction; the assertions then confirm it.
3. Fitting a scaler or imputer on the whole dataset before splitting, and selecting features using the full dataset. Both leak information without putting any row or group on both sides.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](24_Set_Operations_in_NumPy_and_Pandas.md) · [Module README](../README.md)
