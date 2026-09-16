# Debug Lab 11 — Symptoms

> A resource-allocation planner: knapsack selection, partitioning, grid routing
and sequence alignment. All four tables are the right shape.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_knapsack_planner.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — Knapsack takes the same item more than once

```
[1] 0/1 knapsack (each item available ONCE)
      weights=[1, 3, 4, 5] values=[1, 4, 5, 7] cap=7 -> 9 (expected 9)
      weights=[1] values=[10] cap=3 -> 30 (expected 10)
      weights=[2, 3] values=[10, 12] cap=6 -> 30 (expected 22)
      weights=[2, 2, 3] values=[3, 4, 5] cap=5 -> 9 (expected 9)
```

**Questions to answer:**

- Which rows disagree? For `weights=[1], values=[10], cap=3` the answer should be 10 — what was reported, and how many copies of the single item does that imply?
- The one-row optimisation reuses `best[c - w]` from the same pass. When `c` increases, has `best[c - w]` already been updated with the current item?
- Which direction would guarantee that `best[c - w]` still holds the value from *before* this item was considered?

## Symptom 2 — An odd total is partitioned into two equal halves

```
[2] Equal-sum partition
      [1, 5, 11, 5] -> True (expected True)
      [1, 2, 3, 5] -> True (expected False)
      [1, 1] -> True (expected True)
      [1, 3] -> True (expected False)
      [2, 2, 1, 1] -> True (expected True)
```

**Questions to answer:**

- Which rows disagree? Add up each input. What do the failing ones have in common?
- For `[1, 3]` the total is 4 and half is 2. Is 2 reachable from those two numbers? Now try `[1, 2, 3, 5]`, whose total is 11.
- What does `total // 2` evaluate to when `total` is odd, and does `target + target` still equal `total`?

## Symptom 3 — Every grid path cost is far too low

```
[3] Minimum grid path sum
      [[1, 3, 1], [1, 5, 1], [4, 2, 1]] -> 3 (expected 7)
      [[1, 2, 3], [4, 5, 6]] -> 9 (expected 12)
      [[1, 2], [1, 1]] -> 3 (expected 3)
```

**Questions to answer:**

- Which rows disagree? Is the reported cost higher or lower than expected?
- For `[[1,3,1],[1,5,1],[4,2,1]]` the answer is 7. Is there ANY path through that grid costing what was reported?
- Write down in one sentence what `best[c]` is supposed to mean. Now read the line that initialises it. Do the two agree for the cell at column 2 of row 0?

## Symptom 4 — The common subsequence is too short

```
[4] Longest common subsequence
      'abcde' vs 'ace' -> 3 (expected 3)
      'abc' vs 'abc' -> 3 (expected 3)
      'abcd' vs 'dcba' -> 1 (expected 1)
      'abcdefg' vs 'aceg' -> 4 (expected 4)
      'aa' vs 'aaa' -> 2 (expected 2)

====================================================================
Allocation complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Which rows disagree? Is the reported length larger or smaller than expected?
- For `'abcdefg'` vs `'aceg'` the answer should be 4. What was reported?
- In the mismatch branch, the two options are 'drop a character from `a`' and 'drop one from `b`'. Which array positions represent those two options — and is one of them being read from the wrong place?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p04_knapsack_01` |
| 2 | `test_p05_can_partition` |
| 3 | `test_p02_min_path_sum` |
| 4 | `test_p06_lcs` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
