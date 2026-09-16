#!/usr/bin/env python3
"""Systems structures. Exits 0, and evicts the wrong entries.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import hashlib
from collections import OrderedDict

RULE = "=" * 68


def simulate_lru(capacity, ops):
    cache = OrderedDict()
    out = []
    for name, key, value in ops:
        if name == "get":
            if key in cache:
                out.append(cache[key])
            else:
                out.append(-1)
        elif name == "put":
            if key in cache:
                cache.move_to_end(key)
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)
    return out


def bloom_check(items, queries, bits=8192, hashes=3):
    bitset = bytearray(bits)

    def positions(item):
        out = []
        for k in range(hashes):
            digest = hashlib.md5(f"{k}:{item}".encode()).digest()
            out.append(int.from_bytes(digest[:8], "big") % bits)
        return out

    for item in items:
        for p in positions(item):
            bitset[p] = 1

    return [any(bitset[p] for p in positions(q)) for q in queries]


def simulate_ring_buffer(capacity, ops):
    buf = [0] * capacity
    head = 0
    count = 0
    out = []
    for name, value in ops:
        if name == "push":
            buf[(head + count) % capacity] = value
            if count < capacity:
                count += 1
        elif name == "pop":
            if count == 0:
                out.append(None)
            else:
                out.append(buf[head])
                head = (head + 1) % capacity
                count -= 1
        elif name == "items":
            out.append([buf[(head + i) % capacity] for i in range(count)])
    return out


def main() -> None:
    print(RULE)
    print("CACHE AND APPROXIMATION LAYER")
    print(RULE)

    print()
    print("[1] LRU cache")
    cases = [
        (2, [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3),
             ("get", 2, 0), ("get", 1, 0)], [1, -1, 1]),
        (2, [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3),
             ("get", 1, 0), ("get", 3, 0)], [1, 1, 3]),
    ]
    for cap, ops, expected in cases:
        print(f"      capacity={cap}")
        print(f"          reported {simulate_lru(cap, ops)}")
        print(f"          expected {expected}")

    print()
    print("[2] Bloom filter membership")
    words = [f"word-{i}" for i in range(800)]
    verdicts = bloom_check(words, words)
    print(f"      inserted {len(words)} items, queried the same {len(words)}")
    print(f"          false negatives: {verdicts.count(False)}  (must be 0)")
    absent = [f"missing-{i}" for i in range(2000)]
    fp = sum(bloom_check(words, absent))
    print(f"      queried 2000 never-inserted items")
    print(f"          reported present: {fp}  ({100 * fp / 2000:.1f}%)")
    print(f"      a filter with {8192} bits and 800 items sets at most "
          f"{800 * 3} bits ({100 * 800 * 3 / 8192:.0f}% of them)")

    print()
    print("[3] Ring buffer with overwrite-oldest")
    cases = [
        (3, [("push", 1), ("push", 2), ("push", 3), ("push", 4), ("items", 0)],
         [[2, 3, 4]]),
        (2, [("push", 1), ("push", 2), ("push", 3), ("pop", 0)], [2]),
        (1, [("push", 1), ("push", 2), ("items", 0)], [[2]]),
    ]
    for cap, ops, expected in cases:
        print(f"      capacity={cap} {ops}")
        print(f"          reported {simulate_ring_buffer(cap, ops)}")
        print(f"          expected {expected}")

    print()
    print(RULE)
    print("Cache layer complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
