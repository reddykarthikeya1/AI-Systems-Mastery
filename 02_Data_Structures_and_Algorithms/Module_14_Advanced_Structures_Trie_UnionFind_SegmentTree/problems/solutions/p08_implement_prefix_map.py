"""Reference solution — Problem 08: Prefix-Sum Map: Sum Of Keys With A Prefix

Pattern:    Trie with aggregated values
Complexity: Time O(len(key)) per operation, Space O(total characters)
"""

from __future__ import annotations


def simulate_prefix_map(ops: list[tuple[str, str, int]]) -> list[int]:
    root: dict = {"children": {}, "total": 0}
    stored: dict[str, int] = {}
    out: list[int] = []

    for name, key, value in ops:
        if name == "insert":
            # The DELTA, not the value: re-inserting must correct the totals
            # rather than double-count. Adding `value` again would leave every
            # ancestor permanently inflated, silently.
            delta = value - stored.get(key, 0)
            stored[key] = value
            node = root
            node["total"] += delta
            for ch in key:
                node = node["children"].setdefault(ch, {"children": {}, "total": 0})
                node["total"] += delta
        elif name == "sum":
            node = root
            found = True
            for ch in key:
                node = node["children"].get(ch)
                if node is None:
                    found = False
                    break
            out.append(node["total"] if found else 0)
        else:
            raise ValueError(f"unknown operation: {name!r}")

    return out
