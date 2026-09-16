# Debug Lab 01 - Symptoms

> A dataset splitter that guarantees no leakage between train, validation and test. Each guarantee is almost right.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_dataset_split.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - Every row is accounted for, and the totals still look odd

```
    rows in: 100
    train=60  validation=20  test=20
    total out: 100
    distinct rows covered: 100
    overlap train&test: 0
```

The three partitions add up to the input size and nothing overlaps, so the split itself is sound. Check the arithmetic against the fractions you asked for: 60/20/20 of 100.

**Ask yourself:** is this defect in the split, or is this section the one that is actually fine? One of the three sections here is not the bug - deciding which is part of the exercise.

---

## Section 2 - Deduplication is correct but the program is crawling

```
    raw rows: 4000  distinct values present: 500
    deduplicate() returned: 500
```

The returned count is right: 500 distinct values out of 4,000 rows. Nothing is wrong with the answer.

Time it. Then time it with 40,000 rows instead of 4,000 and watch what happens to the ratio.

**Ask yourself:** what is the cost of `row not in seen` when `seen` is a list, and how many times is it paid?

---

## Section 3 - Patients appear in both train and test

```
    patients: 10
    patients appearing in BOTH train and test: 0 []
```

This is the one that ends careers. Each patient contributes three records, and the split cuts the list at a row boundary rather than a patient boundary - so a patient's records land on both sides.

A model trained this way sees the same patient at training and at evaluation. Accuracy looks excellent and the model is worthless.

**Ask yourself:** the split is over rows. What should it be over?

---
