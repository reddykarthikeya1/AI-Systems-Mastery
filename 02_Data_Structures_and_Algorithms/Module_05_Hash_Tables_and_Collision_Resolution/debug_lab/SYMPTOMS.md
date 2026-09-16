# Debug Lab 05 — Symptoms

> A hash-map toolkit used by a text-analytics job: anagram grouping, frequency
ranking, consecutive-run detection and duplicate-window checks.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_hash_toolkit.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — Non-anagrams are grouped together

```
[1] Anagram grouping
      ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
          -> [['bat'], ['eat', 'tea', 'ate'], ['tan', 'nat']]
      ['aab', 'abb']
          -> [['aab', 'abb']]
          NOTE: group ['aab', 'abb'] contains words that are not anagrams
      ['ab', 'aab', 'abb', 'aabb']
          -> [['ab', 'aab', 'abb', 'aabb']]
          NOTE: group ['ab', 'aab', 'abb', 'aabb'] contains words that are not anagrams
```

**Questions to answer:**

- Read the NOTE lines. Which words were grouped together that are not anagrams of each other?
- `"aab"` and `"abb"` use the same letters. Are they anagrams?
- What does `frozenset("aab")` evaluate to? What information about the word does a set discard?

## Symptom 2 — Frequency ties come out in an unpredictable order

```
[2] Top-k frequent elements
      [1, 1, 1, 2, 2, 3] k=2 -> [1, 2]
      [3, 2, 1] k=2 -> [3, 2]
      [1, 2, 3] k=3 -> [1, 2, 3]
      (ties must break by ascending value, so [3,2,1] k=2 -> [1, 2])
```

**Questions to answer:**

- For `[3, 2, 1]` with k=2, every value appears once. What was returned, and what does the note say it should be?
- The sort key is `-kv[1]`. What decides the relative order of two items with the same count?
- Would the answer change if the input were `[1, 2, 3]` instead? Should it?

## Symptom 3 — The consecutive-run scan is quadratic

```
[3] Longest consecutive run (with elapsed time)
      [100, 4, 200, 1, 3, 2] -> 4      (expected 4     ) took      0.00 ms
      range(5000)      -> 5000   (expected 5000  ) took    780.26 ms
      range(20000)     -> 20000  (expected 20000 ) took  12936.18 ms
      (the input quadrupled from 5000 to 20000 - what did the time do?)
```

**Questions to answer:**

- The answers are all correct. Read the elapsed-time column: the input grew by 4x between the last two rows. By what factor did the time grow?
- For `range(20000)`, how many times is the run starting at 0 walked from beginning to end?
- The problem asks for O(n). What condition would let you skip a starting point that is in the middle of a run you have already walked?

## Symptom 4 — The distance limit is ignored entirely

```
[4] Duplicate within distance k
      [1, 2, 3, 1] k=3 -> True (expected True)
      [1, 2, 3, 1] k=2 -> True (expected False)
      [1, 2, 3, 1, 2, 3] k=2 -> True (expected False)
      [1, 1] k=0 -> True (expected False)

====================================================================
Toolkit check complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Which rows disagree with the expected column? Look at the `k` value in each.
- Where does `k` appear in the body of the function?
- The set is named `window`. How many elements does it actually hold by the end of the loop, and how many should a window of size k hold?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_group_anagrams` |
| 2 | `test_p02_top_k_frequent` |
| 3 | `test_p03_longest_consecutive` |
| 4 | `test_p05_contains_nearby_duplicate` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
