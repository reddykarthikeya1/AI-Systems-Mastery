"""
Problem 51: Number of Connected Components in an Undirected Graph (Medium - Graphs)
You have a graph of $n$ nodes. You are given an integer $n$ and an array `edges` where `edges[i] = [a, b]` indicates that there is an edge between $a$ and $b$ in the graph. Return the number of connected components in the graph.
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

def count_components(n: int, edges: list[list[int]]) -> int:
    """Counts connected components using Disjoint Set Union (Union-Find)."""
    parent = list(range(n))
    rank = [1] * n
    
    def find(p: int) -> int:
        while p != parent[p]:
            parent[p] = parent[parent[p]]  # Path compression
            p = parent[p]
        return p
        
    def union(p1: int, p2: int) -> int:
        r1, r2 = find(p1), find(p2)
        if r1 == r2:
            return 0
        if rank[r1] < rank[r2]:
            parent[r1] = r2
            rank[r2] += rank[r1]
        else:
            parent[r2] = r1
            rank[r1] += rank[r2]
        return 1
        
    components = n
    for n1, n2 in edges:
        components -= union(n1, n2)
        
    return components


def run_tests():
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
    assert count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
    assert count_components(4, []) == 4
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p51_number_of_connected_components!")
