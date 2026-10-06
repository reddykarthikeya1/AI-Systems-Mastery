"""
Problem 75: Missing Number (Easy - Bit Manipulation)
Given an array `nums` containing $n$ distinct numbers in the range $[0, n]$, return the only number in the range that is missing from the array.
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

def missing_number(nums: list[int]) -> int:
    """Finds missing number in O(N) time, O(1) space using XOR."""
    res = len(nums)
    for i, num in enumerate(nums):
        res ^= i ^ num
    return res


def run_tests():
    assert missing_number([3, 0, 1]) == 2
    assert missing_number([0, 1]) == 2
    assert missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
    assert missing_number([0]) == 1
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p75_missing_number!")
