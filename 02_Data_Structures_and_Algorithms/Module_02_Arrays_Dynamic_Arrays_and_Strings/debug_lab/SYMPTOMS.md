# Debug Lab 02 — Symptoms

> An array-processing toolkit used by a reporting pipeline: window sums, subarray
counts, pair lookups and a capacity planner. Every function returns a number
that looks reasonable.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_array_toolkit.py
echo "exit=$?"
```

There are **5** distinct defects.

---

## Symptom 1 — An element pairs with itself

```
[1] Two-sum index lookup
      [2, 7, 11, 15] target=9   -> indices [0, 1] values 2+7=9 distinct=True
      [3, 2, 4] target=6   -> indices [0, 0] values 3+3=6 distinct=False
      [5, 1, 10] target=10  -> indices [0, 0] values 5+5=10 distinct=False
      [3, 3] target=6   -> indices [0, 0] values 3+3=6 distinct=False
```

**Questions to answer:**

- Look at the `distinct` column. Is any row reporting a pair whose two indices are the same?
- For `[5, 1, 10]` with target 10, is there any genuine pair summing to 10? What was reported?
- Trace the loop for that case. In what order does it insert into `seen` and check for the complement?

## Symptom 2 — An all-negative window sums to zero

```
[2] Maximum sum of a fixed window
      [2, 1, 5, 1, 3, 2] k=3 -> 9
      [-4, -2, -7, -3] k=2 -> 0
      [-1, -1] k=1 -> 0
```

**Questions to answer:**

- For `[-4, -2, -7, -3]` with k=2, every window has a negative sum. What was reported?
- Is 0 the sum of any window of length 2 in that array?
- What is `best` initialised to, and is that value ever a legal answer?

## Symptom 3 — Subarrays starting at index 0 are not counted

```
[3] k=3 -> reported 0, brute force 1
```

**Questions to answer:**

- Compare the reported and brute-force columns. Which rows disagree, and by how much?
- For `[1, 2, 3]` with k=1, which subarray sums to 1, and where does it start?
- The prefix-sum identity is `sum(i..j) == prefix[j+1] - prefix[i]`. What is `prefix[0]`, and is it in the counts map when the loop begins?

## Symptom 4 — Every reported substring length is far too short

```
[4] Longest substring with at most k distinct characters
      'eceba'          k=2 -> reported 1, brute force 3
      'aa'             k=1 -> reported 0, brute force 2
      'abcadcacacaca'  k=3 -> reported 8, brute force 11
      'abaccc'         k=2 -> reported 3, brute force 4
```

**Questions to answer:**

- Compare the reported and brute-force columns. Every row disagrees. Are the reported values too high or too low?
- For k=2, how many distinct characters does the window actually end up holding? Print `len(counts)` at the end of each iteration and see.
- Read the shrink condition character by character. The window is allowed to hold *at most* k distinct characters. What does the condition permit?

## Symptom 5 — The ship capacity search starts below the largest package

```
[5] Minimum ship capacity
      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] days=5 -> capacity 15 (needs 5 days; heaviest package is 10)
      [3, 2, 2, 4, 1, 4] days=3 -> capacity 6 (needs 3 days; heaviest package is 4)
      [1, 1, 9] days=3 -> capacity 1 (needs 3 days; heaviest package is 9)
      [2, 2, 10] days=3 -> capacity 2 (needs 3 days; heaviest package is 10)

====================================================================
Report complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- For `[1, 1, 9]` and `[2, 2, 10]`, compare the reported capacity with the heaviest package in the same row.
- Can a ship of that capacity carry the heaviest package at all?
- Look at `days_needed`. What does it do with a package heavier than the capacity — does it report failure, or does it do something else?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_two_sum` |
| 2 | `test_p02_max_window_sum` |
| 3 | `test_p04_subarray_sum_k` |
| 4 | `test_p03_longest_k_distinct` |
| 5 | `test_p06_min_ship_capacity` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
