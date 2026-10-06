"""
Problem 21: Search in Rotated Sorted Array (Medium - Binary Search)
There is an integer array `nums` sorted in ascending order (with distinct values), rotated at an unknown pivot index. Given `nums` and a `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.
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

def search_rotated(nums: list[int], target: int) -> int:
    """Searches for target in rotated sorted array in O(log N) time."""
    raise NotImplementedError

