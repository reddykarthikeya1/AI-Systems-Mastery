# Debug Lab 12 — Symptoms

> A scheduling service: merging calendar blocks, packing the most meetings into a
day, allocating fuel stops and planning trades.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_scheduler.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — Merging a nested block shrinks the merged range

```
[1] Merging calendar blocks
      [(1, 3), (2, 6), (8, 10), (15, 18)]
          reported [(1, 6), (8, 10), (15, 18)]
          expected [(1, 6), (8, 10), (15, 18)]
      [(1, 10), (2, 3)]
          reported [(1, 3)]
          expected [(1, 10)]
      [(1, 4), (2, 3)]
          reported [(1, 3)]
          expected [(1, 4)]
      [(1, 100), (2, 3), (4, 5)]
          reported [(1, 3), (4, 5)]
          expected [(1, 100)]
```

**Questions to answer:**

- Which rows disagree? What is the relationship between the two intervals in each failing case?
- For `[(1, 10), (2, 3)]`, the second block sits entirely inside the first. What should the merged block be, and what was reported?
- Look at the merge assignment. When the incoming interval ends EARLIER than the one already accumulated, which end value survives?

## Symptom 2 — Fewer meetings are scheduled than could fit

```
[2] Maximum non-overlapping meetings
      [(1, 3), (2, 4), (3, 5)] -> 2 (expected 2)
      [(1, 10), (2, 3), (4, 5), (6, 7)] -> 1 (expected 3)
      [(0, 2), (1, 4), (3, 5), (4, 6)] -> 2 (expected 2)
```

**Questions to answer:**

- Which rows disagree? For `[(1, 10), (2, 3), (4, 5), (6, 7)]` the answer should be 3 — which three meetings?
- Which meeting does the function pick first, and what does picking it cost you?
- The previous problem sorts by start and is correct. This one sorts by start and is wrong. What is different about the question being asked?

## Symptom 3 — A trade can buy and sell on the same day

```
[3] Best single trade
      [7, 1, 5, 3, 6, 4] -> 5 (expected 5)
      [7, 6, 4, 3, 1] -> 0 (expected 0)
      [9, 1] -> 0 (expected 0)
      [2, 4, 1] -> 2 (expected 2)
      [3, 3] -> 0 (expected 0)
```

**Questions to answer:**

- Which rows disagree? Look closely at `[9, 1]` and `[3, 3]`.
- For `[9, 1]` the price only falls. What profit was reported, and is there any buy-then-sell pair that achieves it?
- Read the two `if` statements in order. On the iteration that sets a new minimum, is that same price also available as a sale price?

## Symptom 4 — An impossible circuit reports a starting station

```
[4] Gas station circuit start
      gas=[1, 2, 3, 4, 5] cost=[3, 4, 5, 1, 2] -> 3 (expected 3)
      gas=[2, 3, 4] cost=[3, 4, 3] -> 2 (expected -1)
      gas=[4] cost=[5] -> 1 (expected -1)
      gas=[3, 1, 1] cost=[1, 2, 2] -> 0 (expected 0)

====================================================================
Scheduling complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Which rows disagree? Add up the gas and the cost for each failing case.
- For `gas=[2,3,4]`, `cost=[3,4,3]`, is there enough fuel in total to complete one lap?
- The function always returns `start`, which is an index. What value should it return when no valid start exists, and where would that check go?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p02_merge_intervals` |
| 2 | `test_p03_max_non_overlapping` |
| 3 | `test_p01_max_profit_stock` |
| 4 | `test_p07_gas_station` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
