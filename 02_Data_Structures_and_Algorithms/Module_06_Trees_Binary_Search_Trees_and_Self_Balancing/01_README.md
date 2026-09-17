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

---

## 🗺️ Recommended Step-by-Step Learning Path

Follow this exact sequence to achieve complete mastery of this module:

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[01_README.md](01_README.md)** | Read conceptual overview, architectural foundations, and mental models. |
| **2** | **[02_FOUNDATIONS_PLAYGROUND.md](02_FOUNDATIONS_PLAYGROUND.md)** | Practice beginner spoonfed micro-drills and line-by-line syntax breakdowns. |
| **3** | **[03_try_it_yourself.py](03_try_it_yourself.py)** | Run in terminal (`python 03_try_it_yourself.py`) for an interactive zero-dependency sandbox. |
| **4** | **[00_interactive_trees_binary_search_trees_and_self_balancing.ipynb](00_interactive_trees_binary_search_trees_and_self_balancing.ipynb)** | Open in Jupyter/VS Code to run interactive visual experiments and benchmarks. |
| **5** | **[06_TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)** | Study forensic runbooks, edge cases, and real-world failure post-mortems. |
| **6** | **[05_SELF_ASSESSMENT_AND_CHALLENGES.md](05_SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test your knowledge with self-assessment quizzes, challenges, and diagnostic scenarios. |
| **7** | **[04_PROJECT_GUIDE.md](04_PROJECT_GUIDE.md)** | Follow guided project implementation for `starter/` and `project_solution/`. |
| **8** | **[problems/](problems/)** | Solve hands-on problem bank challenges and verify with `pytest problems/tests`. |
| **9** | **[debug_lab/](debug_lab/)** | Diagnose and fix silent production bugs in the Bug Hunter Drill. |

---

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

This section walks through the **6 canonical LeetCode challenges** curated for this module.
Each problem is analyzed from brute force intuition to the optimal invariant-driven solution, along with the critical edge cases to guard against in production.

### Problem 1: Maximum Depth of Binary Tree ([LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/)) — Easy

> **Pattern**: `Post-Order Recursive DFS` | **Target Time**: $O(N)$ | **Target Space**: $O(H)

#### Problem Specification
Given the `root` of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

#### Algorithmic Invariants & Optimal Derivation
Base case: depth of empty subtree is 0. Inductive step: depth of current node is $1 + \max(	ext{depth}(left), 	ext{depth}(right))$.

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 2: Invert Binary Tree ([LeetCode #226](https://leetcode.com/problems/invert-binary-tree/)) — Easy

> **Pattern**: `Recursive Tree Transformation` | **Target Time**: $O(N)$ | **Target Space**: $O(H)

#### Problem Specification
Given the `root` of a binary tree, invert the tree (mirroring all left and right subtrees), and return its root.

#### Algorithmic Invariants & Optimal Derivation
Recursively invert the left and right subtrees and swap the children pointers on the root.

```python
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 3: Diameter of Binary Tree ([LeetCode #543](https://leetcode.com/problems/diameter-of-binary-tree/)) — Easy

> **Pattern**: `Bottom-Up Subtree Heights` | **Target Time**: $O(N)$ | **Target Space**: $O(H)

#### Problem Specification
Given the `root` of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.

#### Algorithmic Invariants & Optimal Derivation
At any node, the longest path passing through that node is $	ext{height}(	ext{left}) + 	ext{height}(	ext{right})$. Track the global maximum while returning node height bottom-up.

```python
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0
        def height(node):
            nonlocal diameter
            if not node:
                return 0
            lh = height(node.left)
            rh = height(node.right)
            diameter = max(diameter, lh + rh)
            return 1 + max(lh, rh)
        height(root)
        return diameter
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 4: Validate Binary Search Tree ([LeetCode #98](https://leetcode.com/problems/validate-binary-search-tree/)) — Medium

> **Pattern**: `Range Invariant Bounding` | **Target Time**: $O(N)$ | **Target Space**: $O(H)

#### Problem Specification
Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys strictly less than the node's key.
- The right subtree of a node contains only nodes with keys strictly greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

#### Algorithmic Invariants & Optimal Derivation
Pass lower and upper bounds $(low, high)$ into recursive calls. Going left updates the upper bound to current node value; going right updates the lower bound.

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node, low=-float('inf'), high=float('inf')):
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        return validate(root)
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 5: Lowest Common Ancestor of a BST ([LeetCode #235](https://leetcode.com/problems/lowest-common-ancestor-of-a-bst/)) — Medium

> **Pattern**: `BST Value Branching` | **Target Time**: $O(H)$ | **Target Space**: $O(1)

#### Problem Specification
Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given values `p` and `q`.

The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants.

#### Algorithmic Invariants & Optimal Derivation
Take advantage of BST property: if both p and q are smaller than curr.val, LCA must be in left subtree. If both larger, right subtree. The first node where p and q split (or one equals curr.val) is the LCA.

```python
class Solution:
    def lowestCommonAncestor(self, root: Optional[TreeNode], p: int, q: int) -> int:
        curr = root
        while curr:
            if p < curr.val and q < curr.val:
                curr = curr.left
            elif p > curr.val and q > curr.val:
                curr = curr.right
            else:
                return curr.val
        return -1
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 6: Binary Tree Maximum Path Sum ([LeetCode #124](https://leetcode.com/problems/binary-tree-maximum-path-sum/)) — Hard

> **Pattern**: `Bottom-Up Path Gain Propagation` | **Target Time**: $O(N)$ | **Target Space**: $O(H)

#### Problem Specification
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. A node can only appear in the sequence at most once.

Given the `root` of a binary tree, return the maximum path sum of any non-empty path.

#### Algorithmic Invariants & Optimal Derivation
Compute the maximum branch gain contributed by subtrees bottom-up (clamped to 0 if negative). At each node, the combined arch sum is `node.val + left_gain + right_gain`.

```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        max_sum = -float('inf')
        def max_gain(node):
            nonlocal max_sum
            if not node:
                return 0
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)
            curr_path = node.val + left_gain + right_gain
            max_sum = max(max_sum, curr_path)
            return node.val + max(left_gain, right_gain)
        max_gain(root)
        return max_sum
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

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