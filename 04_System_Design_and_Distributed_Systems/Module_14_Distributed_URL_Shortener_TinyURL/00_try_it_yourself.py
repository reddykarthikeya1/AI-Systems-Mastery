"""Beginner playground for Module 14 - Designing a URL Shortener.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib
import string

# --------------------------------------- 1. Start with the numbers, as always
new_links_per_year = 100_000_000
reads_per_link = 100
SECONDS_PER_YEAR = 31_500_000

write_qps = new_links_per_year / SECONDS_PER_YEAR
read_qps = write_qps * reads_per_link
print(f"writes: {write_qps:>8.0f} per second")
print(f"reads:  {read_qps:>8.0f} per second")
assert round(read_qps / write_qps) == 100
print("100:1 read-heavy. Cache the redirects and this is a small system.")


# ---------------------------------------------- 2. How short can the code be?
ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
assert len(ALPHABET) == 62

for length in (5, 6, 7, 8):
    combos = 62 ** length
    years = combos / new_links_per_year
    print(f"  {length} characters -> {combos:>20,} codes ({years:>12,.0f} years)")

assert 62 ** 7 > 3_500_000_000_000
print("7 characters is 3.5 trillion codes. Comfortably enough.")


# --------------------- 3. Counter plus base62: no collisions, by construction
def to_base62(number):
    if number == 0:
        return ALPHABET[0]
    out = []
    while number:
        number, remainder = divmod(number, 62)
        out.append(ALPHABET[remainder])
    return "".join(reversed(out))


def from_base62(code):
    value = 0
    for character in code:
        value = value * 62 + ALPHABET.index(character)
    return value


for counter in (1, 1_000, 125_000_000):
    code = to_base62(counter)
    print(f"  id {counter:>12,} -> /{code:<6} -> back to {from_base62(code):,}")
    assert from_base62(code) == counter

codes = {to_base62(i) for i in range(50_000)}
assert len(codes) == 50_000, "distinct counters give distinct codes, always"


# --------------------- 4. Why hashing needs a round trip that counters do not
def short_hash(url, length):
    digest = hashlib.sha256(url.encode()).digest()
    number = int.from_bytes(digest[:8], "big")
    return to_base62(number)[:length]


urls = [f"https://example.com/{i}" for i in range(100_000)]
hashed = {}
collisions = 0
for url in urls:
    code = short_hash(url, length=4)
    if code in hashed and hashed[code] != url:
        collisions += 1
    hashed[code] = url

print(f"100,000 URLs into 4-character hashed codes -> {collisions:,} collisions")
assert collisions > 0, "which is why every write must check first"
print("The counter approach needs no check at all. That is the argument for it.")


# -------------------------------------------------- 5. The last two decisions
class IdRangeAllocator:
    def __init__(self, block=1_000_000):
        self.next_block_start = 1
        self.block = block
        self.coordination_calls = 0

    def claim(self):
        self.coordination_calls += 1
        start = self.next_block_start
        self.next_block_start += self.block
        return range(start, start + self.block)


allocator = IdRangeAllocator()
server_a, server_b = allocator.claim(), allocator.claim()
issued = 2_000_000

print(f"ids available without further coordination: {len(server_a) + len(server_b):,}")
print(f"coordination round trips used: {allocator.coordination_calls}")
assert set(server_a) & set(server_b) == set(), "ranges cannot overlap"
assert allocator.coordination_calls == 2, f"2 calls for {issued:,} ids"


print()
print("All checks passed.")
