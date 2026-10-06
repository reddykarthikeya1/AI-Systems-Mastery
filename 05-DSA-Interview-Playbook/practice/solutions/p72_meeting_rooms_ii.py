"""
Problem 72: Meeting Rooms II (Medium - Intervals)
Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms required.
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

import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """Finds minimum meeting rooms needed using min-heap in O(N log N) time."""
    if not intervals:
        return 0
        
    intervals.sort(key=lambda x: x[0])
    rooms: list[int] = []  # Min-heap of end times
    
    for meeting in intervals:
        if rooms and rooms[0] <= meeting[0]:
            heapq.heappop(rooms)
        heapq.heappush(rooms, meeting[1])
        
    return len(rooms)


def run_tests():
    assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert min_meeting_rooms([[7, 10], [2, 4]]) == 1
    assert min_meeting_rooms([[1, 5], [2, 6], [3, 7], [4, 8]]) == 4
    assert min_meeting_rooms([]) == 0
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p72_meeting_rooms_ii!")
