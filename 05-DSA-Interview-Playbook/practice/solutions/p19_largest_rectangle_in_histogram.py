"""
Problem 19: Largest Rectangle in Histogram (Hard - Stack)
Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
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

def largest_rectangle_area(heights: list[int]) -> int:
    """Computes maximum rectangle area using a monotonic increasing stack.
    
    Time: O(N), Space: O(N)
    """
    stack: list[tuple[int, int]] = []  # (index, height)
    max_area = 0
    
    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))
        
    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))
        
    return max_area


def run_tests():
    assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle_area([2, 4]) == 4
    assert largest_rectangle_area([1]) == 1
    assert largest_rectangle_area([]) == 0
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p19_largest_rectangle_in_histogram!")
