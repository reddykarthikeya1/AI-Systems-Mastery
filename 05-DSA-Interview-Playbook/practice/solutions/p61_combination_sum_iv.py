"""
Problem 61: Combination Sum IV (Medium - Dynamic Programming)
Given an array of distinct integers `nums` and a target integer `target`, return the number of possible combinations (permutations) that add up to `target`.
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

def combination_sum_4(nums: list[int], target: int) -> int:
    """Finds number of permutations adding up to target in O(target * len(nums))."""
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for i in range(1, target + 1):
        for num in nums:
            if i - num >= 0:
                dp[i] += dp[i - num]
                
    return dp[target]


def run_tests():
    assert combination_sum_4([1, 2, 3], 4) == 7
    assert combination_sum_4([9], 3) == 0
    assert combination_sum_4([1, 2], 3) == 3 # (1,1,1), (1,2), (2,1)
    assert combination_sum_4([4, 2], 0) == 1
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p61_combination_sum_iv!")
