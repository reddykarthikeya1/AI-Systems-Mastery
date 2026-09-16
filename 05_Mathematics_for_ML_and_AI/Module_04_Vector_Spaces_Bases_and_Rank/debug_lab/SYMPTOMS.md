# Debug Lab 04 - Symptoms

> A rank and null-space analyser used to decide whether a feature matrix is full rank. Each verdict is almost right.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_rank_analysis.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The exact case is right

```
    rows: [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 1.0, 1.0]]
    rank reported: 2   (row 2 is exactly 2x row 1)
```

Row 2 is exactly twice row 1, so the rank is 2. Correct.

**Ask yourself:** what made this case easy, and will the next one share that property?

---

## Section 2 - The same structure in decimals reports a different rank

```
    rows: [[0.1, 0.2, 0.3], [0.3, 0.6, 0.9], [1.0, 1.0, 1.0]]
    rank reported: 3   (row 2 is exactly 3x row 1)
    last row after elimination: ['0.000e+00', '0.000e+00', '2.220e-16']
```

Row 2 is exactly three times row 1, so this matrix has rank 2 just as the last one did. It is reported as 3.

The last line shows why: after elimination the final row is not zero, it is something around 2e-16.

Note that the previous section's matrix eliminated to exact zeros and this one does not. Nothing about the mathematics changed - only whether the particular decimals happen to be representable in binary.

**Ask yourself:** `0.1 + 0.2 == 0.3` is False in binary floating point. What does that do to a test written as `v != 0`?

---

## Section 3 - Rank plus nullity does not equal the number of columns

```
    shape: 2 rows x 4 columns
    rank: 2
    nullity reported: 0
    rank + nullity = 2
```

The rank-nullity theorem says rank + nullity = number of **columns**. This matrix has 4 columns, rank 2, so the nullity should be 2 and the sum should be 4.

**Ask yourself:** read `nullity` and check which dimension it subtracts from. On a square matrix this bug is invisible.

---
