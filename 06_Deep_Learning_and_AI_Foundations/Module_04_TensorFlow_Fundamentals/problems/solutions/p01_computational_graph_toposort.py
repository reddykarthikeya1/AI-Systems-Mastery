"""Reference Solution — Problem 01: Computational Graph Toposort

Topic: 04 TensorFlow Fundamentals
"""

from __future__ import annotations


def computational_graph_toposort(nodes: dict[str, list[str]]) -> list[str]:
    indegree = {k: 0 for k in nodes}
    dependents = {k: [] for k in nodes}
    for n, deps in nodes.items():
        for d in deps:
            if d not in indegree:
                indegree[d] = 0
                dependents[d] = []
            dependents[d].append(n)
            indegree[n] += 1
    queue = sorted([k for k, v in indegree.items() if v == 0])
    order = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in sorted(dependents.get(u, [])):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return order
