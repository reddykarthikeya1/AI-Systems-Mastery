"""
Problem 8: Longest Consecutive Sequence (Medium - Arrays & Hashing)
Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. Must run in $O(N)$ time.
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

def longest_consecutive(nums: list[int]) -> int:
    """Finds length of longest consecutive sequence in O(N) time."""
    raise NotImplementedError

