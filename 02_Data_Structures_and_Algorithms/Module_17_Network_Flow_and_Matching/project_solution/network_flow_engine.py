"""Maximum flow, minimum cut and bipartite matching.

Max-flow is the algorithm people skip and then meet in a Staff-level screen,
because an unusual number of problems are max-flow problems in disguise:

| The question | The flow formulation |
| :--- | :--- |
| Assign N workers to M jobs, most assignments | bipartite matching |
| Cheapest set of edges to disconnect A from B | minimum cut |
| Can this schedule be satisfied? | feasibility of a flow |
| Choose projects with prerequisites for max profit | project selection / min cut |
| Image segmentation, foreground vs background | min cut |

The whole subject rests on one idea - the **residual graph**. Pushing f units
along an edge leaves capacity - f forward, and creates a *backward* edge of
capacity f. That backward edge is what lets a later augmenting path "undo" an
earlier bad decision, and it is why a greedy algorithm that never reconsiders
gets the wrong answer while these get the right one.

Two algorithms, same idea, different path choice:

- **Edmonds-Karp** - BFS, so always a shortest augmenting path. O(V * E^2).
- **Dinic** - build a level graph by BFS, then saturate it with DFS blocking
  flows. O(V^2 * E) generally, and O(E * sqrt(V)) on unit-capacity graphs,
  which is why it is the one to use for bipartite matching.

And the theorem that makes it all worth knowing: **max-flow equals min-cut**.
The largest amount you can push from s to t is exactly the cheapest set of
edges whose removal disconnects them.
"""

from __future__ import annotations

from collections import deque

INF = float("inf")


class FlowNetwork:
    """A directed graph with capacities, stored as an adjacency list of edges.

    Edges are held in one flat list in pairs: edge `i` and its residual partner
    `i ^ 1`. That XOR trick is why pushing flow forward and crediting the
    backward edge is two lines rather than a lookup.
    """

    def __init__(self, nodes: int) -> None:
        self.nodes = nodes
        self.graph: list[list[int]] = [[] for _ in range(nodes)]
        # Each edge is (destination, remaining capacity, original capacity).
        self.to: list[int] = []
        self.capacity: list[int] = []
        self.original: list[int] = []

    def add_edge(self, source: int, target: int, capacity: int) -> int:
        """Add `source -> target` with the given capacity. Returns the edge id.

        A residual edge of capacity 0 is added in the opposite direction at the
        same time. It is not a real edge - it is the accounting entry that lets
        flow be taken back.
        """
        if capacity < 0:
            raise ValueError("capacities must be non-negative")
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
        """How much is actually flowing along an edge: original - remaining."""
        return self.original[edge_id] - self.capacity[edge_id]

    def reset(self) -> None:
        self.capacity = list(self.original)


# ---------------------------------------------------------------------------
# Edmonds-Karp
# ---------------------------------------------------------------------------


def edmonds_karp(network: FlowNetwork, source: int, sink: int) -> int:
    """Max flow by repeatedly pushing along the shortest augmenting path.

    Choosing the *shortest* path is what bounds the running time. Ford-Fulkerson
    with an arbitrary path choice can take time proportional to the flow value
    itself - and with irrational capacities may not terminate at all.
    """
    if source == sink:
        raise ValueError("source and sink must differ")
    total = 0
    while True:
        parent_edge = [-1] * network.nodes
        parent_edge[source] = -2
        queue = deque([source])
        while queue and parent_edge[sink] == -1:
            node = queue.popleft()
            for edge_id in network.graph[node]:
                nxt = network.to[edge_id]
                if parent_edge[nxt] == -1 and network.capacity[edge_id] > 0:
                    parent_edge[nxt] = edge_id
                    queue.append(nxt)
        if parent_edge[sink] == -1:
            return total                      # no augmenting path: we are done

        # Walk the path backwards to find its bottleneck, then push that much.
        bottleneck = INF
        node = sink
        while node != source:
            edge_id = parent_edge[node]
            bottleneck = min(bottleneck, network.capacity[edge_id])
            node = network.to[edge_id ^ 1]
        node = sink
        while node != source:
            edge_id = parent_edge[node]
            network.capacity[edge_id] -= bottleneck
            network.capacity[edge_id ^ 1] += bottleneck
            node = network.to[edge_id ^ 1]
        total += bottleneck


# ---------------------------------------------------------------------------
# Dinic
# ---------------------------------------------------------------------------


