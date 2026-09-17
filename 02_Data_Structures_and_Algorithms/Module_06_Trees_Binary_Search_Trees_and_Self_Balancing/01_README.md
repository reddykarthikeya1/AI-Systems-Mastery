# Module 06: Trees, Binary Search Trees & Self-Balancing (0 to 100 Mastery)

> **Recursive Tree Invariants, BST Search Properties, DFS/BFS & Height-Balanced Rotations**

Trees model hierarchical data and form the index engines of databases (B-Trees) and memory allocators (Red-Black trees). In this module, you master **In-Order / Pre-Order / Post-Order DFS**, **Level-Order BFS**, **BST bifurcation logic**, and **AVL self-balancing rotations**.

---


## AVL Tree Double Rotation (Left-Right Case)

```mermaid
flowchart TD
    subgraph Before["Before Rotation (Imbalance at Node 50, BF = +2)"]
        N50["50 (BF=+2)"] --> N20["20 (BF=-1)"]
        N50 --> N60["60"]
        N20 --> N10["10"]
        N20 --> N30["30 (Right Child)"]
        N30 --> N25["25"]
        N30 --> N35["35"]
    end

    subgraph Step1["Step 1: Left Rotate at Child 20"]
        S50["50"] --> S30["30"]
        S30 --> S20["20"]
        S30 --> S35["35"]
        S20 --> S10["10"]
        S20 --> S25["25"]
    end

    subgraph Step2["Step 2: Right Rotate at Root 50 (Balanced)"]
        R30["30 (BF=0)"]
        R30 --> R20["20 (BF=0)"]
        R30 --> R50["50 (BF=0)"]
        R20 --> R10["10"]
        R20 --> R25["25"]
        R50 --> R35["35"]
        R50 --> R60["60"]
    end

    Before -->|Left Rotate (Child)| Step1 -->|Right Rotate (Root)| Step2
```

## 1. Binary Tree Node Representation

```python
class TreeNode:
    def __init__(self, val: int = 0, left: TreeNode | None = None, right: TreeNode | None = None):
        self.val = val
        self.left = left
        self.right = right
```

---

## 2. Curated LeetCode Problem Breakdowns (Brute Force vs. Optimized)

### Problem 1: Invert Binary Tree ([LeetCode 226](https://leetcode.com/problems/invert-binary-tree/)) — Easy

#### Optimized: Recursive Depth-First Swap
```python
def invert_tree(root: TreeNode | None) -> TreeNode | None:
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```
- **Time Complexity**: $O(N)$ — Visits every node once.
- **Space Complexity**: $O(H)$ recursion stack, where $H = \\log N$ (balanced) or $N$ (worst-case).

---

### Problem 2: Maximum Depth of Binary Tree ([LeetCode 104](https://leetcode.com/problems/maximum-depth-of-binary-tree/)) — Easy

#### Optimized: Post-Order DFS
```python
def max_depth(root: TreeNode | None) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```
- **Time Complexity**: $O(N)$, **Space Complexity**: $O(H)$.

---

### Problem 3: Diameter of Binary Tree ([LeetCode 543](https://leetcode.com/problems/diameter-of-binary-tree/)) — Easy

#### Brute Force: Height Calculation per Node
Calling `height(node.left) + height(node.right)` at each node takes $O(N^2)$ time.

#### Optimized: Bottom-Up Post-Order DFS ($O(N)$ Time)
Return the height from each subtree, while updating a global diameter maximum at each node.
```python
def diameter_of_binary_tree(root: TreeNode | None) -> int:
    max_d = 0
    def dfs(node: TreeNode | None) -> int:
        nonlocal max_d
        if not node:
            return 0
        left_h = dfs(node.left)
        right_h = dfs(node.right)
        max_d = max(max_d, left_h + right_h)
        return 1 + max(left_h, right_h)
        
    dfs(root)
    return max_d
```
- **Time Complexity**: $O(N)$ — Exactly 1 pass.
- **Space Complexity**: $O(H)$ stack space.

---

### Problem 4: Balanced Binary Tree ([LeetCode 110](https://leetcode.com/problems/balanced-binary-tree/)) — Easy

