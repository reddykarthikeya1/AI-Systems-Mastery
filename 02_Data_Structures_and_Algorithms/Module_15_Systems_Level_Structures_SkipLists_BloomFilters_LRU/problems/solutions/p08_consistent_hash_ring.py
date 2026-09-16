"""Reference solution — Problem 08: Consistent Hashing Ring

Pattern:    Consistent hashing
Complexity: Time O((n*v) log(n*v) + k log(n*v)), Space O(n*v)
"""

from __future__ import annotations


def remap_fraction(nodes: list[str], new_node: str, keys: list[str], vnodes: int = 150) -> float:
    import bisect
    import hashlib

    if not nodes:
        raise ValueError("at least one node is required")

    def h(text: str) -> int:
        return int.from_bytes(hashlib.md5(text.encode()).digest()[:8], "big")

    def build(members: list[str]) -> tuple[list[int], dict[int, str]]:
        ring: list[int] = []
        owner: dict[int, str] = {}
        for node in members:
            # Several points per node: with one each the load is badly skewed.
            for v in range(vnodes):
                point = h(f"{node}#{v}")
                ring.append(point)
                owner[point] = node
        ring.sort()
        return ring, owner

    def locate(ring: list[int], owner: dict[int, str], key: str) -> str:
        i = bisect.bisect_right(ring, h(key))
        if i == len(ring):
            i = 0               # wrap around the ring
        return owner[ring[i]]

    before_ring, before_owner = build(nodes)
    after_ring, after_owner = build([*nodes, new_node])

    moved = sum(
        1
        for key in keys
        if locate(before_ring, before_owner, key) != locate(after_ring, after_owner, key)
    )
    return moved / len(keys) if keys else 0.0
