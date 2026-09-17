# Module 07 — Problem Bank

The single most useful trick in this module is counter-intuitive: to find the
**k largest** elements you keep a **min**-heap of size k, not a max-heap. The
root is then the smallest of your current best k, which is exactly the element
to evict when something better arrives.

Getting that backwards is the most common heap mistake, and it costs you
`O(n log n)` instead of `O(n log k)`.

**8 problems** · Easy 1 · Medium 4 · Hard 3

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
| 01 | [K-th Largest Element](p01_kth_largest.py) | Min-heap of size k | Medium | `Time O(n log k), Space O(k)` |
| 02 | [Merge K Sorted Lists](p02_merge_k_sorted.py) | Min-heap k-way merge | Hard | `Time O(N log k), Space O(k)` |
| 03 | [Median From A Data Stream](p03_streaming_median.py) | Two heaps | Hard | `Time O(n log n) total, O(1) per query, Space O(n)` |
| 04 | [K Closest Points To The Origin](p04_k_closest_points.py) | Max-heap of size k | Medium | `Time O(n log k), Space O(k)` |
| 05 | [Last Stone Weight](p05_last_stone_weight.py) | Max-heap simulation | Easy | `Time O(n log n), Space O(n)` |
| 06 | [Minimum Meeting Rooms](p06_min_meeting_rooms.py) | Heap of end times | Medium | `Time O(n log n), Space O(n)` |
| 07 | [Task Scheduler With Cooldown](p07_task_scheduler.py) | Greedy counting (heap-free) | Medium | `Time O(n), Space O(alphabet)` |
| 08 | [Reorganize String](p08_reorganize_string.py) | Greedy with a max-heap | Hard | `Time O(n log 26), Space O(n)` |

## Patterns covered

- Greedy counting (heap-free)
- Greedy with a max-heap
- Heap of end times
- Max-heap of size k
- Max-heap simulation
- Min-heap k-way merge
- Min-heap of size k
- Two heaps

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
| **1** | **Read Requirements** | Review problem docstrings and invariants in `[p01_kth_largest.py](p01_kth_largest.py)`. |
| **2** | **Implement Solution** | Write your algorithmic solution in `problems/` to satisfy all edge cases. |
| **3** | **Run Pytest Suite** | Execute `pytest tests/` in terminal or the web Practice Arena to verify test assertions. |
| **4** | **Review Reference Code** | Inspect `[solutions/](solutions/)` to compare time/space complexity and idiomatic patterns. |

