"""Module 08: Interactive Graph Traversals CLI Sandbox."""
from __future__ import annotations

from collections import deque


def demo():
    print("\n=== DEMO: BFS Level-by-Level Graph Exploration ===")
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["E", "F"],
        "D": [],
        "E": [],
        "F": []
    }
    visited = {"A"}
    q = deque(["A"])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    print("BFS Order of Discovery:", " -> ".join(order))


if __name__ == "__main__":
    demo()
