# Debug Lab 13 — Symptoms

> A configuration enumerator: subsets, permutations, sum combinations and
constraint placement. Backtracking bugs corrupt the output rather than crashing.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_enumerator.py
echo "exit=$?"
```

There are **4** distinct defects.

---

## Symptom 1 — Every subset comes back empty

```
[1] All subsets
      [1, 2] -> [[], [], [], []]
          produced 4 subsets, 1 distinct (expected 4 of each)
      [1, 2, 3] -> [[], [], [], [], [], [], [], []]
          produced 8 subsets, 1 distinct (expected 8 of each)
```

**Questions to answer:**

- How many subsets were produced, and how many are distinct? Is the count right?
- What are the contents of each one?
- `path` is a single list that is mutated throughout the search. What does `out.append(path)` store — a snapshot, or a reference?

## Symptom 2 — Permutations are produced but the `used` flag is never cleared

```
[2] target=6
          reported []
          expected [[2, 2, 2]]
      [2, 3, 5] target=8
          reported [[3, 5]]
          expected [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
```

**Questions to answer:**

- How many permutations were produced versus how many exist?
- Trace `[1, 2]`. After the branch starting with 1 completes, is index 0 marked used or free?
- There are two pieces of state to undo after the recursive call. Find both. Is each one restored?

## Symptom 3 — Candidates cannot be reused

```
[3] Combination sum (candidates may be REUSED)
      [2, 3, 6, 7] target=7
          reported [[7]]
          expected [[2, 2, 3], [7]]
```

**Questions to answer:**

- Which combinations are missing from the reported output? What do the missing ones have in common?
- The problem says a candidate may be used any number of times. For `[2]` with target 6, how many times must 2 be used?
- Look at the recursive call. What index does it pass, and what does that index allow the next level to choose from?

## Symptom 4 — N-Queens finds too many solutions

```
[4] N-Queens solution counts
      n=1 -> 1     (known 1)
      n=2 -> 1     (known 0)
      n=3 -> 3     (known 0)
      n=4 -> 7     (known 2)
      n=5 -> 23    (known 10)
      n=6 -> 83    (known 4)
      n=7 -> 405   (known 40)
      n=8 -> 2113  (known 92)

====================================================================
Enumeration complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Compare every row against the known column. From which n do they start to diverge, and in which direction?
- Place a queen at (0, 0) and another at (1, 1). Do they attack each other? Now try (0, 1) and (1, 0).
- `row - col` is constant along one diagonal. Which quantity is constant along the other one, and does the code track it at all?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_subsets` |
| 2 | `test_p02_permutations` |
| 3 | `test_p04_combination_sum` |
| 4 | `test_p07_n_queens` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
