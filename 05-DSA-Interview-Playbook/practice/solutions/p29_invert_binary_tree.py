"""
Problem 29: Invert Binary Tree (Easy - Trees)
Given the `root` of a binary tree, invert the tree (mirror reflection), and return its root.
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

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Inverts binary tree recursively in O(N) time."""
    if not root:
        return None
        
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


def run_tests():
    root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7, TreeNode(6), TreeNode(9)))
    inverted = invert_tree(root)
    assert inverted.val == 4
    assert inverted.left.val == 7
    assert inverted.right.val == 2
    assert inverted.left.left.val == 9
    assert invert_tree(None) is None
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p29_invert_binary_tree!")
