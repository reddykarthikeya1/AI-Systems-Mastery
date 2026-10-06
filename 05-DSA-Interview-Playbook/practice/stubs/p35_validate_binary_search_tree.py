"""
Problem 35: Validate Binary Search Tree (Medium - Trees)
Given the `root` of a binary tree, determine if it is a valid binary search tree (BST). A valid BST requires all left subtree values to be strictly less than node value, and all right subtree values strictly greater.
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

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Validates BST in O(N) time by propagating valid range bounds."""
    raise NotImplementedError

