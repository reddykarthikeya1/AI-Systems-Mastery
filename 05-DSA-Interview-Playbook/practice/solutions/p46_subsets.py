"""
Problem 46: Subsets (Medium - Backtracking)
Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.
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

def subsets(nums: list[int]) -> list[list[int]]:
    """Generates power set of nums in O(N * 2^N) time."""
    res: list[list[int]] = []
    subset: list[int] = []
    
    def dfs(i: int):
        if i >= len(nums):
            res.append(list(subset))
            return
            
        # Decision 1: Include nums[i]
        subset.append(nums[i])
        dfs(i + 1)
        
        # Decision 2: Do NOT include nums[i]
        subset.pop()
        dfs(i + 1)
        
    dfs(0)
    return res


def run_tests():
    assert sorted([sorted(s) for s in subsets([1, 2, 3])]) == sorted([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])
    assert subsets([0]) == [[0], []] or subsets([0]) == [[], [0]]
    assert subsets([]) == [[]]
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p46_subsets!")
