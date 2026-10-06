"""
Problem 53: Network Delay Time (Medium - Graphs)
You are given a network of $n$ nodes, labeled from $1$ to $n$. You are also given `times`, a list of travel times as directed edges `times[i] = (u, v, w)`. We will send a signal from node $k$. Return the minimum time it takes for all $n$ nodes to receive the signal. If it is impossible, return `-1`.
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

import heapq
from collections import defaultdict

def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """Finds time for signal to reach all nodes using Dijkstra's algorithm."""
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
        
    min_heap = [(0, k)]
    dist: dict[int, int] = {}
    
    while min_heap:
        d, u = heapq.heappop(min_heap)
        if u in dist:
            continue
        dist[u] = d
        
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(min_heap, (d + w, v))
                
    return max(dist.values()) if len(dist) == n else -1


def run_tests():
    assert network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert network_delay_time([[1, 2, 1]], 2, 1) == 1
    assert network_delay_time([[1, 2, 1]], 2, 2) == -1 # Unreachable node
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p53_network_delay_time!")
