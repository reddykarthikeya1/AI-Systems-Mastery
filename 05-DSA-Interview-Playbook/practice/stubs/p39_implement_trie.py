"""
Problem 39: Implement Trie (Prefix Tree) (Medium - Tries)
A trie (pronounced 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. Implement `insert`, `search`, and `starts_with` methods.
"""
from typing import List, Dict, Optional, Tuple, Set

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Trie:
    def __init__(self):
        raise NotImplementedError
    def insert(self, word: str) -> None:
        raise NotImplementedError
    def search(self, word: str) -> bool:
        raise NotImplementedError
    def starts_with(self, prefix: str) -> bool:
        raise NotImplementedError

