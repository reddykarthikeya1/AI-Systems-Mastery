"""
Problem 68: Insert Interval (Medium - Intervals)
You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]` sorted in ascending order by `start_i`. You are also given an interval `newInterval`. Insert `newInterval` into `intervals` such that `intervals` is still sorted and non-overlapping (merge overlapping intervals if necessary).
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

def insert_interval(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    """Inserts and merges new_interval into sorted non-overlapping intervals in O(N)."""
    res: list[list[int]] = []
    i = 0
    n = len(intervals)
    
    # 1. Before new_interval
    while i < n and intervals[i][1] < new_interval[0]:
        res.append(intervals[i])
        i += 1
        
    # 2. Overlapping merges
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    res.append(new_interval)
    
    # 3. After new_interval
    while i < n:
        res.append(intervals[i])
        i += 1
        
    return res


def run_tests():
    assert insert_interval([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
    assert insert_interval([], [5, 7]) == [[5, 7]]
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p68_insert_interval!")
