"""
Problem 57: House Robber II (Medium - Dynamic Programming)
You are a professional robber planning to rob houses along a street, but all houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Determine the maximum amount of money you can rob tonight without alerting the police.
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

def rob_circular(nums: list[int]) -> int:
    """Solves circular house robber problem in O(N) time, O(1) space."""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
        
    def rob_linear(houses: list[int]) -> int:
        r1, r2 = 0, 0
        for h in houses:
            r1, r2 = r2, max(r1 + h, r2)
        return r2
        
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


def run_tests():
    assert rob_circular([2, 3, 2]) == 3
    assert rob_circular([1, 2, 3, 1]) == 4
    assert rob_circular([1, 2, 3]) == 3
    assert rob_circular([1]) == 1
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p57_house_robber_ii!")
