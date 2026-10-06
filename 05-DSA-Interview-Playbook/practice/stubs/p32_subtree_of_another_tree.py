"""
Problem 32: Subtree of Another Tree (Easy - Trees)
Given the roots of two binary trees `root` and `subRoot`, return `True` if there is a subtree of `root` with the same structure and node values of `subRoot` and `False` otherwise.
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

def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    """Checks if sub_root is a subtree of root."""
    raise NotImplementedError

