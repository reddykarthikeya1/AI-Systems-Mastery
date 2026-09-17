# 🐣 Interactive Foundations Playground: Advanced Structures: Trie & Union-Find

> *"A Trie is a spelling tree: each letter branches down to words that share the same prefix."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from collections import defaultdict
```

---

## 1. Prefix Trie Construction and Search

A Trie stores strings by character edges in nested dictionaries, enabling $O(L)$ insertion and prefix search where $L$ is word length.

```python
class Trie:
    def __init__(self):
        self.root = {}
    def insert(self, word: str):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node['#'] = True
    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True

trie = Trie()
trie.insert("apple")
trie.insert("app")
assert trie.starts_with("app") is True
assert trie.starts_with("appl") is True
assert trie.starts_with("ban") is False
print("Trie prefix search verified.")
```

---

## 2. Union-Find with Path Compression & Rank

Path compression flattens the tree during find operations, achieving near-constant $O(\alpha(N))$ time per query.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True

dsu = DSU(5)
assert dsu.union(0, 1) is True
assert dsu.union(1, 2) is True
assert dsu.union(0, 2) is False, "0 and 2 already in the same set"
assert dsu.find(0) == dsu.find(2)
print("DSU rank union and path compression confirmed.")
```

---

## 3. Segment Tree Range Sum Query

A segment tree maintains interval sums in a binary tree representation, supporting $O(\log N)$ point updates and range sum queries.

```python
nums = [1, 3, 5, 7, 9, 11]
n = len(nums)
tree = [0] * (2 * n)
# Build
for i in range(n):
    tree[n + i] = nums[i]
for i in range(n - 1, 0, -1):
    tree[i] = tree[2 * i] + tree[2 * i + 1]

def range_sum(l, r):
    res = 0
    l += n
    r += n
    while l < r:
        if l & 1:
            res += tree[l]
            l += 1
        if r & 1:
            r -= 1
            res += tree[r]
        l //= 2
        r //= 2
    return res

assert range_sum(1, 4) == 15, "nums[1..3] = 3 + 5 + 7 = 15"
assert range_sum(0, 6) == 36, "Sum of all 6 elements"
print(f"Segment tree range sum [1, 4): {range_sum(1, 4)}")
```

---
