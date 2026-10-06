"""
Problem 41: Word Search II (Hard - Tries)
Given an $m \times n$ `board` of characters and a list of strings `words`, return all words on the board. Each word must be constructed from sequentially adjacent cells.
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

def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """Finds all words on board using Trie-guided backtracking DFS."""
    raise NotImplementedError

