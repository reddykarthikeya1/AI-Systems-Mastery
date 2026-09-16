"""Beginner playground for Module 16 - Neo4j and Graph Databases.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import deque

# ------------------------------------- 1. Relationships as first-class things
friends = {
    "ana": ["bo", "cy"],
    "bo": ["ana", "di"],
    "cy": ["ana", "di", "ed"],
    "di": ["bo", "cy", "fay"],
    "ed": ["cy"],
    "fay": ["di"],
}

print("ana's direct friends:", friends["ana"])
assert friends["ana"] == ["bo", "cy"]


# ---------------------------------------------------- 2. Walking, not joining
def n_hops(start, hops):
    seen = {start}
    frontier = {start}
    visited_nodes = 0
    for _ in range(hops):
        nxt = set()
        for person in frontier:
            visited_nodes += 1
            nxt.update(friends[person])
        frontier = nxt - seen
        seen |= nxt
    return seen - {start}, visited_nodes


reach_2, touched = n_hops("ana", 2)
print("within 2 hops of ana:", sorted(reach_2), f"(visited {touched} nodes)")
assert sorted(reach_2) == ["bo", "cy", "di", "ed"]
assert touched <= len(friends), "never more work than there are people"


# ------------------------------------------ 3. Shortest path in one traversal
def shortest_path(start, goal):
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        if path[-1] == goal:
            return path
        for neighbour in friends[path[-1]]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(path + [neighbour])
    return None


route = shortest_path("ana", "fay")
print("ana -> fay:", " -> ".join(route))
assert route is not None and route[0] == "ana" and route[-1] == "fay"
assert len(route) == 4, "ana, one friend, di, fay"


# --------------------------------- 4. Where the relational version falls over
people = 1_000_000
friends_each = 100
edges = people * friends_each

graph_work = [friends_each ** d for d in (1, 2, 3)]
join_work = [edges * d for d in (1, 2, 3)]

for depth in (1, 2, 3):
    print(f"  depth {depth}: graph walks ~{graph_work[depth - 1]:>9,} "
          f"| join considers ~{join_work[depth - 1]:>12,}")

assert graph_work[2] < join_work[2] / 100, "at depth 3 it is not a close contest"
print("The graph's cost follows the answer. The join's cost follows the database.")


print()
print("All checks passed.")
