"""
Problem 34: Binary Tree Level Order Traversal (Medium - Trees)
Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).
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

def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    """Performs level-order BFS traversal in O(N) time."""
    raise NotImplementedError

