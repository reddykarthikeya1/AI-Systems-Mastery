# Debug Lab 07 — Symptoms

> A scheduling and ranking service built on heaps: k-th largest, k-way merge,
streaming median and meeting-room allocation.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_priority_toolkit.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — K-th largest returns the k-th smallest

```
[1] K-th largest element
      [3, 2, 1, 5, 6, 4] k=2 -> 2 (expected 5)
      [7, 3, 9, 1] k=1 -> 1 (expected 9)
      [7, 3, 9, 1] k=4 -> 9 (expected 1)
      [5, 5, 5] k=2 -> 5 (expected 5)
```

**Questions to answer:**

- Which rows are right and which are wrong? What is special about the ones that happen to be right?
- For `[7, 3, 9, 1]` with k=1 the answer should be the maximum. What was returned?
- The values are pushed negated. Which end of the heap is therefore the largest value, and which element does `heappop` remove?

## Symptom 2 — The merge stops as soon as any one list is exhausted

```
[2] Merge k sorted lists
      [[1, 4, 5], [1, 3, 4], [2, 6]]
          reported [1, 1, 2, 3, 4, 4]
          expected [1, 1, 2, 3, 4, 4, 5, 6]
      [[1, 2], [3, 4], [5, 6]]
          reported [1, 2]
          expected [1, 2, 3, 4, 5, 6]
      [[1], [2], [3]]
          reported [1]
          expected [1, 2, 3]
```

**Questions to answer:**

- Compare the reported and expected rows. How many elements came back versus how many went in?
- The `else` branch runs when one list has no more elements. What does it do to the loop?
- Is 'this particular list is finished' the same condition as 'there is nothing left to merge'?

## Symptom 3 — The median is wrong for every even-length prefix

```
[3] Streaming median
      [2, 3, 4]
          reported [2.0, 2.0, 3.0]
          expected [2.0, 2.5, 3.0]
      [5, 4, 3, 2, 1]
          reported [5.0, 4.0, 4.0, 3.0, 3.0]
          expected [5.0, 4.5, 4.0, 3.5, 3.0]
      [1, 2]
          reported [1.0, 1.0]
          expected [1.0, 1.5]
```

**Questions to answer:**

- Compare reported against expected element by element. Which positions disagree — the odd-numbered prefixes or the even-numbered ones?
- For `[1, 2]` the two values are 1 and 2. What is their median, and what was reported?
- After the rebalance, `len(lower)` is either equal to `len(upper)` or one greater. Which of those two cases means the count is even, and which branch does the code take for it?

## Symptom 4 — Meeting rooms depends on the order of the input

```
[4] Minimum meeting rooms
      [(0, 30), (5, 10), (15, 20)] -> 2 (expected 2)
      [(15, 20), (0, 30), (5, 10)] -> 3 (expected 2)
      [(1, 10), (2, 9), (3, 8)] -> 3 (expected 3)
      [(1, 2), (2, 3), (3, 4)] -> 1 (expected 1)

====================================================================
Toolkit check complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- The first two rows contain the same three meetings in a different order. Do they report the same number of rooms?
- Which rows disagree with the expected column?
- The algorithm reuses a room when the earliest end time is at or before the new start. What must be true about the order in which meetings are considered for that comparison to mean anything?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_kth_largest` |
| 2 | `test_p02_merge_k_sorted` |
| 3 | `test_p03_streaming_median` |
| 4 | `test_p06_min_meeting_rooms` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
