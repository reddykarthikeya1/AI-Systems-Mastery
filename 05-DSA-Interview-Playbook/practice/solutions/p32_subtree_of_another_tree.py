"""
Problem 32: Subtree of Another Tree (Easy - Trees)
Given the roots of two binary trees `root` and `subRoot`, return `True` if there is a subtree of `root` with the same structure and node values of `subRoot` and `False` otherwise.
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

def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    """Checks if sub_root is a subtree of root."""
    def is_same(p, q):
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return is_same(p.left, q.left) and is_same(p.right, q.right)

    if not sub_root:
        return True
    if not root:
        return False
    if is_same(root, sub_root):
        return True
    return is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)


def run_tests():
    root = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2)), TreeNode(5))
    sub = TreeNode(4, TreeNode(1), TreeNode(2))
    assert is_subtree(root, sub) is True
    root_extra = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2, TreeNode(0))), TreeNode(5))
    assert is_subtree(root_extra, sub) is False
    assert is_subtree(None, None) is True
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p32_subtree_of_another_tree!")
