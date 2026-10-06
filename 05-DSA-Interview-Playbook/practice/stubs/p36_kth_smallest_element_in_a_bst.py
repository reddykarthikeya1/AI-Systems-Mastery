"""
Problem 36: Kth Smallest Element in a BST (Medium - Trees)
Given the `root` of a binary search tree, and an integer `k`, return the $k^{\text{th}}$ smallest value (1-indexed) of all the values of the nodes in the tree.
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

def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """Finds kth smallest element in BST using in-order traversal."""
    raise NotImplementedError

