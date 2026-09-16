"""Reference solution — Problem 01: Trie: Insert, Search, StartsWith

Pattern:    Trie
Complexity: Time O(len(word)) per operation, Space O(total characters)
"""

from __future__ import annotations


def simulate_trie(ops: list[tuple[str, str]]) -> list[bool | None]:
    # A node is (children, is_word). A plain dict of dicts is enough here.
    root: dict = {"children": {}, "is_word": False}
    out: list[bool | None] = []

    def walk(prefix: str) -> dict | None:
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
            # The flag is what separates a stored word from a mere prefix.
            node["is_word"] = True
        elif name == "search":
            node = walk(arg)
            out.append(bool(node is not None and node["is_word"]))
        elif name == "starts_with":
            out.append(walk(arg) is not None)
        else:
            raise ValueError(f"unknown operation: {name!r}")

    return out