#### Optimized: Bottom-Up Height Sentinel (-1)
If any subtree is unbalanced ($|h_{left} - h_{right}| > 1$), immediately bubble up `-1`.
```python
def is_balanced(root: TreeNode | None) -> bool:
    def check(node: TreeNode | None) -> int:
        if not node:
            return 0
        left = check(node.left)
        if left == -1:
            return -1
        right = check(node.right)
        if right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)
        
    return check(root) != -1
```
- **Time Complexity**: $O(N)$ — Early-exits on imbalance.
- **Space Complexity**: $O(H)$.

---

### Problem 5: Lowest Common Ancestor of a BST ([LeetCode 235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)) — Medium

#### Optimized: BST Value Split ($O(H)$ Time, $O(1)$ Space)
If both $p$ and $q$ are smaller than `root.val`, LCA must be in left subtree. If both are larger, LCA is in right subtree. The moment they split, `root` is the LCA.
```python
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr
    return root
```
- **Time Complexity**: $O(H)$ — Traverses one branch.
- **Space Complexity**: $O(1)$ iterative.

---

### Problem 6: Binary Tree Level Order Traversal ([LeetCode 102](https://leetcode.com/problems/binary-tree-level-order-traversal/)) — Medium

#### Optimized: Queue-Based BFS with Level Batch Sizing
```python
from collections import deque

def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []
    res = []
    q: deque[TreeNode] = deque([root])
    
    while q:
        level = []
        for _ in range(len(q)):  # Process all nodes currently in queue
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
        
    return res
```
- **Time Complexity**: $O(N)$, **Space Complexity**: $O(N/2) = O(N)$ width of tree.

---

### Problem 7: Validate Binary Search Tree ([LeetCode 98](https://leetcode.com/problems/validate-binary-search-tree/)) — Medium

#### Optimized: DFS with Valid Min/Max Value Bounds
Every node must strictly satisfy $low < node.val < high$.
```python
def is_valid_bst(root: TreeNode | None) -> bool:
    def validate(node: TreeNode | None, low: float, high: float) -> bool:
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        
    return validate(root, float("-inf"), float("inf"))
```
- **Time Complexity**: $O(N)$, **Space Complexity**: $O(H)$.

---

### Problem 8: Kth Smallest Element in a BST ([LeetCode 230](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)) — Medium

#### Optimized: Early-Stopping Iterative In-Order Traversal
In a BST, in-order traversal visits values in strictly ascending order. Pop $k$ times.
```python
def kth_smallest(root: TreeNode | None, k: int) -> int:
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
    return -1
```
- **Time Complexity**: $O(H + K)$, **Space Complexity**: $O(H)$.

---

### Problem 9: Binary Tree Maximum Path Sum ([LeetCode 124](https://leetcode.com/problems/binary-tree-maximum-path-sum/)) — Hard

#### Optimized: Post-Order Maximum Branch Gain
For each node, compute `max(0, gain(left))` and `max(0, gain(right))`. Update `max_path = max(max_path, left + right + node.val)`. Return `node.val + max(left, right)`.
- **Time Complexity**: $O(N)$, **Space Complexity**: $O(H)$.

---

## 3. Hands-On Project & Test Suite

Verify your self-balancing AVL Tree engine:
- Starter Template: [`starter/avl_tree_engine.py`](starter/avl_tree_engine.py)
- Production Solution: [`project_solution/avl_tree_engine.py`](project_solution/avl_tree_engine.py)
- Pytest Suite: [`project_solution/test_avl_tree_engine.py`](project_solution/test_avl_tree_engine.py)

## 🧪 Practice & Verification

Reading a module teaches recognition. Only the problems teach recall — and the
debug lab teaches the thing neither of them does, which is diagnosis.

### 1. Build the module project

```bash
cd starter
python -m pytest ../project_solution -q      # must FAIL before you start
```

Every shipped test must fail with `NotImplementedError` on an untouched
starter. If any passes, the grading loop is broken and is telling you your work
is correct when it has not been done — run `make integrity` from the course
root.

### 2. Work the problem bank — 8 problems

