"""Reference solution — Problem 04: Find All Dictionary Words With A Prefix

Pattern:    Trie traversal
Complexity: Time O(total chars + limit * len), Space O(total chars)
"""

from __future__ import annotations


def words_with_prefix(words: list[str], prefix: str, limit: int = 10) -> list[str]:
    root: dict = {"children": {}, "is_word": False}
    for word in words:
        node = root
        for ch in word:
            node = node["children"].setdefault(ch, {"children": {}, "is_word": False})
        node["is_word"] = True

    # Walk to the prefix node.
    node = root
    for ch in prefix:
        node = node["children"].get(ch)
        if node is None:
            return []

    out: list[str] = []

    def collect(cur: dict, built: str) -> None:
        if len(out) >= limit:
            return                  # early exit is what makes this usable
        if cur["is_word"]:
            out.append(built)
        # Sorted keys give lexicographic order with no final sort.
        for ch in sorted(cur["children"]):
            if len(out) >= limit:
                return
            collect(cur["children"][ch], built + ch)

    collect(node, prefix)
    return out
