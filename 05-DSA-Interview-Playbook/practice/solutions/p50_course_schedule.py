"""
Problem 50: Course Schedule (Medium - Graphs)
There are a total of `numCourses` courses you have to take, labeled from $0$ to $\text{numCourses} - 1$. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates that you must take course $b$ first if you want to take course $a$. Return `True` if you can finish all courses.
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

from collections import deque

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """Determines if all courses can be finished using topological sort."""
    adj: list[list[int]] = [[] for _ in range(num_courses)]
    in_degrees = [0] * num_courses
    
    for crs, pre in prerequisites:
        adj[pre].append(crs)
        in_degrees[crs] += 1
        
    queue = deque([i for i in range(num_courses) if in_degrees[i] == 0])
    count = 0
    
    while queue:
        node = queue.popleft()
        count += 1
        for nei in adj[node]:
            in_degrees[nei] -= 1
            if in_degrees[nei] == 0:
                queue.append(nei)
                
    return count == num_courses


def run_tests():
    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False # Cycle deadlock
    assert can_finish(1, []) is True
    assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p50_course_schedule!")
