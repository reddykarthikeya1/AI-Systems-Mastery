# Lesson 01.01 — Why Sets Are the Vocabulary of ML

> **Module 01:** Set Language for Machine Learning · Lesson 1 of 25

---

## What you will be able to do after this lesson

- [ ] State what changes about a dataset when you call it a *set* rather than a list, and name two bugs that distinction prevents.
- [ ] Compute the size of a train/test overlap and say why any non-zero answer invalidates an evaluation.

## Prerequisites

- None. This is the entry point for the module.

---

## 1. The idea

Machine learning is full of questions that sound like engineering and are
actually questions about sets.

*Did any training example leak into the test set?* That is
`train ∩ test = ∅`. *Does every label the model can emit correspond to a class
it was trained on?* That is `predicted ⊆ trained`. *Are these two feature
columns measuring the same thing?* That is a question about whether one set of
values determines another.

A **set** is a collection where only membership matters. Two things follow, and
both are the reason the vocabulary is worth adopting:

- **Order is irrelevant.** `{1, 2}` and `{2, 1}` are the same set.
- **Repetition is irrelevant.** `{1, 1, 2}` and `{1, 2}` are the same set.

A Python `list` has order and repetition; a `set` has neither. Choosing the
wrong one is how a dataset ends up with 4,000 rows and 500 distinct examples,
and nobody notices because the row count looks healthy.

## 2. Worked example

A dataset of 8 user ids, with duplicates:

    rows = [7, 3, 7, 1, 3, 7, 9, 1]

As a **list** it has length 8. As a **set** it is `{1, 3, 7, 9}`, size 4.

Now split it by position: the first 6 rows for training, the last 2 for test.

    train (rows 0-5) = [7, 3, 7, 1, 3, 7]  ->  as a set {1, 3, 7}
    test  (rows 6-7) = [9, 1]              ->  as a set {1, 9}

The intersection is `{1}`. User 1 appears in both. The model will be evaluated
on a user it has already seen, so the test score measures memorisation, not
generalisation.

The row counts gave no hint of this: 6 and 2, adding to 8, exactly as intended.

## 3. Verify it in code

```python
rows = [7, 3, 7, 1, 3, 7, 9, 1]

# A list keeps order and repetition; a set keeps neither.
assert len(rows) == 8
assert len(set(rows)) == 4
assert set(rows) == {1, 3, 7, 9}

# Order and repetition genuinely do not distinguish sets.
assert {1, 2} == {2, 1}
assert {1, 1, 2} == {1, 2}

train_rows, test_rows = rows[:6], rows[6:]
train, test = set(train_rows), set(test_rows)

assert len(train_rows) + len(test_rows) == len(rows)   # the counts look fine
leak = train & test
assert leak == {1}, "user 1 is in both halves"
assert leak != set(), "a non-empty intersection is a broken evaluation"

# The property an honest split must have:
clean_train, clean_test = {1, 3, 7}, {9}
assert clean_train & clean_test == set()
```

## 4. The mistake people actually make

**Splitting rows when the unit of independence is something else.**

The split above is correct *as a split of rows*. Every row lands on exactly one
side and none is lost. What makes it wrong is that rows are not independent -
several rows belong to the same user, and a user is the thing that must not
appear twice.

This is why the bug survives review. Somebody checks that the partition is
valid (it is), that the sizes are right (they are), and that nothing was
dropped (nothing was). The question nobody asks is *what is the unit here*.

The symptom is an evaluation score that is too good, and there is no error
message. It is caught by computing the intersection and asserting it is empty,
which costs one line.

---

## Check yourself

1. `rows = [5, 5, 5]`. What is `len(rows)` and what is `len(set(rows))`?
2. A colleague says their split is fine because the train and test row counts add up to the dataset size. What have they checked, and what have they not?
3. Why is `{1, 2} == {2, 1}` true but `[1, 2] == [2, 1]` false?

<details>
<summary>Answers</summary>

1. 3 and 1. The list has three elements; the set has one, because repetition does not distinguish members.
2. They have checked that the split is a partition of the rows - exhaustive and non-overlapping *by row*. They have not checked that the underlying units (user, patient, document) are disjoint, which is the property that actually matters.
3. Set equality is defined by membership alone: two sets are equal when each contains exactly the members of the other. List equality is defined element-by-element in order, so position matters.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Set_Notation_Membership_and_Equality.md)
