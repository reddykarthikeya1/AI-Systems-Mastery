"""
Problem 30: Maximum Depth of Binary Tree (Easy - Trees)
Given the `root` of a binary tree, return its maximum depth (number of nodes along the longest path from root to farthest leaf).
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

def max_depth(root: Optional[TreeNode]) -> int:
    """Calculates maximum depth of binary tree in O(N) time."""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def run_tests():
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert max_depth(root) == 3
    assert max_depth(TreeNode(1, None, TreeNode(2))) == 2
    assert max_depth(None) == 0
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p30_maximum_depth_of_binary_tree!")
