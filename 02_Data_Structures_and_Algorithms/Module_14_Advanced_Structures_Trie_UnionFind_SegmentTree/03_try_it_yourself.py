"""Beginner playground for Module 14 - Advanced Structures: Trie & Union-Find.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import defaultdict

# -------------------------------------------- 1. Prefix Trie Construction and Search
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

# -------------------------------------------- 2. Union-Find with Path Compression & Rank
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

# -------------------------------------------- 3. Segment Tree Range Sum Query
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

print()
print("All checks passed.")
