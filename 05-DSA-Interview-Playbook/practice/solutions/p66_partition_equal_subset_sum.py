"""
Problem 66: Partition Equal Subset Sum (Medium - Dynamic Programming)
Given an integer array `nums`, return `True` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or `False` otherwise.
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

def can_partition(nums: list[int]) -> bool:
    """Determines if array can be partitioned into two equal subsets."""
    total = sum(nums)
    if total % 2 != 0:
        return False
        
    target = total // 2
    dp = {0}
    
    for num in nums:
        next_dp = set(dp)
        for t in dp:
            if t + num == target:
                return True
            if t + num < target:
                next_dp.add(t + num)
        dp = next_dp
        
    return target in dp


def run_tests():
    assert can_partition([1, 5, 11, 5]) is True
    assert can_partition([1, 2, 3, 5]) is False
    assert can_partition([2, 2]) is True
    assert can_partition([1]) is False
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p66_partition_equal_subset_sum!")
