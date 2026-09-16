# Module 02 — Problem Bank

This is the highest-yield problem set in the course. Two pointers, sliding
window and prefix sums between them cover an enormous share of real interview
problems, and the three are easy to confuse.

Pay particular attention to problems 03 and 04: they look almost identical and
require *different* techniques, because a sliding window needs the window's
validity to be monotone and a sum-equals-k condition with negative numbers is
not. That distinction is the lesson.

**8 problems** · Easy 2 · Medium 6 · Hard 0

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
| 01 | [Two Sum](p01_two_sum.py) | Hash map complement | Easy | `Time O(n), Space O(n)` |
| 02 | [Maximum Sum Of A Fixed-Size Window](p02_max_window_sum.py) | Sliding window (fixed) | Easy | `Time O(n), Space O(1)` |
| 03 | [Longest Substring With At Most K Distinct Characters](p03_longest_k_distinct.py) | Sliding window (variable) | Medium | `Time O(n), Space O(k)` |
| 04 | [Count Subarrays Summing To K](p04_subarray_sum_k.py) | Prefix sums + hash map | Medium | `Time O(n), Space O(n)` |
| 05 | [Product Of Array Except Self](p05_product_except_self.py) | Prefix/suffix products | Medium | `Time O(n), Space O(1) beyond the output` |
| 06 | [Least Ship Capacity To Deliver In D Days](p06_min_ship_capacity.py) | Binary search on the answer | Medium | `Time O(n log(sum)), Space O(1)` |
| 07 | [Three Sum](p07_three_sum.py) | Sorting + two pointers | Medium | `Time O(n^2), Space O(1) beyond the output` |
| 08 | [Longest Palindromic Substring](p08_longest_palindrome.py) | Expand around centre | Medium | `Time O(n^2), Space O(1)` |

## Patterns covered

- Binary search on the answer
- Expand around centre
- Hash map complement
- Prefix sums + hash map
- Prefix/suffix products
- Sliding window (fixed)
- Sliding window (variable)
- Sorting + two pointers

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
