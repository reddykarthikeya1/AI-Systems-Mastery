"""
Problem 52: Graph Valid Tree (Medium - Graphs)
Given $n$ nodes labeled from $0$ to $n - 1$ and a list of undirected edges, write a function to check whether these edges make up a valid tree.
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

def valid_tree(n: int, edges: list[list[int]]) -> bool:
    """Checks if graph is a valid tree using Disjoint Set Union."""
    if len(edges) != n - 1:
        return False
        
    parent = list(range(n))
    
    def find(p: int) -> int:
        while p != parent[p]:
            parent[p] = parent[parent[p]]
            p = parent[p]
        return p
        
    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u == root_v:
            return False  # Cycle detected
        parent[root_u] = root_v
        
    return True


def run_tests():
    assert valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
    assert valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False # Cycle between 1, 2, 3
    assert valid_tree(4, [[0, 1], [2, 3]]) is False # Disconnected
    assert valid_tree(1, []) is True
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p52_graph_valid_tree!")
