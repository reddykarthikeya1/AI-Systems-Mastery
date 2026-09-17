# Module 14: Advanced Structures: Trie, Union-Find & Segment Tree (0 to 100 Mastery)

> **Prefix Routing, Near-Constant Disjoint Set Amortization, and Range Segment Trees**

Advanced data structures handle massive datasets where basic arrays and hash maps fail asymptotic requirements. In this module, you master **Prefix Tries**, **Disjoint Set Union (DSU) with Path Compression & Union-by-Rank (Ackermann function inverse $\\alpha(N) \\le 4$)**, and **Range Query Segment Trees**.

---

## 1. DSU Invariant: Path Compression & Union by Rank

With both optimizations applied:
- **Union by Rank**: Always attaches the smaller depth tree under the root of the larger depth tree.
- **Path Compression**: During `find(x)`, flattens the pointer path directly to the root.
- **Amortized Time Complexity per Operation**: $O(\\alpha(N))$, where $\\alpha$ is the Inverse Ackermann Function ($< 5$ for any universe size $N \le 10^{80}$).

---

## 2. Curated LeetCode Problem Breakdowns (Brute Force vs. Optimized)

This section walks through the **6 canonical LeetCode challenges** curated for this module.
Each problem is analyzed from brute force intuition to the optimal invariant-driven solution, along with the critical edge cases to guard against in production.

### Problem 1: Implement Trie (Prefix Tree) ([LeetCode #208](https://leetcode.com/problems/implement-trie-prefix-tree/)) — Medium

> **Pattern**: `Prefix Tree / Multi-Way Branching` | **Target Time**: $O(L) per operation$ | **Target Space**: $O(N \cdot L)

