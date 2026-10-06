"""
Problem 53: Network Delay Time (Medium - Graphs)
You are given a network of $n$ nodes, labeled from $1$ to $n$. You are also given `times`, a list of travel times as directed edges `times[i] = (u, v, w)`. We will send a signal from node $k$. Return the minimum time it takes for all $n$ nodes to receive the signal. If it is impossible, return `-1`.
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

def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """Finds time for signal to reach all nodes using Dijkstra's algorithm."""
    raise NotImplementedError

