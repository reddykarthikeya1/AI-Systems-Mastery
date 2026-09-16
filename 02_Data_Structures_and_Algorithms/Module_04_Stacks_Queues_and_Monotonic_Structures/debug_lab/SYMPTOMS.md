# Debug Lab 04 — Symptoms

> A stack-and-deque toolkit: bracket validation, next-greater-element, daily
temperatures and a sliding-window maximum. All four have the same shape, and all
four are subtly wrong.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_monotonic_toolkit.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — An unclosed bracket is reported as balanced

```
[1] Bracket validation
      '()'       -> True   (expected True)
      '()[]{}'   -> True   (expected True)
      '{[()]}'   -> True   (expected True)
      '([)]'     -> False  (expected False)
      '('        -> True   (expected False)
      '([]'      -> True   (expected False)
      ')'        -> False  (expected False)
```

**Questions to answer:**

- Which rows disagree with the expected column? What do those inputs have in common?
- For the input `"("`, walk through the loop. What is on the stack when it finishes?
- The function returns `True` at the end unconditionally. What condition should hold at that point for the string to be balanced?

## Symptom 2 — Equal values are treated as greater

```
[2] Next greater element
      [2, 1, 2, 4, 3] -> [2, 2, 4, -1, -1]   (expected [4, 2, 4, -1, -1])
      [1, 1, 2] -> [1, 2, -1]   (expected [2, 2, -1])
      [2, 2, 2] -> [2, 2, -1]   (expected [-1, -1, -1])
      [1, 2, 3] -> [2, 3, -1]   (expected [2, 3, -1])
```

**Questions to answer:**

- Which inputs disagree with the expected column? What do the disagreeing positions have in common?
- For `[1, 1, 2]`, what does the function report for index 0, and is that value strictly greater than 1?
- Look at the `while` comparison. The problem asks for the next STRICTLY greater element. What does `<=` do when the two values are equal?

## Symptom 3 — Daily temperatures reports an index instead of a wait

```
[3] Daily temperatures (days to wait)
      [73, 74, 75, 71, 69, 72, 76, 73] -> [1, 2, 6, 5, 5, 6, 0, 0]
          expected [1, 1, 4, 2, 1, 1, 0, 0]
      [30, 40, 50, 60] -> [1, 2, 3, 0]
          expected [1, 1, 1, 0]
      [50, 50, 51] -> [2, 2, 0]
          expected [2, 1, 0]
```

**Questions to answer:**

- Compare the reported and expected rows. Are the reported values larger or smaller, and is there a pattern to the difference?
- The question is 'how many days must you wait'. What quantity is being stored in `out[j]`?
- For index 0 of the first example the answer should be 1. What was reported, and what is `i` at the moment index 0 is resolved?

## Symptom 4 — The sliding-window maximum reports stale values

```
[4] Sliding window maximum
      [1, 3, -1, -3, 5, 3, 6, 7] k=3
          reported [3, 3, 5, 5, 6, 7]
          expected [3, 3, 5, 5, 6, 7]
      [5, 4, 3, 2, 1] k=2
          reported [5, 5, 5, 5]
          expected [5, 4, 3, 2]
      [1, 2, 3, 4, 5] k=2
          reported [2, 3, 4, 5]
          expected [2, 3, 4, 5]

====================================================================
Toolkit check complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Which of the three inputs disagrees with the expected row? What is different about that input compared with the others?
- For `[5, 4, 3, 2, 1]` with k=2, the reported first value is right and the later ones are not. What is at the front of the deque by then?
- Two evictions are needed each step: one from the back, one from the front. Find the back eviction in the code. Where is the front one?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_balanced_brackets` |
| 2 | `test_p02_next_greater` |
| 3 | `test_p03_daily_temperatures` |
| 4 | `test_p05_sliding_window_max` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
