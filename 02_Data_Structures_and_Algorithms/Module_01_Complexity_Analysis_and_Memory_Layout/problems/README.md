# Module 01 — Problem Bank

Complexity analysis is the one module whose problems are not about writing
clever code — they are about **predicting cost before you write any**. Every
problem here has a closed-form answer you should be able to derive on paper,
and the tests check that your formula holds at sizes far beyond what you could
brute-force.

This is the module that makes Step 1 of the pattern-recognition triage possible.

**6 problems** · Easy 4 · Medium 2 · Hard 0

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
| 01 | [Classify Empirical Growth Rate](p01_classify_growth.py) | Complexity analysis | Easy | `Time O(k), Space O(k) for k measurements` |
| 02 | [Total Copies Under Geometric Growth](p02_amortized_copies.py) | Amortized analysis | Medium | `Time O(log n), Space O(1)` |
| 03 | [Worst-Case Binary Search Comparisons](p03_binary_search_steps.py) | Complexity analysis | Easy | `Time O(1), Space O(1)` |
| 04 | [Count Distinct Pair Iterations](p04_pair_iterations.py) | Complexity analysis | Easy | `Time O(1), Space O(1)` |
| 05 | [Does This Complexity Fit The Constraint?](p05_fits_budget.py) | Complexity analysis | Medium | `Time O(1) amortised, Space O(1)` |
| 06 | [Row-Major Memory Layout](p06_row_major.py) | Memory layout | Easy | `Time O(1), Space O(1)` |

## Patterns covered

- Amortized analysis
- Complexity analysis
- Memory layout

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)

---

## 🗺️ Recommended Step-by-Step Problem Solving Path

Follow this sequence to solve the module practice problems:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Read Requirements** | Review problem docstrings and invariants in `[p01_classify_growth.py](p01_classify_growth.py)`. |
| **2** | **Implement Solution** | Write your algorithmic solution in `problems/` to satisfy all edge cases. |
| **3** | **Run Pytest Suite** | Execute `pytest tests/` in terminal or the web Practice Arena to verify test assertions. |
| **4** | **Review Reference Code** | Inspect `[solutions/](solutions/)` to compare time/space complexity and idiomatic patterns. |

