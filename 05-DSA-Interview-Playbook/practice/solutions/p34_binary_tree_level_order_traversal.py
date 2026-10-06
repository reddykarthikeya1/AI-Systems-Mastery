"""
Problem 34: Binary Tree Level Order Traversal (Medium - Trees)
Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).
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

from collections import deque

def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    """Performs level-order BFS traversal in O(N) time."""
    if not root:
        return []
        
    res = []
    q = deque([root])
    
    while q:
        level_size = len(q)
        current_level = []
        for _ in range(level_size):
            node = q.popleft()
            current_level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(current_level)
        
    return res


def run_tests():
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert level_order(root) == [[3], [9, 20], [15, 7]]
    assert level_order(TreeNode(1)) == [[1]]
    assert level_order(None) == []
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p34_binary_tree_level_order_traversal!")
