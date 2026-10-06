"""
Problem 63: Unique Paths (Medium - Dynamic Programming)
There is a robot on an $m \times n$ grid. The robot is initially located at the top-left corner and tries to move to the bottom-right corner. The robot can only move either down or right at any point in time. Return the number of possible unique paths.
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

def unique_paths(m: int, n: int) -> int:
    """Finds unique paths in m x n grid using 2D DP in O(m * n) time."""
    raise NotImplementedError

