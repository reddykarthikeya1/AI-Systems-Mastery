"""Reference solution — Problem 02: Union-Find With Path Compression

Pattern:    Disjoint set union
Complexity: Time O(α(n)) amortised per op, Space O(n)
"""

from __future__ import annotations


def simulate_union_find(n: int, ops: list[tuple[str, int, int]]) -> list[bool | int]:
    parent = list(range(n))
    size = [1] * n
    groups = n
    out: list[bool | int] = []

    def find(x: int) -> int:
        # Iterative, so a long chain cannot exhaust the call stack.
        root = x
        while parent[root] != root:
            root = parent[root]
        # Path compression: point everything on the path straight at the root.
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for name, a, b in ops:
        if name == "union":
            ra, rb = find(a), find(b)
            if ra != rb:
                # Union by size keeps the trees shallow.
                if size[ra] < size[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                size[ra] += size[rb]
                groups -= 1
        elif name == "connected":
            out.append(find(a) == find(b))
        elif name == "count":
            out.append(groups)
        else:
            raise ValueError(f"unknown operation: {name!r}")

    return out
