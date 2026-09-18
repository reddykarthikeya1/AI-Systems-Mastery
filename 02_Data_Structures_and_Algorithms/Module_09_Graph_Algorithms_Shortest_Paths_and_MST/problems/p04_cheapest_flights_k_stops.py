"""Problem 04 — Cheapest Flight With At Most K Stops

Pattern:    Bellman-Ford by rounds
Difficulty: Hard
Target:     Time O(k*E), Space O(V)

Return the cheapest price from ``src`` to ``dst`` using at most ``k`` stops
(so at most ``k + 1`` flights), or ``-1`` if no such route exists.

Constraints
- ``1 <= n <= 100``
- ``0 <= k < n``
- prices are non-negative

Example
    cheapest_flights(4, [(0,1,100),(1,2,100),(2,0,100),(1,3,600),(2,3,200)], 0, 3, 1) -> 700
    same graph with k = 2 -> 400

Example:
    >>> flights = [(0, 1, 100), (1, 2, 100), (2, 0, 100), (1, 3, 600), (2, 3, 200)]
    >>> cheapest_flights(4, flights, 0, 3, 1)
    700
    >>> cheapest_flights(4, flights, 0, 3, 2)
    400

Hints — read one at a time, and try again between each.

    Hint 1: Dijkstra is the wrong tool here even though all weights are non-negative. Its greedy invariant - once finalised, always optimal - does not hold when there is a hop limit, because a more expensive route with fewer hops can be the only feasible one.
    Hint 2: Bellman-Ford relaxes in rounds, and round r settles the best price using at most r edges. That is exactly the structure you need.
    Hint 3: Run k+1 rounds. Crucially, each round must read from the PREVIOUS round's distances - relax into a fresh copy, or a single round can chain several flights and exceed the hop limit.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def cheapest_flights(n: int, flights: list[tuple[int, int, int]], src: int, dst: int, k: int) -> int:
    raise NotImplementedError("implement cheapest_flights")
