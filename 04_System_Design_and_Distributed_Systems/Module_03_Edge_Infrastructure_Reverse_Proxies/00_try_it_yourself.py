"""Beginner playground for Module 03 - Edge Infrastructure and Reverse Proxies.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ---------------------- 1. Forward proxy, reverse proxy - which side is it on
backends = ["app-1", "app-2", "app-3"]
tls_terminated_at = "proxy"


def reverse_proxy(request_number):
    return {
        "handled_tls": tls_terminated_at,
        "routed_to": backends[request_number % len(backends)],
    }


for i in range(4):
    print(f"  request {i} ->", reverse_proxy(i)["routed_to"])
assert reverse_proxy(0)["routed_to"] == "app-1"
assert reverse_proxy(3)["routed_to"] == "app-1", "round robin wraps around"
assert all(reverse_proxy(i)["handled_tls"] == "proxy" for i in range(4)), (
    "backends never see a certificate")


# -------------------------------- 2. What a cache hit ratio is actually worth
total_rps = 10_000
for hit_ratio in (0.0, 0.50, 0.90, 0.95, 0.99):
    origin = total_rps * (1 - hit_ratio)
    print(f"  hit ratio {hit_ratio:>5.0%} -> origin sees {origin:>8,.0f} req/s")

assert round(total_rps * (1 - 0.95)) == 500
assert round((total_rps * (1 - 0.90)) / (total_rps * (1 - 0.95))) == 2
print("90% -> 95% is not a 5% improvement. It is half the servers.")


# ----------------------------------------- 3. The cache key is the whole game
cache = {}
origin_hits = {"count": 0}


def fetch(url, key_builder):
    key = key_builder(url)
    if key in cache:
        return "HIT"
    origin_hits["count"] += 1
    cache[key] = "response"
    return "MISS"


def naive_key(url):
    return url                                   # includes every query parameter


def sensible_key(url):
    return url.split("?")[0]                     # ignore tracking parameters


requests = [f"/product/42?utm_source=email&uid={i}" for i in range(1_000)]

origin_hits["count"] = 0
cache.clear()
for url in requests:
    fetch(url, naive_key)
naive_origin = origin_hits["count"]

origin_hits["count"] = 0
cache.clear()
for url in requests:
    fetch(url, sensible_key)
sensible_origin = origin_hits["count"]

print("1,000 requests for the SAME product page")
print(f"  key includes tracking params: {naive_origin:>5,} reached the origin")
print(f"  key strips them:              {sensible_origin:>5,} reached the origin")
assert naive_origin == 1_000, "every request was unique, so nothing was reusable"
assert sensible_origin == 1, "999 requests served from the edge"


# --------------------------- 4. Stale, and why it is usually the right answer
class EdgeCache:
    def __init__(self):
        self.value = None
        self.age = 0

    def get(self, ttl, origin_healthy):
        if self.value is None:
            return "MISS - user waits for the origin"
        if self.age <= ttl:
            return "HIT - fresh"
        if not origin_healthy:
            return "HIT - stale, but the origin is down and this beats a 503"
        return "HIT - stale, served now, refreshed in the background"


edge = EdgeCache()
edge.value, edge.age = "price: 19.99", 400
print(" ", edge.get(ttl=300, origin_healthy=True))
print(" ", edge.get(ttl=300, origin_healthy=False))
print(" ", edge.get(ttl=600, origin_healthy=True))
assert "background" in edge.get(ttl=300, origin_healthy=True)
assert "503" in edge.get(ttl=300, origin_healthy=False)
assert "fresh" in edge.get(ttl=600, origin_healthy=True)


print()
print("All checks passed.")
