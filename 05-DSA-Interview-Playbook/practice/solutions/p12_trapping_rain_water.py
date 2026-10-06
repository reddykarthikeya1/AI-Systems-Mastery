"""
Problem 12: Trapping Rain Water (Hard - Two Pointers)
Given $n$ non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
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

def trap_rain_water(height: list[int]) -> int:
    """Computes trapped rain water in O(N) time and O(1) space.
    
    Time: O(N), Space: O(1)
    """
    if not height:
        return 0

    left, right = 0, len(height) - 1
    max_left, max_right = 0, 0
    total_water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= max_left:
                max_left = height[left]
            else:
                total_water += max_left - height[left]
            left += 1
        else:
            if height[right] >= max_right:
                max_right = height[right]
            else:
                total_water += max_right - height[right]
            right -= 1

    return total_water


def run_tests():
    assert trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap_rain_water([4, 2, 0, 3, 2, 5]) == 9
    assert trap_rain_water([]) == 0
    assert trap_rain_water([3, 3, 3]) == 0
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p12_trapping_rain_water!")
