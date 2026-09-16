"""Reference solution — Problem 04: Detect A Cycle In A Directed Graph

Pattern:    DFS with three colours
Complexity: Time O(n + E), Space O(n + E)
"""

from __future__ import annotations


def has_cycle_directed(n: int, edges: list[tuple[int, int]]) -> bool:
    WHITE, GREY, BLACK = 0, 1, 2

    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)

    colour = [WHITE] * n

    # Iterative DFS so a 10**5-node chain does not exhaust the call stack.
    for start in range(n):
        if colour[start] != WHITE:
            continue
        stack: list[tuple[int, int]] = [(start, 0)]
        colour[start] = GREY
        while stack:
            u, idx = stack.pop()
            if idx < len(adj[u]):
                stack.append((u, idx + 1))     # resume here next time
                v = adj[u][idx]
                if colour[v] == GREY:
                    return True                # back edge to the current path
                if colour[v] == WHITE:
                    colour[v] = GREY
                    stack.append((v, 0))
                # colour[v] == BLACK is a re-convergence, which is fine.
            else:
                colour[u] = BLACK              # all descendants explored

    return False
