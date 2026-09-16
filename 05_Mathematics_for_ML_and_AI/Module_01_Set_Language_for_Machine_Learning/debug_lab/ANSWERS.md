# Debug Lab 01 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - there is none here

`split` is correct. 60/20/20 of 100 rows is 60/20/20, the totals add up, and
the partitions are disjoint.

That is deliberate. A debugging exercise where every section is broken teaches
you to find a fault wherever you look, which is the opposite of the skill. Part
of reading output is being able to say "this part is fine".

**The general lesson.** Confirm what works before hunting for what does not.
An investigation that assumes a bug in the first place it looks will find one.

---

## Defect 2 - a linear membership test inside a loop

**Where:** `deduplicate`, the line `if row not in seen`.

`seen` is a **list**, so `in` scans it from the start. With `d` distinct values
already collected, each new row costs up to `d` comparisons, and the whole pass
is `O(n * d)` - quadratic when most rows are distinct.

The answer is right, which is why this survives review. It is a performance
defect with no functional symptom, and it only becomes visible at a scale
nobody tested at.

**The fix.** A set membership test is `O(1)`:

```python
def deduplicate(rows):
    seen = set()
    out = []
    for row in rows:
        if row not in seen:
            seen.add(row)
            out.append(row)
    return out
```

Order is preserved, which `set(rows)` would not do.

**The general lesson.** `in` means two entirely different algorithms depending
on the container. On a list it is a scan; on a set or dict it is a hash lookup.
This is Module 01's material doing real work: a set is not a tidier list, it is
a different data structure with a different cost model.

---

## Defect 3 - splitting rows when the unit of independence is the patient

**Where:** `group_split`, which cuts the row list at `int(len(rows) * 0.7)`
without ever looking at `groups`.

Each patient contributes three records. Cutting at row 21 puts patient `p7`'s
first record in train and the other two in test. The model then sees the same
patient on both sides.

This is **data leakage**, and it is the single most common cause of a model
that scores brilliantly in evaluation and fails in production. Nothing errors.
The metric goes *up*, which is why nobody investigates.

**The fix.** Split the groups, then take whole groups:

```python
def group_split(rows, groups, train_frac=0.7):
    unique = sorted(set(groups))
    cut = int(len(unique) * train_frac)
    train_groups = set(unique[:cut])
    train = [i for i, g in enumerate(groups) if g in train_groups]
    test = [i for i, g in enumerate(groups) if g not in train_groups]
    return train, test
```

**The general lesson.** In set language: a train/test split must be a
**partition of the units that are independent**, not of the rows. Ask what the
independent unit actually is - patient, user, session, document - and partition
that. The rows follow.
