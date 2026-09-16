# Module 11 — Problem Bank

Two-dimensional DP is the same four questions as 1D — the state simply has two
coordinates. What is new is the **space optimisation**: when `dp[i]` depends
only on `dp[i-1]`, you can collapse the table to one or two rows.

That optimisation has a trap, and problem 04 is built around it. For 0/1
knapsack the single-row version must iterate the capacity **backwards**;
forwards silently turns it into *unbounded* knapsack, letting each item be used
many times. It produces a plausible larger number and no error at all.

**8 problems** · Easy 0 · Medium 5 · Hard 3

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
| 01 | [Unique Paths In A Grid](p01_unique_paths.py) | 2D grid DP | Medium | `Time O(m*n), Space O(n)` |
| 02 | [Minimum Path Sum](p02_min_path_sum.py) | 2D grid DP | Medium | `Time O(rows*cols), Space O(cols)` |
| 03 | [Edit Distance](p03_edit_distance.py) | 2D sequence DP | Hard | `Time O(n*m), Space O(min(n, m))` |
| 04 | [0/1 Knapsack](p04_knapsack_01.py) | 0/1 knapsack DP | Hard | `Time O(n*capacity), Space O(capacity)` |
| 05 | [Partition Equal Subset Sum](p05_can_partition.py) | Subset-sum DP | Medium | `Time O(n * total/2), Space O(total/2)` |
| 06 | [Longest Common Subsequence](p06_lcs.py) | 2D sequence DP | Medium | `Time O(n*m), Space O(min(n, m))` |
| 07 | [Unique Paths With Obstacles](p07_unique_paths_obstacles.py) | 2D grid DP with blocked cells | Medium | `Time O(rows*cols), Space O(cols)` |
| 08 | [Longest Palindromic Subsequence](p08_longest_palindromic_subseq.py) | Interval DP | Hard | `Time O(n^2), Space O(n^2)` |

## Patterns covered

- 0/1 knapsack DP
- 2D grid DP
- 2D grid DP with blocked cells
- 2D sequence DP
- Interval DP
- Subset-sum DP

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
