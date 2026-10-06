"""
Problem 44: Combination Sum (Medium - Backtracking)
Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. The same number may be chosen unlimited times.
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

def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """Finds all unique combinations that sum to target using backtracking."""
    res: list[list[int]] = []
    
    def backtrack(start: int, comb: list[int], remain: int):
        if remain == 0:
            res.append(list(comb))
            return
        if remain < 0:
            return
            
        for i in range(start, len(candidates)):
            comb.append(candidates[i])
            backtrack(i, comb, remain - candidates[i])
            comb.pop()
            
    backtrack(0, [], target)
    return res


def run_tests():
    assert sorted(combination_sum([2, 3, 6, 7], 7)) == [[2, 2, 3], [7]]
    assert sorted(combination_sum([2, 3, 5], 8)) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert combination_sum([2], 1) == []
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p44_combination_sum!")
