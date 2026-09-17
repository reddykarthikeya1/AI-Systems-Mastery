# Module 12 — Problem Bank

Greedy is the pattern people get wrong most often, because a wrong greedy passes
the examples. The examples are chosen to illustrate, not to falsify.

The single most useful fact in this module: **for intervals, sort by START to
merge and by END to schedule.** Getting that backwards gives a plausible wrong
answer with no error anywhere. Problems 02 and 03 are the same input shape with
opposite sort keys, deliberately adjacent so the difference is unmissable.

And the rule that saves you: *if you cannot prove the greedy choice is safe,
use DP.* DP is slower and always correct.

**8 problems** · Easy 1 · Medium 6 · Hard 1

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
| 01 | [Best Time To Buy And Sell Stock](p01_max_profit_stock.py) | Greedy running minimum | Easy | `Time O(n), Space O(1)` |
| 02 | [Merge Overlapping Intervals](p02_merge_intervals.py) | Sort by START, then sweep | Medium | `Time O(n log n), Space O(n)` |
| 03 | [Maximum Non-Overlapping Intervals](p03_max_non_overlapping.py) | Sort by END, then greedy | Medium | `Time O(n log n), Space O(1)` |
| 04 | [Minimum Arrows To Burst Balloons](p04_min_arrows.py) | Sort by END, then greedy | Medium | `Time O(n log n), Space O(1)` |
| 05 | [Jump Game](p05_can_jump.py) | Greedy reachability | Medium | `Time O(n), Space O(1)` |
| 06 | [Jump Game II (Fewest Jumps)](p06_min_jumps.py) | Greedy BFS by levels | Hard | `Time O(n), Space O(1)` |
| 07 | [Gas Station Circuit](p07_gas_station.py) | Greedy with a restart point | Medium | `Time O(n), Space O(1)` |
| 08 | [Partition Labels](p08_partition_labels.py) | Greedy with last-occurrence bounds | Medium | `Time O(n), Space O(alphabet)` |

## Patterns covered

- Greedy BFS by levels
- Greedy reachability
- Greedy running minimum
- Greedy with a restart point
- Greedy with last-occurrence bounds
- Sort by END, then greedy
- Sort by START, then sweep

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
| **1** | **Read Requirements** | Review problem docstrings and invariants in `[p01_max_profit_stock.py](p01_max_profit_stock.py)`. |
| **2** | **Implement Solution** | Write your algorithmic solution in `problems/` to satisfy all edge cases. |
| **3** | **Run Pytest Suite** | Execute `pytest tests/` in terminal or the web Practice Arena to verify test assertions. |
| **4** | **Review Reference Code** | Inspect `[solutions/](solutions/)` to compare time/space complexity and idiomatic patterns. |

