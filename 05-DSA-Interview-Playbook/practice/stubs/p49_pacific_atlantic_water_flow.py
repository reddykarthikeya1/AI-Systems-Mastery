"""
Problem 49: Pacific Atlantic Water Flow (Medium - Graphs)
There is an $m \times n$ rectangular island that borders both the Pacific Ocean (top and left edges) and Atlantic Ocean (bottom and right edges). Water flows from a cell to an adjacent cell with an equal or lower height. Return a list of grid coordinates where water can flow to both oceans.
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

def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    """Finds cells that can reach both oceans via reverse uphill BFS/DFS."""
    raise NotImplementedError

