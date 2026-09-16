# Debug Lab 06 — Answers

> Read this only after you have written a diagnosis for each symptom.

4 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — A tree that is not a BST is approved

**Location:** `is_valid_bst`, the parent/child comparisons

**The bug:**

```python
if root.left is not None and root.left.val >= root.val:
    return False
if root.right is not None and root.right.val <= root.val:
    return False        # only the IMMEDIATE children are ever checked
```

**The fix:**

```python
def check(node, low: float, high: float) -> bool:
    if node is None:
        return True
    if not (low < node.val < high):
        return False
    # Descending left tightens the ceiling; descending right raises the floor.
    return check(node.left, low, node.val) and check(node.right, node.val, high)

return check(root, float("-inf"), float("inf"))
```

**Why it matters.** The BST property is global: every node in a left subtree must be less than the
node, not merely the child that hangs directly off it. Checking only immediate
children is a local test for a global invariant, and it passes trees that are not
BSTs.

`[5, 1, 4, None, None, 3, 6]` is the canonical counterexample. Node 4's children
3 and 6 satisfy every local comparison, but 3 lies in 5's right subtree while
being smaller than 5. The function approves it.

The consequence is not cosmetic: approving a non-BST as a search index means
lookups silently miss keys that are present. Every node is constrained by *all*
of its ancestors, which is what carrying a `(low, high)` range down the recursion
expresses.

**Proved by:** `test_p04_is_valid_bst`

## Defect 2 — Every depth is one too large

**Location:** `max_depth`, the base case

**The bug:**

```python
if root is None:
    return 1        # an empty tree has depth 0, not 1
```

**The fix:**

```python
if root is None:
    return 0
```

**Why it matters.** The base case claims an absent subtree has depth 1, so every leaf's depth is
inflated by one and the error propagates all the way to the root.

The reported numbers are small positive integers of exactly the right shape, and
the relative comparison between two trees is still correct — so anything that
only ranks trees by depth behaves fine. Only the absolute value is wrong, which
is the sort of error that surfaces much later, in whatever consumes the number.

A recursion's base case is a specification, not a formality. Ask what the answer
is for the empty input and write that.

**Proved by:** `test_p03_max_depth`

## Defect 3 — An unbalanced tree is reported as balanced

**Location:** `is_balanced`, the single top-level check

**The bug:**

```python
return abs(height(root.left) - height(root.right)) <= 1
# checked at the root only - never recursed into the subtrees
```

**The fix:**

```python
UNBALANCED = -1

def height(node) -> int:
    if node is None:
        return 0
    left = height(node.left)
    if left == UNBALANCED:
        return UNBALANCED
    right = height(node.right)
    if right == UNBALANCED:
        return UNBALANCED
    if abs(left - right) > 1:
        return UNBALANCED       # verdict propagates upward
    return 1 + max(left, right)

return height(root) != UNBALANCED
```

**Why it matters.** Height-balance is a property of every node, and this checks only the root. A
tree whose root is perfectly balanced can contain a deeply skewed subtree, and
the function approves it.

The last case in the output is exactly that: the root's two subtree heights
differ by 2 — no wait, they differ by acceptable amounts at the root while the
left subtree is a chain. The verdict is a plausible boolean either way, so
nothing signals that most of the tree was never examined.

The fix also removes an O(n²) recomputation: returning the verdict *through* the
height, with a sentinel, computes both in one bottom-up pass.

**Proved by:** `test_p07_is_balanced`

## Defect 4 — Level order returns one node per level

**Location:** `level_order`, the grouping

**The bug:**

```python
while queue:
    node = queue.popleft()
    out.append([node.val])      # one group per NODE, not per level
```

**The fix:**

```python
while queue:
    # Snapshot the width BEFORE enqueuing children: that is the level size.
    level_size = len(queue)
    level = []
    for _ in range(level_size):
        node = queue.popleft()
        level.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    out.append(level)
```

**Why it matters.** The traversal order is correct — BFS does visit nodes level by level — but each
node is wrapped in its own list, so the level structure is lost. The output is a
list of singleton lists in the right sequence, which flattens to exactly the
right answer and therefore looks almost right.

Anything that only reads the flattened order works. Anything that relies on the
grouping — rendering a tree by rows, computing per-level aggregates — gets the
wrong shape.

The trick is one line: `len(queue)` at the top of the loop is precisely the
number of nodes on the current level, because nothing from the next level has
been enqueued yet.

**Proved by:** `test_p02_level_order`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | A tree that is not a BST is approved | No |
| 2 | Every depth is one too large | No |
| 3 | An unbalanced tree is reported as balanced | No |
| 4 | Level order returns one node per level | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
