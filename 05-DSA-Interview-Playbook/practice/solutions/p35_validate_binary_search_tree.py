"""
Problem 35: Validate Binary Search Tree (Medium - Trees)
Given the `root` of a binary tree, determine if it is a valid binary search tree (BST). A valid BST requires all left subtree values to be strictly less than node value, and all right subtree values strictly greater.
"""
from typing import List, Dict, Optional, Tuple, Set
import heapq
from collections import deque, defaultdict
import bisect

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

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
    def validate(node, low=float("-inf"), high=float("inf")):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        
    return validate(root)


def run_tests():
    valid_t = TreeNode(2, TreeNode(1), TreeNode(3))
    assert is_valid_bst(valid_t) is True
    invalid_t = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
    assert is_valid_bst(invalid_t) is False
    assert is_valid_bst(TreeNode(1, TreeNode(1))) is False # Strict inequality
    assert is_valid_bst(None) is True
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p35_validate_binary_search_tree!")
