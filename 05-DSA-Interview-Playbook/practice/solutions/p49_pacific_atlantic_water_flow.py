"""
Problem 49: Pacific Atlantic Water Flow (Medium - Graphs)
There is an $m \times n$ rectangular island that borders both the Pacific Ocean (top and left edges) and Atlantic Ocean (bottom and right edges). Water flows from a cell to an adjacent cell with an equal or lower height. Return a list of grid coordinates where water can flow to both oceans.
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

def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    """Finds cells that can reach both oceans via reverse uphill BFS/DFS."""
    if not heights:
        return []
        
    rows, cols = len(heights), len(heights[0])
    pac, atl = set(), set()
    
    def dfs(r: int, c: int, visit: set):
        visit.add((r, c))
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visit:
                if heights[nr][nc] >= heights[r][c]:  # Reverse flow: uphill
                    dfs(nr, nc, visit)
                    
    for c in range(cols):
        dfs(0, c, pac)
        dfs(rows - 1, c, atl)
    for r in range(rows):
        dfs(r, 0, pac)
        dfs(r, cols - 1, atl)
        
    return [list(coord) for coord in (pac & atl)]


def run_tests():
    h = [
      [1,2,2,3,5],
      [3,2,3,4,4],
      [2,4,5,3,1],
      [6,7,1,4,5],
      [5,1,1,2,4]
    ]
    res = pacific_atlantic(h)
    assert sorted(res) == sorted([[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]])
    assert pacific_atlantic([[1]]) == [[0, 0]]
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p49_pacific_atlantic_water_flow!")
