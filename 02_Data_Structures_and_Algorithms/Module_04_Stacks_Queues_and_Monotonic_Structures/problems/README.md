# Module 04 — Problem Bank

The monotonic stack is the highest-value idea in this module and the one people
most often fail to recognise. Any time a problem asks for the *next* or
*previous* element that is greater or smaller, it is a monotonic stack, and the
solution is O(n) even though the code has a `while` nested inside a `for`.

Being able to explain why that nesting is still linear — each index is pushed
once and popped at most once — is a genuine interview differentiator.

**8 problems** · Easy 1 · Medium 5 · Hard 2

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
| 01 | [Valid Parentheses](p01_balanced_brackets.py) | Stack | Easy | `Time O(n), Space O(n)` |
| 02 | [Next Greater Element](p02_next_greater.py) | Monotonic stack | Medium | `Time O(n), Space O(n)` |
| 03 | [Daily Temperatures](p03_daily_temperatures.py) | Monotonic stack | Medium | `Time O(n), Space O(n)` |
| 04 | [Largest Rectangle In A Histogram](p04_largest_rectangle.py) | Monotonic stack | Hard | `Time O(n), Space O(n)` |
| 05 | [Sliding Window Maximum](p05_sliding_window_max.py) | Monotonic deque | Hard | `Time O(n), Space O(k)` |
| 06 | [Min Stack (O(1) Minimum)](p06_min_stack.py) | Stack with auxiliary state | Medium | `Time O(1) per operation, Space O(n)` |
| 07 | [Evaluate Reverse Polish Notation](p07_eval_rpn.py) | Stack | Medium | `Time O(n), Space O(n)` |
| 08 | [Decode String](p08_decode_string.py) | Stack of contexts | Medium | `Time O(output length), Space O(depth + output)` |

## Patterns covered

- Monotonic deque
- Monotonic stack
- Stack
- Stack of contexts
- Stack with auxiliary state

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
| **1** | **Read Requirements** | Review problem docstrings and invariants in `[p01_balanced_brackets.py](p01_balanced_brackets.py)`. |
| **2** | **Implement Solution** | Write your algorithmic solution in `problems/` to satisfy all edge cases. |
| **3** | **Run Pytest Suite** | Execute `pytest tests/` in terminal or the web Practice Arena to verify test assertions. |
| **4** | **Review Reference Code** | Inspect `[solutions/](solutions/)` to compare time/space complexity and idiomatic patterns. |

