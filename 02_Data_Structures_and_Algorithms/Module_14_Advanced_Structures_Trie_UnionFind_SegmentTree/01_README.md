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

### Problem 1: Implement Trie (Prefix Tree) ([LeetCode 208](https://leetcode.com/problems/implement-trie-prefix-tree/)) — Medium

#### Optimized: N-ary Tree with Character Hash Map
```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
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
- **Time Complexity**: $O(L)$ for all operations, where $L$ is word length.
- **Space Complexity**: $O(\\Sigma \\times L \\times N)$ where $\\Sigma$ is alphabet size.

---

### Problem 2: Design Add and Search Words Data Structure ([LeetCode 211](https://leetcode.com/problems/design-add-and-search-words-data-structure/)) — Medium

#### Optimized: Trie with Backtracking Wildcard Search
When encountering `'.'`: iterate over all existing children at current node and recursively search suffix.
- **Time Complexity**: $O(L)$ for exact words, $O(26^L)$ worst-case for all dots.
- **Space Complexity**: $O(L)$ stack depth.

---

### Problem 3: Word Search II ([LeetCode 212](https://leetcode.com/problems/word-search-ii/)) — Hard

#### Brute Force: Word Search I for each Word
Takes $O(W \\times R \\times C \\times 4^L)$ — Severe TLE.

#### Optimized: Prefix Trie + Grid Backtracking Pruning
Insert all target words into a Trie. Walk the grid once; only continue recursive DFS if the current grid path exists as a prefix in the Trie.
- **Time Complexity**: $O(R \\times C \\times 4^L)$ where $L$ is max word length.
- **Space Complexity**: $O(\\sum \\text{length of words})$.

---

### Problem 4: Redundant Connection ([LeetCode 684](https://leetcode.com/problems/redundant-connection/)) — Medium

#### Optimized: Disjoint Set Union (DSU) Cycle Detection
Iterate through edges. For edge $(u, v)$, if `find(u) == find(v)`, adding this edge creates a cycle (it is redundant!). Otherwise, `union(u, v)`.
```python
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    parent = list(range(len(edges) + 1))
    
    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
        
    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u == root_v:
            return [u, v]
        parent[root_u] = root_v
        
    return []
```
- **Time Complexity**: $O(N \\alpha(N)) \\approx O(N)$ near-linear time.
- **Space Complexity**: $O(N)$ parent array.

---

### Problem 5: Number of Provinces ([LeetCode 547](https://leetcode.com/problems/number-of-provinces/)) — Medium

#### Optimized: DSU Component Counting
Initialize $V$ components. For each connected pair `isConnected[i][j] == 1`, perform `union(i, j)`. Each successful union decrements component count by 1.
- **Time Complexity**: $O(N^2 \\alpha(N))$, **Space Complexity**: $O(N)$.

---

### Problem 6: Accounts Merge ([LeetCode 721](https://leetcode.com/problems/accounts-merge/)) — Medium

#### Optimized: Email-to-Index DSU Union
Map each unique email to an ID and union all emails belonging to the same account. Group emails by parent root.
- **Time Complexity**: $O(N \\times K \\log(N \\times K))$, **Space Complexity**: $O(N \\times K)$.

---

## 3. Hands-On Project & Test Suite

Verify your Prefix Trie and Disjoint Set Union engine:
- Starter Template: [`starter/trie_and_union_find_engine.py`](starter/trie_and_union_find_engine.py)
- Production Solution: [`project_solution/trie_and_union_find_engine.py`](project_solution/trie_and_union_find_engine.py)
- Pytest Suite: [`project_solution/test_trie_and_union_find_engine.py`](project_solution/test_trie_and_union_find_engine.py)

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
