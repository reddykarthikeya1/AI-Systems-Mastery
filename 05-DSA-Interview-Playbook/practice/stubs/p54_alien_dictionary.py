"""
Problem 54: Alien Dictionary (Hard - Graphs)
There is a new alien language that uses the English alphabet. Given a list of words from the alien language dictionary sorted lexicographically by the rules of this new language, derive the order of letters in this language. If the order is invalid, return `""`.
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

def alien_order(words: list[str]) -> str:
    """Derives alien alphabet order using topological sort."""
    raise NotImplementedError

