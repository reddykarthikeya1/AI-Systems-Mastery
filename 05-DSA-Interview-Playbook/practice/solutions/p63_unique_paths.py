"""
Problem 63: Unique Paths (Medium - Dynamic Programming)
There is a robot on an $m \times n$ grid. The robot is initially located at the top-left corner and tries to move to the bottom-right corner. The robot can only move either down or right at any point in time. Return the number of possible unique paths.
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

def unique_paths(m: int, n: int) -> int:
    """Finds unique paths in m x n grid using 2D DP in O(m * n) time."""
    row = [1] * n
    
    for _ in range(m - 1):
        new_row = [1] * n
        for c in range(1, n):
            new_row[c] = new_row[c - 1] + row[c]
        row = new_row
        
    return row[-1]


def run_tests():
    assert unique_paths(3, 7) == 28
    assert unique_paths(3, 2) == 3
    assert unique_paths(1, 1) == 1
    assert unique_paths(3, 3) == 6
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p63_unique_paths!")
