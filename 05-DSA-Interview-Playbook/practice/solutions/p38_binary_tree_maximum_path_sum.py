"""
Problem 38: Binary Tree Maximum Path Sum (Hard - Trees)
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. Return the maximum path sum of any non-empty path.
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

def max_path_sum(root: Optional[TreeNode]) -> int:
    """Computes maximum path sum in O(N) time and O(H) space."""
    max_sum = float("-inf")
    
    def gain(node: Optional[TreeNode]) -> int:
        nonlocal max_sum
        if not node:
            return 0
            
        left_gain = max(gain(node.left), 0)
        right_gain = max(gain(node.right), 0)
        
        current_path_sum = node.val + left_gain + right_gain
        max_sum = max(max_sum, current_path_sum)
        
        return node.val + max(left_gain, right_gain)
        
    gain(root)
    return int(max_sum)


def run_tests():
    root = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert max_path_sum(root) == 42
    assert max_path_sum(TreeNode(-3)) == -3
    assert max_path_sum(TreeNode(1, TreeNode(2), TreeNode(3))) == 6
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p38_binary_tree_maximum_path_sum!")
