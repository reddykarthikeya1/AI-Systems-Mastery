"""
Problem 33: Lowest Common Ancestor of a BST (Medium - Trees)
Given a Binary Search Tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.
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

def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """Finds LCA in a BST in O(H) time and O(1) space."""
    raise NotImplementedError

