"""
Problem 68: Insert Interval (Medium - Intervals)
You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]` sorted in ascending order by `start_i`. You are also given an interval `newInterval`. Insert `newInterval` into `intervals` such that `intervals` is still sorted and non-overlapping (merge overlapping intervals if necessary).
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

def insert_interval(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    """Inserts and merges new_interval into sorted non-overlapping intervals in O(N)."""
    raise NotImplementedError

