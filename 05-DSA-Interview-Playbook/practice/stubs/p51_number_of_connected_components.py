"""
Problem 51: Number of Connected Components in an Undirected Graph (Medium - Graphs)
You have a graph of $n$ nodes. You are given an integer $n$ and an array `edges` where `edges[i] = [a, b]` indicates that there is an edge between $a$ and $b$ in the graph. Return the number of connected components in the graph.
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

def count_components(n: int, edges: list[list[int]]) -> int:
    """Counts connected components using Disjoint Set Union (Union-Find)."""
    raise NotImplementedError

