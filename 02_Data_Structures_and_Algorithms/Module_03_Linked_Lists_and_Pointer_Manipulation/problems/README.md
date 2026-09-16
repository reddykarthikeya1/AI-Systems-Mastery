# Module 03 — Problem Bank

Linked-list problems are pointer-discipline drills. Almost every bug here is one
of three things: losing the rest of the list before you have saved it, an
off-by-one in how far a pointer advances, or forgetting that the head itself can
be the node you need to change.

The dummy-head trick removes an entire class of those bugs, and problems 05 and
06 exist to make you reach for it.

**8 problems** · Easy 4 · Medium 3 · Hard 1

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
| 01 | [Reverse A Linked List](p01_reverse_list.py) | Pointer manipulation | Easy | `Time O(n), Space O(1)` |
| 02 | [Detect A Cycle](p02_has_cycle.py) | Fast and slow pointers | Easy | `Time O(n), Space O(1)` |
| 03 | [Find Where The Cycle Begins](p03_cycle_start.py) | Floyd's algorithm | Medium | `Time O(n), Space O(1)` |
| 04 | [Middle Of The List](p04_middle_node.py) | Fast and slow pointers | Easy | `Time O(n), Space O(1)` |
| 05 | [Merge Two Sorted Lists](p05_merge_sorted.py) | Dummy head + two pointers | Easy | `Time O(n + m), Space O(1)` |
| 06 | [Remove The N-th Node From The End](p06_remove_nth_from_end.py) | Dummy head + gap pointers | Medium | `Time O(n), Space O(1)` |
| 07 | [Palindrome Linked List](p07_is_palindrome_list.py) | Fast/slow + in-place reversal | Medium | `Time O(n), Space O(1)` |
| 08 | [Reorder List](p08_reorder_list.py) | Split + reverse + weave | Hard | `Time O(n), Space O(1)` |

## Patterns covered

- Dummy head + gap pointers
- Dummy head + two pointers
- Fast and slow pointers
- Fast/slow + in-place reversal
- Floyd's algorithm
- Pointer manipulation
- Split + reverse + weave

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
