"""Problem 01 — Skip List Probabilistic Index

Topic: 21 Vector Database HNSW Index Milvus
Target: Production-grade implementation

Probabilistic layered skip list search returning target value node.

Example:
    >>> layers = [{10: 50}, {10: 30, 30: 50}, {10: 20, 20: 30, 30: 40, 40: 50}]
    >>> skip_list_probabilistic_index(layers, 30)
    30
    >>> skip_list_probabilistic_index(layers, 25) is None
    True

Hints:
    Hint 1: A skip list search only ever moves forward or drops down a
        level, never backward -- each higher layer is a shortcut over the
        one below it, letting you skip large ranges of keys cheaply.
    Hint 2: Start at the head position (the smallest key, shared by every
        layer), then for each layer top to bottom: advance `curr` forward
        within that layer while doing so wouldn't overshoot the target,
        then fall through to the next layer at the SAME `curr` position.
    Hint 3: Carry `curr` forward between layers instead of resetting it to
        each layer's own minimum key -- that's what makes the search
        converge; and if the walk never lands exactly on `target` once
        layer 0 is exhausted (as with target 25, which isn't a key
        anywhere in the structure), the result is None.
"""

from __future__ import annotations


def skip_list_probabilistic_index(layers: list[dict[int, int]], target: int) -> int | None:
    """layers: list of dicts mapping key -> next_key in that layer, from top layer to bottom layer 0.
    Start at top layer, walk forward while next_key <= target. Drop to next layer when blocked.
    Returns target if found at bottom layer, else None.
    """
    raise NotImplementedError("Implement skip_list_probabilistic_index")
