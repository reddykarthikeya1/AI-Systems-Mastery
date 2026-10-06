"""
Problem 71: Meeting Rooms (Easy - Intervals)
Given an array of meeting time intervals where `intervals[i] = [start_i, end_i]`, determine if a person could attend all meetings without overlap.
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

def can_attend_meetings(intervals: list[list[int]]) -> bool:
    """Determines if a person can attend all meetings in O(N log N) time."""
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True


def run_tests():
    assert can_attend_meetings([[0, 30], [5, 10], [15, 20]]) is False
    assert can_attend_meetings([[7, 10], [2, 4]]) is True
    assert can_attend_meetings([]) is True
    assert can_attend_meetings([[1, 5], [5, 10]]) is True # Adjacent meetings permitted
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p71_meeting_rooms!")
