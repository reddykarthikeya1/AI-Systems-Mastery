"""Reference Solution — Problem 01: Dependency Inversion Container

Topic: 05 SOLID Principles Clean Architecture
"""

from __future__ import annotations


def dependency_inversion_container(bindings: dict[str, list[str]]) -> list[str]:
    indegree = {k: 0 for k in bindings}
    graph = {k: [] for k in bindings}
    for svc, deps in bindings.items():
        for d in deps:
            if d not in bindings:
                indegree[d] = 0
                graph[d] = []
            graph[d].append(svc)
            indegree[svc] += 1
    queue = [k for k, v in indegree.items() if v == 0]
    queue.sort()
    order = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in sorted(graph.get(u, [])):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(order) < len(indegree):
        raise ValueError("Circular dependency detected")
    return order
