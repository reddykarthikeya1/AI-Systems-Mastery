"""
Problem 22: Find Minimum in Rotated Sorted Array (Medium - Binary Search)
Suppose an array of length $n$ sorted in ascending order is rotated between 1 and $n$ times. Given the sorted rotated array `nums` of unique elements, return the minimum element of this array. Must run in $O(\log N)$ time.
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

def find_min(nums: list[int]) -> int:
    """Finds minimum element in rotated sorted array in O(log N) time."""
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
            
    return nums[left]


def run_tests():
    assert find_min([3, 4, 5, 1, 2]) == 1
    assert find_min([4, 5, 6, 7, 0, 1, 2]) == 0
    assert find_min([11, 13, 15, 17]) == 11
    assert find_min([2, 1]) == 1
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p22_find_minimum_in_rotated_sorted_array!")
