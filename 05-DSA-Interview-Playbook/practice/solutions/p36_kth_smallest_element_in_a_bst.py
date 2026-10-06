"""
Problem 36: Kth Smallest Element in a BST (Medium - Trees)
Given the `root` of a binary search tree, and an integer `k`, return the $k^{\text{th}}$ smallest value (1-indexed) of all the values of the nodes in the tree.
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

def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """Finds kth smallest element in BST using in-order traversal."""
    stack = []
    curr = root
    
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
        
    return -1


def run_tests():
    t1 = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
    assert kth_smallest(t1, 1) == 1
    t2 = TreeNode(5, TreeNode(3, TreeNode(2, TreeNode(1)), TreeNode(4)), TreeNode(6))
    assert kth_smallest(t2, 3) == 3
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p36_kth_smallest_element_in_a_bst!")
