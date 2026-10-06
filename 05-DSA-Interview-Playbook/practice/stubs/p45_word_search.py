"""
Problem 45: Word Search (Medium - Backtracking)
Given an $m \times n$ grid of characters `board` and a string `word`, return `True` if `word` exists in the grid. The word can be constructed from sequentially adjacent cells horizontally or vertically. The same cell may not be used more than once.
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

def exist(board: list[list[str]], word: str) -> bool:
    """Checks if word exists on board using DFS backtracking."""
    raise NotImplementedError

