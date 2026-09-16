"""Module 15: Interactive Systems Data Structures CLI Sandbox."""
from __future__ import annotations


def demo():
    print("\n=== DEMO: LRU Cache Eviction Simulation ===")
    from collections import OrderedDict
    cache = OrderedDict()
    capacity = 2
    for k, v in [("A", 1), ("B", 2), ("A", 1), ("C", 3)]:
        if k in cache:
            cache.move_to_end(k)
        cache[k] = v
        if len(cache) > capacity:
            evicted = cache.popitem(last=False)
            print(f"Evicted LRU item: {evicted}")
    print("Final cache contents:", dict(cache))


if __name__ == "__main__":
    demo()
