"""Reference solution — Problem 05: Course Schedule

Pattern:    Cycle detection on prerequisites
Complexity: Time O(V + E), Space O(V + E)
"""

from __future__ import annotations


def can_finish_courses(num_courses: int, prerequisites: list[tuple[int, int]]) -> bool:
    from collections import deque

    # (a, b) means b must come first, so the edge points b -> a.
    adj: dict[int, list[int]] = {i: [] for i in range(num_courses)}
    indegree = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indegree[a] += 1

    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    taken = 0
    while queue:
        u = queue.popleft()
        taken += 1
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    return taken == num_courses
