"""Module 17: watch augmenting paths being found, one at a time.

    python 03_try_it_yourself.py
"""
from __future__ import annotations

from collections import deque

INF = float("inf")


def max_flow_verbose(nodes: int, edges: list[tuple[int, int, int]],
                     source: int, sink: int, names: dict[int, str]) -> int:
    graph = [[] for _ in range(nodes)]
    to, cap = [], []
    for a, b, c in edges:
        graph[a].append(len(to))
        to.append(b)
        cap.append(c)
        graph[b].append(len(to))
        to.append(a)
        cap.append(0)

    total = 0
    round_number = 0
    while True:
        parent = [-1] * nodes
        parent[source] = -2
        queue = deque([source])
        while queue and parent[sink] == -1:
            node = queue.popleft()
            for edge_id in graph[node]:
                nxt = to[edge_id]
                if parent[nxt] == -1 and cap[edge_id] > 0:
                    parent[nxt] = edge_id
                    queue.append(nxt)
        if parent[sink] == -1:
            print(f"  no augmenting path left. total flow = {total}")
            return total

        round_number += 1
        path, node = [], sink
        bottleneck = INF
        while node != source:
            edge_id = parent[node]
            bottleneck = min(bottleneck, cap[edge_id])
            path.append(node)
            node = to[edge_id ^ 1]
        path.append(source)
        path.reverse()

        node = sink
        while node != source:
            edge_id = parent[node]
            cap[edge_id] -= bottleneck
            cap[edge_id ^ 1] += bottleneck
            node = to[edge_id ^ 1]
        total += bottleneck
        route = " -> ".join(names[n] for n in path)
        print(f"  round {round_number}: {route}  (bottleneck {bottleneck})")


def main() -> None:
    print("=" * 62)
    print("DEMO 1: two independent routes")
    print("=" * 62)
    names = {0: "tap", 1: "a", 2: "b", 3: "drain"}
    flow = max_flow_verbose(
        4, [(0, 1, 3), (1, 3, 2), (0, 2, 2), (2, 3, 3)], 0, 3, names)
    assert flow == 4, "each route is limited by its narrowest pipe"

    print()
    print("=" * 62)
    print("DEMO 2: the graph that must undo a decision")
    print("=" * 62)
    names = {0: "s", 1: "a", 2: "b", 3: "t"}
    flow = max_flow_verbose(
        4, [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)], 0, 3, names)
    print("  (if a round routes through the middle, a later one takes it back)")
    assert flow == 2, "without residual edges this would stop at 1"

    print()
    print("=" * 62)
    print("DEMO 3: greedy assignment loses")
    print("=" * 62)
    qualified = [(0, 0), (0, 1), (1, 0)]
    taken_left, taken_right, greedy = set(), set(), []
    for worker, job in qualified:
        if worker not in taken_left and job not in taken_right:
            taken_left.add(worker)
            taken_right.add(job)
            greedy.append((worker, job))
    print(f"  greedy assignment: {greedy}  ({len(greedy)} job(s) covered)")

    names = {0: "worker0", 1: "worker1", 2: "job0", 3: "job1", 4: "start", 5: "end"}
    edges = [(4, 0, 1), (4, 1, 1), (2, 5, 1), (3, 5, 1),
             (0, 2, 1), (0, 3, 1), (1, 2, 1)]
    best = max_flow_verbose(6, edges, 4, 5, names)
    print(f"  maximum assignment: {best} jobs covered")
    assert len(greedy) == 1 and best == 2

    print()
    print("All demos complete.")


if __name__ == "__main__":
    main()
