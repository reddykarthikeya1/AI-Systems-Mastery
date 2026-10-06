"""
Problem 48: Clone Graph (Medium - Graphs)
Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in the graph contains a value (`int`) and a list (`List[Node]`) of its neighbors.
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

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node: Optional[GraphNode]) -> Optional[GraphNode]:
    """Clones an undirected graph using DFS in O(V + E) time."""
    if not node:
        return None
        
    cloned: dict[GraphNode, GraphNode] = {}
    
    def dfs(curr: GraphNode) -> GraphNode:
        if curr in cloned:
            return cloned[curr]
            
        copy = GraphNode(curr.val)
        cloned[curr] = copy
        for nei in curr.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy
        
    return dfs(node)


def run_tests():
    n1 = GraphNode(1)
    n2 = GraphNode(2)
    n1.neighbors.append(n2)
    n2.neighbors.append(n1)
    
    c1 = clone_graph(n1)
    assert c1 is not n1
    assert c1.val == 1
    assert len(c1.neighbors) == 1
    assert c1.neighbors[0].val == 2
    assert c1.neighbors[0].neighbors[0] is c1
    assert clone_graph(None) is None
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p48_clone_graph!")
