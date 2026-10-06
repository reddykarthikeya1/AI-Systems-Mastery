"""
Problem 56: House Robber (Medium - Dynamic Programming)
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected and will automatically contact the police if two adjacent houses were broken into on the same night. Determine the maximum amount of money you can rob tonight without alerting the police.
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

def rob(nums: list[int]) -> int:
    """Finds max non-adjacent house loot in O(N) time, O(1) space."""
    rob1, rob2 = 0, 0
    for num in nums:
        rob1, rob2 = rob2, max(rob1 + num, rob2)
    return rob2


def run_tests():
    assert rob([1, 2, 3, 1]) == 4
    assert rob([2, 7, 9, 3, 1]) == 12
    assert rob([5]) == 5
    assert rob([]) == 0
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p56_house_robber!")
