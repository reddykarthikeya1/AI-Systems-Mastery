"""A logistics planner with three planted defects.

It runs to completion, raises nothing and exits 0. Every number it prints is
plausible. Three of them are wrong.

    python broken_flow_service.py
    echo "exit=$?"
"""
from __future__ import annotations

from collections import deque

INF = float("inf")


class Network:
    def __init__(self, nodes: int) -> None:
        self.nodes = nodes
        self.graph: list[list[int]] = [[] for _ in range(nodes)]
        self.to: list[int] = []
        self.capacity: list[int] = []
        self.original: list[int] = []

    def add_edge(self, source: int, target: int, capacity: int) -> int:
        edge_id = len(self.to)
        self.graph[source].append(edge_id)
        self.to.append(target)
        self.capacity.append(capacity)
        self.original.append(capacity)

        self.graph[target].append(edge_id + 1)
        self.to.append(source)
        self.capacity.append(0)
        self.original.append(0)
        return edge_id

    def flow_on(self, edge_id: int) -> int:
        return self.original[edge_id] - self.capacity[edge_id]

    def reset(self) -> None:
        self.capacity = list(self.original)


def max_flow(network: Network, source: int, sink: int) -> int:
    """Correct Edmonds-Karp. This is the reference for symptom 1."""
    total = 0
    while True:
        parent = [-1] * network.nodes
        parent[source] = -2
        queue = deque([source])
        while queue and parent[sink] == -1:
            node = queue.popleft()
            for edge_id in network.graph[node]:
                nxt = network.to[edge_id]
                if parent[nxt] == -1 and network.capacity[edge_id] > 0:
                    parent[nxt] = edge_id
                    queue.append(nxt)
        if parent[sink] == -1:
            return total
        bottleneck = INF
        node = sink
        while node != source:
            edge_id = parent[node]
            bottleneck = min(bottleneck, network.capacity[edge_id])
            node = network.to[edge_id ^ 1]
        node = sink
        while node != source:
            edge_id = parent[node]
            network.capacity[edge_id] -= bottleneck
            network.capacity[edge_id ^ 1] += bottleneck
            node = network.to[edge_id ^ 1]
        total += bottleneck


def route_shipments(nodes: int, links: list[tuple[int, int, int]],
                    depot: int, port: int) -> int:
    """How many containers per day can move from the depot to the port."""
    network = Network(nodes)
    for a, b, capacity in links:
        network.add_edge(a, b, capacity)
        network.add_edge(b, a, capacity)
    return max_flow(network, depot, port)


def find_bottleneck_links(nodes: int, links: list[tuple[int, int, int]],
                          depot: int, port: int) -> tuple[int, list[tuple[int, int]]]:
    """Which links, if they failed, would cut the depot off from the port."""
    network = Network(nodes)
    for a, b, capacity in links:
        network.add_edge(a, b, capacity)
    value = max_flow(network, depot, port)

    reachable = [False] * network.nodes
    reachable[depot] = True
    queue = deque([depot])
    while queue:
        node = queue.popleft()
        for edge_id in network.graph[node]:
            nxt = network.to[edge_id]
            if not reachable[nxt] and network.original[edge_id] > 0:
                reachable[nxt] = True
                queue.append(nxt)

    crossing = []
    for edge_id in range(0, len(network.to), 2):
        tail = network.to[edge_id ^ 1]
        head = network.to[edge_id]
        if reachable[tail] and not reachable[head] and network.original[edge_id] > 0:
            crossing.append((tail, head))
    return value, sorted(crossing)


def assign_drivers(drivers: int, routes: int,
                   qualified: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Give each driver at most one route and each route at most one driver."""
    source = drivers + routes
    sink = source + 1
    network = Network(sink + 1)

    for driver in range(drivers):
        network.add_edge(source, driver, 2)
    for route in range(routes):
        network.add_edge(drivers + route, sink, 1)

    edge_ids = {}
    for driver, route in qualified:
        edge_ids[(driver, route)] = network.add_edge(driver, drivers + route, 1)

    max_flow(network, source, sink)
    return sorted(pair for pair, edge_id in edge_ids.items()
                  if network.flow_on(edge_id) == 1)


def main() -> None:
    print("=" * 68)
    print("LOGISTICS PLANNER - daily capacity report")
    print("=" * 68)

    print()
    print("[1] Container throughput, depot -> port")
    # Every link is ONE WAY, in the direction written.
    links = [(0, 1, 3), (2, 1, 3), (2, 3, 3), (0, 4, 2), (4, 3, 2)]
    routed = route_shipments(5, links, 0, 3)
    leaving_depot = sum(c for a, _, c in links if a == 0)
    entering_port = sum(c for _, b, c in links if b == 3)
    print(f"    one-way links (from, to, capacity): {links}")
    print(f"    capacity leaving the depot : {leaving_depot}")
    print(f"    capacity entering the port : {entering_port}")
    print(f"    planner says throughput is : {routed}")

    print()
    print("[2] Which links are the bottleneck?")
    value, cut = find_bottleneck_links(5, links, 0, 3)
    print(f"    planner says max throughput is : {value}")
    print(f"    planner says the bottleneck is : {cut}")
    surviving = [(a, b, c) for a, b, c in links if (a, b) not in cut]
    print(f"    capacity of those links     : {sum(c for a, b, c in links if (a, b) in cut)}")
    print(f"    links remaining after cutting them: {len(surviving)} of {len(links)}")

    print()
    print("[3] Driver assignment")
    qualified = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]
    assignment = assign_drivers(3, 2, qualified)
    print(f"    3 drivers, 2 routes, qualifications: {qualified}")
    print(f"    planner assigned: {assignment}")
    per_driver: dict[int, int] = {}
    for driver, _ in assignment:
        per_driver[driver] = per_driver.get(driver, 0) + 1
    print(f"    routes per driver: {dict(sorted(per_driver.items()))}")

    print()
    print("=" * 68)
    print("Report complete. Exit status 0.")
    print("=" * 68)


if __name__ == "__main__":
    main()