def dinic(network: FlowNetwork, source: int, sink: int) -> int:
    """Max flow via level graphs and blocking flows.

    One BFS labels every node with its distance from the source. The DFS then
    only follows edges that go strictly one level deeper, which makes it
    impossible to wander, and saturates the whole level graph before the next
    BFS. The number of BFS phases is bounded by V, and on unit capacities by
    sqrt(E) - which is the bound that makes bipartite matching fast.
    """
    if source == sink:
        raise ValueError("source and sink must differ")

    def build_levels() -> list[int]:
        level = [-1] * network.nodes
        level[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for edge_id in network.graph[node]:
                nxt = network.to[edge_id]
                if level[nxt] == -1 and network.capacity[edge_id] > 0:
                    level[nxt] = level[node] + 1
                    queue.append(nxt)
        return level

    def push(node: int, limit: int, level: list[int], progress: list[int]) -> int:
        if node == sink:
            return limit
        while progress[node] < len(network.graph[node]):
            edge_id = network.graph[node][progress[node]]
            nxt = network.to[edge_id]
            if network.capacity[edge_id] > 0 and level[nxt] == level[node] + 1:
                pushed = push(nxt, min(limit, network.capacity[edge_id]), level, progress)
                if pushed:
                    network.capacity[edge_id] -= pushed
                    network.capacity[edge_id ^ 1] += pushed
                    return pushed
            # This edge leads nowhere useful in this phase; never retry it.
            progress[node] += 1
        return 0

    total = 0
    while True:
        level = build_levels()
        if level[sink] == -1:
            return total
        progress = [0] * network.nodes
        while True:
            pushed = push(source, INF, level, progress)
            if not pushed:
                break
            total += pushed


# ---------------------------------------------------------------------------
# Min cut
# ---------------------------------------------------------------------------


def min_cut(network: FlowNetwork, source: int, sink: int) -> tuple[int, list[tuple[int, int]]]:
    """Return (cut value, the edges crossing the cut).

    Run max flow, then BFS the *residual* graph from the source. Everything
    reachable is on the source side; everything else is on the sink side. The
    original edges crossing that boundary are the minimum cut, and their total
    capacity equals the max flow - that is the max-flow min-cut theorem, and
    this function is its constructive proof.

    The network is reset first, so this is self-contained and gives the same
    answer whether or not a flow has already been run on it.
    """
    network.reset()
    value = dinic(network, source, sink)

    reachable = [False] * network.nodes
    reachable[source] = True
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for edge_id in network.graph[node]:
            nxt = network.to[edge_id]
            if not reachable[nxt] and network.capacity[edge_id] > 0:
                reachable[nxt] = True
                queue.append(nxt)

    crossing = []
    for edge_id in range(0, len(network.to), 2):     # original edges only
        tail = network.to[edge_id ^ 1]
        head = network.to[edge_id]
        if reachable[tail] and not reachable[head] and network.original[edge_id] > 0:
            crossing.append((tail, head))
    return value, sorted(crossing)


# ---------------------------------------------------------------------------
# Bipartite matching
# ---------------------------------------------------------------------------


def bipartite_matching(left: int, right: int,
                       edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Maximum matching, as a flow problem.

    Add a super-source into every left node and a super-sink out of every right
    node, all with capacity 1. Every unit of flow is one pairing, and the
    capacity-1 constraint is what stops a worker being assigned twice.

    Returns the chosen (left, right) pairs.
    """
    source = left + right
    sink = source + 1
    network = FlowNetwork(sink + 1)

    for node in range(left):
        network.add_edge(source, node, 1)
    for node in range(right):
        network.add_edge(left + node, sink, 1)

    edge_ids = {}
    for a, b in edges:
        if not (0 <= a < left and 0 <= b < right):
            raise ValueError(f"edge ({a}, {b}) is outside the bipartition")
        edge_ids[(a, b)] = network.add_edge(a, left + b, 1)

    dinic(network, source, sink)
    return sorted(pair for pair, edge_id in edge_ids.items()
                  if network.flow_on(edge_id) == 1)


def greedy_matching(left: int, right: int,
                    edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Take each edge if both endpoints are free.

    Deliberately included because it is what people write first, it is often
    right, and when it is wrong it is wrong quietly. A test pins down a case
    where it returns a smaller matching than the maximum.
    """
    used_left: set[int] = set()
    used_right: set[int] = set()
    chosen = []
    for a, b in edges:
        if a not in used_left and b not in used_right:
            used_left.add(a)
            used_right.add(b)
            chosen.append((a, b))
    return sorted(chosen)


# ---------------------------------------------------------------------------
# A worked application: project selection
# ---------------------------------------------------------------------------


def max_profit_projects(profits: dict[str, int],
                        costs: dict[str, int],
                        requires: dict[str, list[str]]) -> tuple[int, list[str]]:
    """Choose a set of projects maximising profit, where each project needs
    certain machines and each machine is bought once.

    The reduction: source -> project with capacity = profit, machine -> sink
    with capacity = cost, project -> machine with infinite capacity. The answer
    is (total profit) - (min cut), and the projects on the source side of the
    cut are the ones to run.

    Infinite capacity on the middle edges is the part that encodes the rule
    "you cannot take the project without buying the machine" - cutting such an
    edge is never worth it, so the cut must instead pay for either the profit
    or the machine.
    """
    project_names = sorted(profits)
    machine_names = sorted(costs)
    index = {name: i for i, name in enumerate(project_names)}
    offset = len(project_names)
    index.update({name: offset + i for i, name in enumerate(machine_names)})

    source = offset + len(machine_names)
    sink = source + 1
    network = FlowNetwork(sink + 1)

    total_profit = 0
    for name in project_names:
        total_profit += profits[name]
        network.add_edge(source, index[name], profits[name])
    for name in machine_names:
        network.add_edge(index[name], sink, costs[name])
    for project, machines in requires.items():
        for machine in machines:
            network.add_edge(index[project], index[machine], 10 ** 9)

    cut_value, _ = min_cut(network, source, sink)

    reachable = [False] * network.nodes
    reachable[source] = True
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for edge_id in network.graph[node]:
            nxt = network.to[edge_id]
            if not reachable[nxt] and network.capacity[edge_id] > 0:
                reachable[nxt] = True
                queue.append(nxt)

    chosen = [name for name in project_names if reachable[index[name]]]
    return total_profit - cut_value, chosen
