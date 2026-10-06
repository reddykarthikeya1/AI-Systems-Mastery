"""
Problem 33: Lowest Common Ancestor of a BST (Medium - Trees)
Given a Binary Search Tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.
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

def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """Finds LCA in a BST in O(H) time and O(1) space."""
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr
    return root


def run_tests():
    r = TreeNode(6, TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))), TreeNode(8, TreeNode(7), TreeNode(9)))
    assert lowest_common_ancestor(r, TreeNode(2), TreeNode(8)).val == 6
    assert lowest_common_ancestor(r, TreeNode(2), TreeNode(4)).val == 2
    assert lowest_common_ancestor(r, TreeNode(3), TreeNode(5)).val == 4
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p33_lowest_common_ancestor_of_a_bst!")
