# Lesson 01.23 — Train, Validation and Test as a Partition

> **Module 01:** Set Language for Machine Learning · Lesson 23 of 25

---

## What you will be able to do after this lesson

- [ ] State the three conditions that make a train/validation/test split a partition of the correct units.
- [ ] Detect leakage by computing the pairwise intersections, and explain why grouped and temporal data need different split rules.

## Prerequisites

- [Lesson 01.10](10_Equivalence_Relations_and_Partitions.md) - partitions.
- [Lesson 01.04](04_Union_Intersection_and_Difference.md) - intersection.

---

## 1. The idea

A train/validation/test split should be a **partition** of the *units of
independence*:

1. **Exhaustive** - every unit lands somewhere: `train ∪ val ∪ test = U`
2. **Disjoint** - no unit lands twice: all pairwise intersections empty
3. **Of the right units** - the blocks are units, not rows

Condition 3 is the one that is almost always the problem, and it is not
detectable from the split itself. The unit of independence is whatever, if it
appeared on both sides, would let the model recall rather than generalise:

| Data | Unit |
| :--- | :--- |
| Independent rows | the row |
| Several records per patient | the patient |
| Sentences from documents | the document |
| Repeated purchases per user | the user |
| Time series | the time period |

Time series needs more than disjointness. Training on data *after* the test
period leaks the future, even though the sets are disjoint - the split must be
**chronological**, not random. Disjointness is necessary and not sufficient.

The check costs three lines, and it is the most valuable assertion in a
pipeline: compute the three pairwise intersections and assert they are empty.

## 2. Worked example

30 records from 10 patients, 3 records each. Patient `i` owns records
`3i, 3i+1, 3i+2`.

**Row split, 70/30.** Records 0-20 train, 21-29 test.

    train patients = {0,...,6}      (records 0-20 cover patients 0-6)
    test patients  = {7, 8, 9}

Here the cut at 21 happens to fall on a patient boundary, so it is clean. Now
split at 22 instead:

    train = records 0-21  -> patients {0,...,7}
    test  = records 22-29 -> patients {7, 8, 9}

    train ∩ test = {7}

Patient 7 is in both. The rows are disjoint; the patients are not. The row-level
check passes and the split is invalid.

**Group split.** Partition the *patients* first - `{0,...,6}` train,
`{7,8,9}` test - then take all rows belonging to each. Now the patient sets are
disjoint by construction, and the row counts come out 21/9 rather than exactly
70/30. That imbalance is the price, and it is not negotiable: you cannot split a
patient in half.

## 3. Verify it in code

```python
records = list(range(30))
patient = {r: r // 3 for r in records}

def patients_of(rows):
    return {patient[r] for r in rows}

# Row split at 22: rows are disjoint, patients are not.
train_rows, test_rows = records[:22], records[22:]
assert set(train_rows) & set(test_rows) == set(), "rows look fine"
leak = patients_of(train_rows) & patients_of(test_rows)
assert leak == {7}, "and a patient is in both halves"

# Group split: partition the units, then collect their rows.
units = sorted(set(patient.values()))
train_units, test_units = set(units[:7]), set(units[7:])
train = [r for r in records if patient[r] in train_units]
test = [r for r in records if patient[r] in test_units]

# The three conditions.
assert set(train) | set(test) == set(records)                  # exhaustive
assert set(train) & set(test) == set()                         # disjoint rows
assert patients_of(train) & patients_of(test) == set()         # disjoint UNITS
assert len(train) == 21 and len(test) == 9

# Three-way split, all pairwise intersections empty.
tr, va, te = set(units[:6]), set(units[6:8]), set(units[8:])
assert tr & va == va & te == tr & te == set()
assert tr | va | te == set(units)

# Time series: disjoint is not enough, the split must be chronological.
times = list(range(100))
random_train, random_test = set(times[::2]), set(times[1::2])
assert random_train & random_test == set(), "disjoint..."
assert max(random_train) > min(random_test), "...and still leaks the future"

chrono_train, chrono_test = set(times[:80]), set(times[80:])
assert max(chrono_train) < min(chrono_test), "no future information in training"
```

## 4. The mistake people actually make

**Checking that the split is disjoint without checking what it is disjoint in.**

`set(train) & set(test) == set()` over row indices always passes for any
positional split, because a row index cannot be in two slices. The assertion
looks like a leakage check and tests nothing about leakage.

The assertion that matters names the unit:

```python
assert units_of(train) & units_of(test) == set()
```

and the work is in defining `units_of` correctly - which is a question about the
data, not about the code.

Two further leaks that a disjointness check will never catch:

- **Fitting the scaler on all the data before splitting.** The test set's mean
  and variance influence the training transformation. The sets are disjoint; the
  information is not.
- **Selecting features using the full dataset.** Same shape of error: the choice
  of columns was informed by the test rows.

The rule that covers all three: anything fitted must be fitted on training data
only, and the split must come first.

---

## Check yourself

1. Why can a positional row split satisfy disjointness and still leak?
2. Give the three pairwise assertions for a train/validation/test split.
3. For a time series, why is a random disjoint split still invalid?

<details>
<summary>Answers</summary>

1. Because rows are disjoint by construction, while the unit of independence - patient, user, document - can still appear on both sides. Disjointness of rows says nothing about disjointness of units.
2. `train & val == ∅`, `val & test == ∅`, and `train & test == ∅`, each computed over the unit ids rather than row indices.
3. Because training rows can come from after the test period, so the model sees future information. The split must be chronological: every training timestamp must precede every test timestamp.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](22_Label_Sets_and_OneHot_Encoding.md) · [Module README](../README.md) · [Next →](24_Set_Operations_in_NumPy_and_Pandas.md)
