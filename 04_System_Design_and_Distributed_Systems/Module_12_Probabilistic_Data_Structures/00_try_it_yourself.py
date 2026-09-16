"""Beginner playground for Module 12 - Probabilistic Data Structures.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib

# ------------------------------------ 1. Exact membership costs what it costs
items = [f"https://example.com/page/{i}" for i in range(100_000)]
exact = set(items)
exact_bytes = sum(len(s) for s in items)
print(f"exact set: roughly {exact_bytes / 1e6:.1f} MB of strings")
assert len(exact) == 100_000


# ------------------------------- 2. A Bloom filter is a row of light switches
class BloomFilter:
    def __init__(self, bits, hashes):
        self.bits = bytearray(bits)
        self.size = bits
        self.hashes = hashes

    def _positions(self, item):
        digest = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(digest[i * 4:i * 4 + 4], "big") % self.size
                for i in range(self.hashes)]

    def add(self, item):
        for position in self._positions(item):
            self.bits[position] = 1

    def __contains__(self, item):
        return all(self.bits[p] for p in self._positions(item))


bloom = BloomFilter(bits=1_000_000, hashes=7)
for item in items:
    bloom.add(item)

packed_bytes = bloom.size / 8      # a real filter packs 8 flags per byte
print(f"bloom filter: {packed_bytes / 1e6:.3f} MB once packed as real bits")
print(f"exact set:    {exact_bytes / 1e6:.1f} MB of strings")
print("(this teaching version uses a whole byte per flag, for readability)")
assert packed_bytes < exact_bytes / 20, "over 20x smaller"


# ------------------ 3. Measure the error, and confirm which direction it goes
false_negatives = sum(1 for item in items if item not in bloom)
print("false negatives:", false_negatives)
assert false_negatives == 0, "this is guaranteed by construction"

never_added = [f"https://example.com/other/{i}" for i in range(100_000)]
false_positives = sum(1 for item in never_added if item in bloom)
rate = false_positives / len(never_added)
print(f"false positives: {false_positives:,} of {len(never_added):,} = {rate:.2%}")
assert 0 < rate < 0.05, "a small, measurable, bounded error rate"
print()
print("So: 'not present' is proof. 'Present' means 'go and check properly'.")


# ---------------------------------------------- 4. The same trade, twice more
class CountMinSketch:
    def __init__(self, width, depth):
        self.width, self.depth = width, depth
        self.counts = [[0] * width for _ in range(depth)]

    def _cols(self, item):
        digest = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(digest[i * 4:i * 4 + 4], "big") % self.width
                for i in range(self.depth)]

    def add(self, item):
        for row, col in enumerate(self._cols(item)):
            self.counts[row][col] += 1

    def estimate(self, item):
        return min(self.counts[row][col] for row, col in enumerate(self._cols(item)))


sketch = CountMinSketch(width=2_000, depth=5)
truth = {"popular": 5_000, "rare": 3}
for item, times in truth.items():
    for _ in range(times):
        sketch.add(item)
for i in range(20_000):
    sketch.add(f"noise{i}")

for item, actual in truth.items():
    guess = sketch.estimate(item)
    print(f"  {item:<8} actual {actual:>5,}  estimated {guess:>5,}")
    assert guess >= actual, "Count-Min never undercounts - it takes the minimum row"
print("Overestimates only. That one-sidedness is what makes it safe to use.")


print()
print("All checks passed.")
