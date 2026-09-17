"""Reference Solution — Problem 01: Cost Based Join Order

Topic: 22 Query Optimization CBO Index Tuning
"""

from __future__ import annotations


def cost_based_join_order(table_sizes: dict[str, int], join_selectivities: dict[tuple[str, str], float]) -> tuple[list[str], float]:
    import itertools
    tables = list(table_sizes.keys())
    if not tables:
        return ([], 0.0)
    best_order = None
    min_cost = float('inf')
    
    def get_sel(t1: str, t2: str) -> float:
        return join_selectivities.get((t1, t2), join_selectivities.get((t2, t1), 0.1))

    for perm in itertools.permutations(tables):
        cost = 0.0
        curr_card = float(table_sizes[perm[0]])
        for next_t in perm[1:]:
            curr_card = curr_card * float(table_sizes[next_t]) * get_sel(perm[0], next_t)
            cost += curr_card
        if cost < min_cost:
            min_cost = cost
            best_order = list(perm)
    return (best_order if best_order is not None else tables, min_cost if min_cost != float('inf') else 0.0)
