# Module 13 — Problem Bank

Backtracking is the pattern to reach for when the problem asks for **all**
valid configurations. That phrasing alone rules out DP: DP compresses the state
space, which is exactly what destroys the individual answers.

Two bugs account for most backtracking failures, and both appear in this set:

* **Appending the path instead of a copy of it.** `out.append(path)` stores a
  reference to a list you are about to mutate, so every result ends up
  identical. It must be `path[:]`.
* **Forgetting to undo.** Every `append` needs its matching `pop`.

The third thing worth internalising is that **pruning is where the speed lives**
— problem 07 is intractable without it and instant with it.

**8 problems** · Easy 0 · Medium 6 · Hard 2

---

## How to work these

```bash
cd problems
python -m pytest tests -q                 # all of this module's problems
python -m pytest tests -q -k p03          # just problem 3
```

Every problem must **fail** before you start — each stub raises
`NotImplementedError`. Fill in `pNN_<slug>.py`, not the solution file.

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Jumping to the reference solution costs you the exact skill the problem
exists to build.

When you are done, compare against `solutions/pNN_<slug>.py` — not to check the
answer, which the tests already did, but to compare *approach* and complexity.

---

## Problems

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [All Subsets](p01_subsets.py) | Backtracking | Medium | `Time O(n * 2^n), Space O(n) excluding output` |
| 02 | [All Permutations](p02_permutations.py) | Backtracking with a used set | Medium | `Time O(n * n!), Space O(n) excluding output` |
| 03 | [Subsets With Duplicates](p03_subsets_with_dups.py) | Backtracking with duplicate skipping | Medium | `Time O(n * 2^n), Space O(n) excluding output` |
| 04 | [Combination Sum](p04_combination_sum.py) | Backtracking with reuse | Medium | `Time O(n^(target/min)) worst case, Space O(target/min)` |
| 05 | [Generate Valid Parentheses](p05_generate_parentheses.py) | Backtracking with validity pruning | Medium | `Time O(4^n / sqrt(n)) (Catalan), Space O(n)` |
| 06 | [Word Search In A Grid](p06_word_search.py) | Backtracking on a grid | Medium | `Time O(rows*cols*4^len(word)), Space O(len(word))` |
| 07 | [N-Queens](p07_n_queens.py) | Backtracking with constraint pruning | Hard | `Time O(n!) with heavy pruning, Space O(n)` |
| 08 | [Palindrome Partitioning](p08_palindrome_partition.py) | Backtracking with a validity check | Hard | `Time O(n * 2^n), Space O(n) excluding output` |

## Patterns covered

- Backtracking
- Backtracking on a grid
- Backtracking with a used set
- Backtracking with a validity check
- Backtracking with constraint pruning
- Backtracking with duplicate skipping
- Backtracking with reuse
- Backtracking with validity pruning

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
