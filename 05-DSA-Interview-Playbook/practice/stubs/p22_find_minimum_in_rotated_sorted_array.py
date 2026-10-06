"""
Problem 22: Find Minimum in Rotated Sorted Array (Medium - Binary Search)
Suppose an array of length $n$ sorted in ascending order is rotated between 1 and $n$ times. Given the sorted rotated array `nums` of unique elements, return the minimum element of this array. Must run in $O(\log N)$ time.
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

def find_min(nums: list[int]) -> int:
    """Finds minimum element in rotated sorted array in O(log N) time."""
    raise NotImplementedError

