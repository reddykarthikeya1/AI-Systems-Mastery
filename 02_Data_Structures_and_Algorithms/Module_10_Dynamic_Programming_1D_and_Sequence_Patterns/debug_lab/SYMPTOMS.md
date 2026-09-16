# Debug Lab 10 — Symptoms

> A planning service built on one-dimensional DP: change-making, non-adjacent
selection, longest runs and product maximisation.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_dp_planner.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — An impossible amount is reported as costing zero coins

```
[1] Fewest coins to make an amount
      coins=[1, 2, 5] amount=11  -> 3 (expected 3)
      coins=[2] amount=3   -> 1 (expected impossible)
      coins=[1, 3, 4] amount=6   -> 2 (expected 2)
      coins=[7, 11] amount=5   -> 0 (expected impossible)
      coins=[5] amount=0   -> 0 (expected 0)
```

**Questions to answer:**

- Which rows disagree? What do those coin sets have in common?
- With coins `[2]` and amount 3, can any combination reach 3 exactly?
- Look at the `else 0` branch. What does `best[a] = 0` claim about amount `a`, and is that claim ever true for a positive `a`?

## Symptom 2 — Non-adjacent selection forces alternation

```
[2] Maximum non-adjacent sum
      [1, 2, 3, 1] -> 4 (expected 4)
      [2, 7, 9, 3, 1] -> 12 (expected 12)
```

**Questions to answer:**

- Which rows disagree? For `[2, 1, 1, 2]` the answer should be 4 — which two elements give that?
- The constraint is that two *adjacent* elements cannot both be taken. Does it require that every other element be taken?
- Trace the two variables on `[2, 1, 1, 2]`. Does `take` ever have the option of skipping an element and keeping its previous total?

## Symptom 3 — Equal values extend the increasing subsequence

```
[3] Longest strictly increasing subsequence
      [10, 9, 2, 5, 3, 7, 101, 18] -> 4 (expected 4)
      [7, 7, 7, 7] -> 4 (expected 1)
      [1, 2, 2, 3] -> 4 (expected 3)
      [2, 2] -> 2 (expected 1)
```

**Questions to answer:**

- Which rows disagree? What do the disagreeing inputs contain that the others do not?
- For `[7, 7, 7, 7]` the answer should be 1. What was reported, and what subsequence would justify that number?
- The problem says *strictly* increasing. Read the comparison in the inner loop — what does it do when two values are equal?

## Symptom 4 — A negative product should have become the maximum

```
[4] Maximum product subarray
      [2, 3, -2, 4] -> 6 (expected 6)
      [-2, 3, -4] -> 3 (expected 24)
      [-1, -2, -3, -4] -> 12 (expected 24)
      [-2, 0, -1] -> 0 (expected 0)

====================================================================
Planning complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Which rows disagree? What do those arrays contain that the others do not?
- For `[-2, 3, -4]` the best product is 24. Which elements produce it, and what is the sign of the product of the first two?
- The running state is a single 'best so far'. What does multiplying by a negative number do to a running maximum — and what would you need to have kept in order to exploit it?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p03_coin_change_min` |
| 2 | `test_p02_house_robber` |
| 3 | `test_p04_lis` |
| 4 | `test_p07_max_product_subarray` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