#### Problem Specification
A trie (pronounced as 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings.
Implement the `Trie` class:
- `Trie()` Initializes the trie object.
- `void insert(String word)` Inserts the string `word` into the trie.
- `boolean search(String word)` Returns `true` if the string `word` is in the trie, and `false` otherwise.
- `boolean startsWith(String prefix)` Returns `true` if there is a previously inserted string that has the prefix `prefix`.

#### Algorithmic Invariants & Optimal Derivation
Each node maintains a children dictionary and an `is_end` boolean. Traversal follows string characters step by step in $O(L)$ where $L$ is string length.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self.root
        for c in word:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return curr.is_end

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return True
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 2: Design Add and Search Words Data Structure ([LeetCode #211](https://leetcode.com/problems/design-add-and-search-words-data-structure/)) — Medium

> **Pattern**: `Trie with Wildcard DFS Search` | **Target Time**: $O(L) insert, O(26^L) worst search$ | **Target Space**: $O(N \cdot L)

#### Problem Specification
Design a data structure that supports adding new words and finding if a string matches any previously added string with '.' representing any single letter.

#### Algorithmic Invariants & Optimal Derivation
Store words in a trie dictionary. For '.', branch DFS across all child nodes in the current layer.

```python
class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr:
                curr[c] = {}
            curr = curr[c]
        curr['#'] = True

    def search(self, word: str) -> bool:
        def dfs(idx, node):
            curr = node
            for i in range(idx, len(word)):
                c = word[i]
                if c == '.':
                    for child in curr.values():
                        if isinstance(child, dict) and dfs(i + 1, child):
                            return True
                    return False
                else:
                    if c not in curr:
                        return False
                    curr = curr[c]
            return '#' in curr
        return dfs(0, self.root)
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 3: Number of Provinces ([LeetCode #547](https://leetcode.com/problems/number-of-provinces/)) — Medium

> **Pattern**: `Union-Find / Disjoint Set Union (DSU)` | **Target Time**: $O(N^2 \cdot lpha(N))$ | **Target Space**: $O(N)

#### Problem Specification
There are `n` cities. Some of them are connected, while some are not. If city `a` is connected directly with city `b`, and city `b` is connected directly with city `c`, then city `a` is connected indirectly with city `c`.
A province is a group of directly or indirectly connected cities.
Given an `n x n` matrix `isConnected` where `isConnected[i][j] = 1` if the `i-th` city and the `j-th` city are directly connected, return the total number of provinces.

#### Algorithmic Invariants & Optimal Derivation
Initialize n disjoint components. For every connection `isConnected[i][j] == 1`, union the two components and decrement total component count.

```python
class Solution:
    def findCircleNum(self, isConnected: list[list[int]]) -> int:
        n = len(isConnected)
        parent = list(range(n))
        rank = [1] * n
        components = n

        def find(p):
            while p != parent[p]:
                parent[p] = parent[parent[p]]
                p = parent[p]
            return p

        def union(p1, p2):
            nonlocal components
            r1, r2 = find(p1), find(p2)
            if r1 == r2:
                return
            if rank[r1] > rank[r2]:
                parent[r2] = r1
            elif rank[r2] > rank[r1]:
                parent[r1] = r2
            else:
                parent[r2] = r1
                rank[r1] += 1
            components -= 1

        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j] == 1:
                    union(i, j)
        return components
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 4: Redundant Connection ([LeetCode #684](https://leetcode.com/problems/redundant-connection/)) — Medium

> **Pattern**: `Union-Find Cycle Detection` | **Target Time**: $O(N \cdot lpha(N))$ | **Target Space**: $O(N)

#### Problem Specification
In this problem, a tree is an undirected graph that is connected and has no cycles.
You are given a graph that started as a tree with `n` nodes labeled from 1 to `n`, with one additional edge added. The added edge has two different vertices chosen from 1 to `n`, and was not an edge that already existed.
Return an edge that can be removed so that the resulting graph is a tree of `n` nodes.

#### Algorithmic Invariants & Optimal Derivation
For each edge $(u, v)$, find their roots. If `find(u) == find(v)`, adding $(u, v)$ completes a cycle, meaning this is the redundant edge.

```python
class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        n = len(edges)
        parent = list(range(n + 1))

        def find(p):
            while p != parent[p]:
                parent[p] = parent[parent[p]]
                p = parent[p]
            return p

        for u, v in edges:
            ru, rv = find(u), find(v)
            if ru == rv:
                return [u, v]
            parent[ru] = rv
        return []
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 5: Word Search II ([LeetCode #212](https://leetcode.com/problems/word-search-ii/)) — Hard

> **Pattern**: `Trie + Grid Backtracking Pruning` | **Target Time**: $O(M 	imes N 	imes 4^L)$ | **Target Space**: $O(\sum L)

#### Problem Specification
Given an `m x n` `board` of characters and a list of strings `words`, return all words on the board.
Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring.

#### Algorithmic Invariants & Optimal Derivation
Store all target words in a Trie. Traverse the grid with DFS, advancing along corresponding Trie branches and immediately pruning branches when characters deviate.

```python
class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        # Build Trie
        trie = {}
        for w in words:
            curr = trie
            for c in w:
                if c not in curr:
                    curr[c] = {}
                curr = curr[c]
            curr['#'] = w

        rows, cols = len(board), len(board[0])
        res = []

        def dfs(r, c, parent_node):
            ch = board[r][c]
            curr_node = parent_node[ch]

            if '#' in curr_node:
                res.append(curr_node['#'])
                del curr_node['#']  # avoid duplicates

            board[r][c] = '$'
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in curr_node:
                    dfs(nr, nc, curr_node)
            board[r][c] = ch

        for r in range(rows):
            for c in range(cols):
                if board[r][c] in trie:
                    dfs(r, c, trie)
        return res
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---

### Problem 6: Range Sum Query - Mutable ([LeetCode #307](https://leetcode.com/problems/range-sum-query-mutable/)) — Medium

> **Pattern**: `Binary Indexed Tree (BIT) / Segment Tree` | **Target Time**: $O(\log N) update and query$ | **Target Space**: $O(N)

#### Problem Specification
Given an integer array `nums`, handle two types of queries:
1. Update the value of an element in `nums`.
2. Calculate the sum of the elements of `nums` between indices `left` and `right` inclusive.
Both operations must run in $O(\log n)$ time.

#### Algorithmic Invariants & Optimal Derivation
A Fenwick tree (Binary Indexed Tree) supports point updates and prefix sum queries in $O(\log N)$ using bit manipulation `idx & (-idx)`.

```python
class NumArray:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.nums = nums[:]
        self.bit = [0] * (self.n + 1)
        for i, val in enumerate(nums):
            self._add(i + 1, val)

    def _add(self, idx, delta):
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & (-idx)

    def _prefix_sum(self, idx):
        total = 0
        while idx > 0:
            total += self.bit[idx]
            idx -= idx & (-idx)
        return total

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self._add(index + 1, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix_sum(right + 1) - self._prefix_sum(left)
```

#### Critical Production Edge Cases to Guard:
- **Boundary Limits**: Empty inputs, single-element collections, and minimum constraint sizes.
- **Extremes & Negative Values**: Negative indices, zero values, and maximum integer magnitude constraints.
- **Duplicates & Uniform Sequences**: All identical values, alternating keys, or repeated entries.
- **Structural Invariants**: Target at boundary indices (index `0` or `N-1`), missing targets, or cycles.

---


## 3. Hands-On Project & Test Suite

Verify your Prefix Trie and Disjoint Set Union engine:
- Starter Template: [`starter/trie_and_union_find_engine.py`](starter/trie_and_union_find_engine.py)
- Production Solution: [`project_solution/trie_and_union_find_engine.py`](project_solution/trie_and_union_find_engine.py)
- Pytest Suite: [`project_solution/test_trie_and_union_find_engine.py`](project_solution/test_trie_and_union_find_engine.py)

## 🧪 Practice & Verification

<!-- GENERATED_ALGORITHM_DIAGRAM: FENWICK_TREE START -->

```mermaid
graph TD
  %% Fenwick Tree Interval Coverage & Lowbit Jumps
  %% Generated from verified algorithm execution
  classDef default fill:#18181b,stroke:#3f3f46,stroke-width:1px,color:#f4f4f5;
  classDef queryPath fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#ffffff;
  classDef updatePath fill:#7c3aed,stroke:#a78bfa,stroke-width:2px,color:#ffffff;
  classDef node8 fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
  N1["Index 1 (0001)<br/>Covers: [1..1]<br/>Tree Val: 3"]
  N2["Index 2 (0010)<br/>Covers: [1..2]<br/>Tree Val: 5"]
  N3["Index 3 (0011)<br/>Covers: [3..3]<br/>Tree Val: -1"]
  N4["Index 4 (0100)<br/>Covers: [1..4]<br/>Tree Val: 10"]
  N5["Index 5 (0101)<br/>Covers: [5..5]<br/>Tree Val: 5"]
  N6["Index 6 (0110)<br/>Covers: [5..6]<br/>Tree Val: 9"]
  N7["Index 7 (0111)<br/>Covers: [7..7]<br/>Tree Val: -3"]
  N8["Index 8 (1000)<br/>Covers: [1..8]<br/>Tree Val: 19"]

  %% Structural Coverage Hierarchy
  N8 --> N4
  N8 --> N6
  N8 --> N7
  N4 --> N2
  N4 --> N3
  N2 --> N1
  N6 --> N5

  %% Query(7) Jump Path: 7 -> (7-1=6) -> (6-2=4) -> 0
  N7 -.->|'-lowbit(7)'| N6
  N6 -.->|'-lowbit(6)'| N4
```

<!-- GENERATED_ALGORITHM_DIAGRAM: FENWICK_TREE END -->

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
| 01 | [Trie: Insert, Search, StartsWith](problems/p01_trie_operations.py) | Trie | Medium | `Time O(len(word)) per operation, Space O(total characters)` |
| 02 | [Union-Find With Path Compression](problems/p02_union_find.py) | Disjoint set union | Medium | `Time O(α(n)) amortised per op, Space O(n)` |
| 03 | [Segment Tree: Range Sum With Updates](problems/p03_segment_tree.py) | Segment tree | Hard | `Time O(log n) per operation, Space O(n)` |
| 04 | [Find All Dictionary Words With A Prefix](problems/p04_word_search_trie.py) | Trie traversal | Medium | `Time O(total chars + limit * len), Space O(total chars)` |
| 05 | [Accounts Merge](problems/p05_accounts_merge.py) | Union-find over strings | Hard | `Time O(E log E) for the sort, Space O(E)` |
| 06 | [Sparse Table: Range Minimum, No Updates](problems/p06_range_min_query.py) | Sparse table | Hard | `Time O(n log n) preprocessing, O(1) per query` |
| 07 | [Count Of Smaller Numbers After Self](problems/p07_count_smaller_after.py) | Fenwick tree (BIT) | Hard | `Time O(n log n), Space O(n)` |
| 08 | [Prefix-Sum Map: Sum Of Keys With A Prefix](problems/p08_implement_prefix_map.py) | Trie with aggregated values | Medium | `Time O(len(key)) per operation, Space O(total characters)` |

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Every reference solution in `problems/solutions/` is cross-checked against
a brute force or a second implementation, so the answers are verified rather
than asserted.

### 3. Work the debug lab

```bash
cd debug_lab
python broken_index_structures.py
echo "exit=$?"
```

It exits 0 and prints wrong answers. Read [`SYMPTOMS.md`](debug_lab/SYMPTOMS.md),
write a diagnosis for each, and only then open `ANSWERS.md`. The diagnostic
reasoning is the transferable skill; reading the answer first skips it.

---

## ✅ You have mastered this module when you can…

1. Say what a trie answers that a hash map cannot, and what union-find cannot do at all.
2. Implement union-find with path compression and union by size, and state the cost of omitting either.
3. Choose between prefix sums, a Fenwick tree and a segment tree from the read/write mix.
4. Explain why a sparse table works for range minimum but not for range sum.

Each of these is something you **do**, not something you know. If you cannot do
one without reference, that is the section to revisit — not the whole module.

---

## 🧭 Navigation

- [Pattern Recognition Guide](../PATTERN_RECOGNITION_GUIDE.md) — how to attack a problem you have never seen
- [Course README](../README.md) · [Master Syllabus](../MASTER_SYLLABUS.md)
- [Problem bank](problems/README.md) · [Debug lab](debug_lab/SYMPTOMS.md)
