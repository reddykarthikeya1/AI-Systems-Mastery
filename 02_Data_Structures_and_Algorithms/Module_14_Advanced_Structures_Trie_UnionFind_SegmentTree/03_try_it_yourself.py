"""Module 14: Interactive Advanced Structures CLI Sandbox."""
from __future__ import annotations


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


def demo():
    print("\n=== DEMO: Trie Autocomplete Prefix Search ===")
    root = TrieNode()
    for word in ["apple", "app", "application", "banana"]:
        curr = root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_end = True
    print("Stored words: ['apple', 'app', 'application', 'banana']")
    prefix = "app"
    curr = root
    found = True
    for ch in prefix:
        if ch not in curr.children:
            found = False
            break
        curr = curr.children[ch]
    print(f"Does prefix '{prefix}' exist in tree?:", found)


if __name__ == "__main__":
    demo()
