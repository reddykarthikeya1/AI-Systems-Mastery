#!/usr/bin/env python3
"""Index structures. Exits 0, and answers prefix queries wrongly.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import time

RULE = "=" * 68


def simulate_trie(ops):
    root = {"children": {}, "is_word": False}
    out = []

    def walk(prefix):
        node = root
        for ch in prefix:
            child = node["children"].get(ch)
            if child is None:
                return None
            node = child
        return node

    for name, arg in ops:
        if name == "insert":
            node = root
            for ch in arg:
                node = node["children"].setdefault(ch, {"children": {}, "is_word": False})
            node["is_word"] = True
        elif name == "search":
            out.append(walk(arg) is not None)
        elif name == "starts_with":
            out.append(walk(arg) is not None)
    return out


def simulate_union_find(n, ops):
    parent = list(range(n))
    out = []

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for name, a, b in ops:
        if name == "union":
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra
        elif name == "connected":
            out.append(find(a) == find(b))
    return out


def simulate_segment_tree(nums, ops):
    n = len(nums)
    tree = [0] * (2 * n)
    tree[n : 2 * n] = nums
    for i in range(n - 1, 0, -1):
        tree[i] = tree[2 * i] + tree[2 * i + 1]
    out = []
    for name, a, b in ops:
        if name == "update":
            i = a + n
            tree[i] = b
        elif name == "query":
            lo, hi = a + n, b + n + 1
            total = 0
            while lo < hi:
                if lo & 1:
                    total += tree[lo]
                    lo += 1
                if hi & 1:
                    hi -= 1
                    total += tree[hi]
                lo //= 2
                hi //= 2
            out.append(total)
    return out


def main() -> None:
    print(RULE)
    print("INDEX STRUCTURES")
    print(RULE)

    print()
    print("[1] Trie: search vs starts_with")
    ops = [("insert", "apple"), ("search", "apple"), ("search", "app"),
           ("starts_with", "app"), ("insert", "app"), ("search", "app")]
    print(f"      ops = {ops}")
    print(f"          reported {simulate_trie(ops)}")
    print(f"          expected [True, False, True, True]")
    ops2 = [("insert", "hello"), ("search", "hell"), ("search", "he"),
            ("starts_with", "hell")]
    print(f"      ops = {ops2}")
    print(f"          reported {simulate_trie(ops2)}")
    print(f"          expected [False, False, True]")

    print()
    print("[2] Union-find: connectivity (with timing)")
    for size in (4_000, 16_000):
        # union(i+1, i) re-parents the CURRENT ROOT under the new node, so the
        # tree grows one level deeper each time. union(i, i+1) would build a
        # flat star instead and hide the problem entirely.
        ops = [("union", i + 1, i) for i in range(size - 1)]
        # Building the chain is cheap; it is REPEATED LOOKUPS from the deep end
        # that pay for the depth. Query count scales with the chain length.
        ops += [("connected", 0, size - 1) for _ in range(size // 10)]
        started = time.perf_counter()
        result = simulate_union_find(size, ops)
        elapsed = (time.perf_counter() - started) * 1000
        print(f"      chain of {size:<6} + {size // 10:<5} lookups -> "
              f"connected={result[-1]} took {elapsed:9.2f} ms")
    print("      (both the chain AND the lookup count quadrupled - "
          "what did the time do?)")

    print()
    print("[3] Segment tree: range sums with updates")
    cases = [
        ([1, 3, 5], [("query", 0, 2), ("update", 1, 2), ("query", 0, 2)], [9, 8]),
        ([1, 2, 3, 4], [("query", 0, 3), ("update", 0, 10), ("query", 0, 3)], [10, 19]),
        ([5], [("update", 0, 3), ("query", 0, 0)], [3]),
    ]
    for nums, ops, expected in cases:
        print(f"      {nums} {ops}")
        print(f"          reported {simulate_segment_tree(nums, ops)}")
        print(f"          expected {expected}")

    print()
    print(RULE)
    print("Index check complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
