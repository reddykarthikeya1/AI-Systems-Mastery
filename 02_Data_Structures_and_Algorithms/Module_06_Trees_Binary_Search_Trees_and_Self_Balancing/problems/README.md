# Module 06 — Problem Bank

Tree problems split cleanly in two. Traversal problems are about *order* — which
node you visit when. BST problems are about *invariants* — what the structure
guarantees, and what it does not.

Problem 04 is the one worth dwelling on: almost everyone's first attempt at
validating a BST compares each node only against its immediate children, which
accepts trees that are not BSTs. The invariant is a *range*, not a local
comparison.

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
| 01 | [Iterative Inorder Traversal](p01_inorder_traversal.py) | Explicit stack traversal | Medium | `Time O(n), Space O(height)` |
| 02 | [Level Order Traversal](p02_level_order.py) | BFS | Medium | `Time O(n), Space O(width)` |
| 03 | [Maximum Depth](p03_max_depth.py) | Tree recursion | Easy | `Time O(n), Space O(height)` |
| 04 | [Validate A Binary Search Tree](p04_is_valid_bst.py) | Range invariant propagation | Medium | `Time O(n), Space O(height)` |
| 05 | [Lowest Common Ancestor In A BST](p05_lca_bst.py) | BST invariant walk | Medium | `Time O(height), Space O(1)` |
| 06 | [K-th Smallest Element In A BST](p06_kth_smallest_bst.py) | Inorder with early exit | Medium | `Time O(height + k), Space O(height)` |
| 07 | [Height-Balanced Binary Tree](p07_is_balanced.py) | Bottom-up recursion | Medium | `Time O(n), Space O(height)` |
| 08 | [Diameter Of A Binary Tree](p08_tree_diameter.py) | Bottom-up recursion with a running best | Hard | `Time O(n), Space O(height)` |

## Patterns covered

- BFS
- BST invariant walk
- Bottom-up recursion
- Bottom-up recursion with a running best
- Explicit stack traversal
- Inorder with early exit
- Range invariant propagation
- Tree recursion

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