```bash
cd problems
python -m pytest tests -q                    # all of this module's problems
python -m pytest tests -q -k p03             # just problem 3
```

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [Iterative Inorder Traversal](problems/p01_inorder_traversal.py) | Explicit stack traversal | Medium | `Time O(n), Space O(height)` |
| 02 | [Level Order Traversal](problems/p02_level_order.py) | BFS | Medium | `Time O(n), Space O(width)` |
| 03 | [Maximum Depth](problems/p03_max_depth.py) | Tree recursion | Easy | `Time O(n), Space O(height)` |
| 04 | [Validate A Binary Search Tree](problems/p04_is_valid_bst.py) | Range invariant propagation | Medium | `Time O(n), Space O(height)` |
| 05 | [Lowest Common Ancestor In A BST](problems/p05_lca_bst.py) | BST invariant walk | Medium | `Time O(height), Space O(1)` |
| 06 | [K-th Smallest Element In A BST](problems/p06_kth_smallest_bst.py) | Inorder with early exit | Medium | `Time O(height + k), Space O(height)` |
| 07 | [Height-Balanced Binary Tree](problems/p07_is_balanced.py) | Bottom-up recursion | Medium | `Time O(n), Space O(height)` |
| 08 | [Diameter Of A Binary Tree](problems/p08_tree_diameter.py) | Bottom-up recursion with a running best | Hard | `Time O(n), Space O(height)` |

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Every reference solution in `problems/solutions/` is cross-checked against
a brute force or a second implementation, so the answers are verified rather
than asserted.

### 3. Work the debug lab

```bash
cd debug_lab
python broken_tree_validator.py
echo "exit=$?"
```

It exits 0 and prints wrong answers. Read [`SYMPTOMS.md`](debug_lab/SYMPTOMS.md),
write a diagnosis for each, and only then open `ANSWERS.md`. The diagnostic
reasoning is the transferable skill; reading the answer first skips it.

---

## 3. Systems-Level Deep Dive: Cache-Conscious Node Packing vs Pointer Chasing

In real-world database storage engines and high-frequency trading systems, theoretical $O(\log N)$ time is dominated by **CPU memory hierarchy and cache misses**.

### 3.1 Pointer-Chasing Penalty in Binary Search Trees
A standard `TreeNode` occupies heap memory scattered by the allocator. Each node traversal (`node = node.left` or `node.right`) dereferences a 64-bit pointer into a new memory location, incurring a **CPU L1/L2/L3 cache miss (~100–250 CPU cycles)**.

```
Standard BST Pointer Chasing (Scattered across Heap):
[Node A: 0x1040] ----(miss)----> [Node B: 0x8890] ----(miss)----> [Node C: 0x3010]
```

### 3.2 Cache-Conscious B-Tree Node Packing
A Cache-Conscious Tree packs multiple keys and child pointers into contiguous memory aligned to **64-byte CPU cache lines**:

```
64-Byte CPU Cache Line Aligned B-Tree Node:
+-------------------------------------------------------------------------------+
| Header (8B) | Key 0 (8B) | Key 1 (8B) | Key 2 (8B) | Child 0 | Child 1 | ...  |
+-------------------------------------------------------------------------------+
|<----------------------------- 64 Bytes (1 Cache Line) ----------------------->|
```

- **SIMD / Vectorized In-Node Search**: Once the 64-byte node is loaded into the CPU L1 cache, binary search or SIMD comparisons (`_mm256_cmpeq_epi64`) find the child pointer branch in **1-2 clock cycles** with zero additional cache misses!
- **Branch Fanout vs Tree Height**: Fanout $B=16$ reduces tree height from $\log_2 N$ to $\log_{16} N$, cutting DRAM accesses by a factor of 4!

---

## ✅ You have mastered this module when you can…

1. Validate a BST with a propagated (low, high) range, and produce a tree that a parent/child check wrongly accepts.
2. Write an iterative inorder traversal and say why recursion is unsafe past ~1000 depth in Python.
3. Compute height and balance in one bottom-up pass, and explain why the naive version is O(n^2).
4. Separate BFS levels using the queue length snapshot, and say why it must be taken before enqueuing children.

Each of these is something you **do**, not something you know. If you cannot do
one without reference, that is the section to revisit — not the whole module.

---

## 🧭 Navigation

- [Pattern Recognition Guide](../PATTERN_RECOGNITION_GUIDE.md) — how to attack a problem you have never seen
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md)
- [Problem bank](problems/README.md) · [Debug lab](debug_lab/SYMPTOMS.md)