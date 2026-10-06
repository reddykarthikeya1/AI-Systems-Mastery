"""
Problem 71: Meeting Rooms (Easy - Intervals)
Given an array of meeting time intervals where `intervals[i] = [start_i, end_i]`, determine if a person could attend all meetings without overlap.
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

def can_attend_meetings(intervals: list[list[int]]) -> bool:
    """Determines if a person can attend all meetings in O(N log N) time."""
    raise NotImplementedError

