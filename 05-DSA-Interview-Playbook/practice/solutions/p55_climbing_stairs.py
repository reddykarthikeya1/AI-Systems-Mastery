"""
Problem 55: Climbing Stairs (Easy - Dynamic Programming)
You are climbing a staircase. It takes $n$ steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
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

def climb_stairs(n: int) -> int:
    """Calculates number of ways to climb n stairs in O(N) time, O(1) space."""
    if n <= 2:
        return n
        
    one, two = 1, 2
    for _ in range(3, n + 1):
        one, two = two, one + two
        
    return two


def run_tests():
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
    assert climb_stairs(1) == 1
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p55_climbing_stairs!")
