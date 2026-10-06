"""
Problem 70: Non-overlapping Intervals (Medium - Intervals)
Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.
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

def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """Finds minimum intervals to remove for no overlaps in O(N log N) time."""
    raise NotImplementedError

