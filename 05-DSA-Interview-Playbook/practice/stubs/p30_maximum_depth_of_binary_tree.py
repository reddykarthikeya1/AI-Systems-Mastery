"""
Problem 30: Maximum Depth of Binary Tree (Easy - Trees)
Given the `root` of a binary tree, return its maximum depth (number of nodes along the longest path from root to farthest leaf).
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

def max_depth(root: Optional[TreeNode]) -> int:
    """Calculates maximum depth of binary tree in O(N) time."""
    raise NotImplementedError

