"""
Problem 72: Meeting Rooms II (Medium - Intervals)
Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms required.
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

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """Finds minimum meeting rooms needed using min-heap in O(N log N) time."""
    raise NotImplementedError

