# Module 05 — Problem Bank

A hash map turns "have I seen this?" into an O(1) question, and an enormous
share of interview problems are exactly that question wearing a costume.

What it cannot do is answer anything about *order* or *ranges* — that is what
problem 03 is really about. Recognising when a hash map is the wrong tool is as
valuable as recognising when it is the right one.

**8 problems** · Easy 2 · Medium 5 · Hard 1

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
| 01 | [Group Anagrams](p01_group_anagrams.py) | Hash map with a canonical key | Medium | `Time O(total characters), Space O(total characters)` |
| 02 | [Top K Frequent Elements](p02_top_k_frequent.py) | Counting + bucket sort | Medium | `Time O(n), Space O(n)` |
| 03 | [Longest Consecutive Sequence](p03_longest_consecutive.py) | Hash set + sequence-start check | Medium | `Time O(n), Space O(n)` |
| 04 | [First Unique Character](p04_first_unique_char.py) | Frequency counting | Easy | `Time O(n), Space O(alphabet)` |
| 05 | [Duplicate Within Distance K](p05_contains_nearby_duplicate.py) | Sliding window + hash set | Medium | `Time O(n), Space O(min(n, k))` |
| 06 | [Isomorphic Strings](p06_is_isomorphic.py) | Two-way hash mapping | Easy | `Time O(n), Space O(alphabet)` |
| 07 | [Subarray Sums Divisible By K](p07_subarrays_div_by_k.py) | Prefix sums + modular arithmetic | Medium | `Time O(n), Space O(k)` |
| 08 | [Four Sum Count (Two Hash Maps)](p08_four_sum_count.py) | Meet in the middle with a hash map | Hard | `Time O(n^2), Space O(n^2)` |

## Patterns covered

- Counting + bucket sort
- Frequency counting
- Hash map with a canonical key
- Hash set + sequence-start check
- Meet in the middle with a hash map
- Prefix sums + modular arithmetic
- Sliding window + hash set
- Two-way hash mapping

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
| **1** | **Read Requirements** | Review problem docstrings and invariants in `[p01_group_anagrams.py](p01_group_anagrams.py)`. |
| **2** | **Implement Solution** | Write your algorithmic solution in `problems/` to satisfy all edge cases. |
| **3** | **Run Pytest Suite** | Execute `pytest tests/` in terminal or the web Practice Arena to verify test assertions. |
| **4** | **Review Reference Code** | Inspect `[solutions/](solutions/)` to compare time/space complexity and idiomatic patterns. |

