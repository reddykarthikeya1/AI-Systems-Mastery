"""
Problem 55: Climbing Stairs (Easy - Dynamic Programming)
You are climbing a staircase. It takes $n$ steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
"""
from typing import List, Dict, Optional, Tuple, Set

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

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
    raise NotImplementedError

