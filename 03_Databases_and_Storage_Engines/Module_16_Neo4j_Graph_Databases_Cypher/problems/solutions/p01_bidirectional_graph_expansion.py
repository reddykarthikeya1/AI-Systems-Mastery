"""Reference Solution — Problem 01: Bidirectional Graph Expansion

Topic: 16 Neo4j Graph Databases Cypher
"""

from __future__ import annotations


def bidirectional_graph_expansion(adj: dict[str, list[str]], start: str, target: str, max_depth: int = 5) -> int:
    if start == target:
        return 0
    front_q = {start: 0}
    back_q = {target: 0}
    f_frontier = {start}
    b_frontier = {target}
    depth = 0
    while f_frontier and b_frontier and depth <= max_depth:
        # Expand smaller frontier
        if len(f_frontier) <= len(b_frontier):
            next_f = set()
            for u in f_frontier:
                d = front_q[u]
                for v in adj.get(u, []):
                    if v in back_q:
                        total = d + 1 + back_q[v]
                        return total if total <= max_depth else -1
                    if v not in front_q:
                        front_q[v] = d + 1
                        next_f.add(v)
            f_frontier = next_f
        else:
            next_b = set()
            for u in b_frontier:
                d = back_q[u]
                for v in adj.get(u, []):
                    if v in front_q:
                        total = d + 1 + front_q[v]
                        return total if total <= max_depth else -1
                    if v not in back_q:
                        back_q[v] = d + 1
                        next_b.add(v)
            b_frontier = next_b
        depth += 1
    return -1
