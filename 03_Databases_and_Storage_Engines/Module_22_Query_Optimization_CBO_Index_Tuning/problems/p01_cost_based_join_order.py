"""Problem 01 — Cost Based Join Order

Topic: 22 Query Optimization CBO Index Tuning
Target: Production-grade implementation

Find optimal join order of tables using cost estimation.

Example:
    >>> sizes = {'orders': 1000, 'users': 100, 'items': 50}
    >>> selectivity = {('orders', 'users'): 0.001, ('orders', 'items'): 0.01}
    >>> cost_based_join_order(sizes, selectivity)
    (['orders', 'users', 'items'], 150.0)

Hints:
    Hint 1: With only a handful of tables, the optimizer doesn't need
        dynamic programming — it's cheap enough to just try every possible
        join order and keep whichever one produces the smallest running
        total of intermediate result sizes.
    Hint 2: Use itertools.permutations over the table names; for each
        candidate order, walk left to right accumulating an intermediate
        cardinality and summing it into a total cost, then keep the
        (order, cost) pair with the lowest total across all permutations.
    Hint 3: Each step's cardinality multiplies the running cardinality by
        the next table's size and the selectivity between the FIRST table
        in the permutation and that next table (not the previously-joined
        table) — and selectivity lookups must fall back to the reversed key
        pair, defaulting to 0.1 when the pair isn't in join_selectivities at
        all.
"""

from __future__ import annotations


def cost_based_join_order(table_sizes: dict[str, int], join_selectivities: dict[tuple[str, str], float]) -> tuple[list[str], float]:
    """Compute optimal left-deep join order for all tables minimizing total intermediate tuples.
    Returns (best_order_list, min_cost).
    """
    raise NotImplementedError("Implement cost_based_join_order")
