# Beginner Playground - Edge Infrastructure and Reverse Proxies

> *"A reverse proxy is the hotel front desk: guests never walk into the kitchen. A CDN is the corner shop - the popular things are already near you."*

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 1. Forward proxy, reverse proxy - which side is it on

A **forward proxy** acts for the *client*: your company's outbound web filter.
A **reverse proxy** acts for the *server*: clients think they are talking to your
service, and it decides which machine actually handles it.

Everything at the edge is a reverse proxy wearing a different hat: load balancing,
TLS termination, rate limiting, compression, and caching. One place to do the
work every backend would otherwise duplicate.

```python
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
```

---

## 2. What a cache hit ratio is actually worth

Origin load is `(1 - hit_ratio) x total`. The interesting property is how
non-linear the relief is at the top end.

Going from 90% to 95% does not sound like much. It halves your origin traffic.

```python
total_rps = 10_000
for hit_ratio in (0.0, 0.50, 0.90, 0.95, 0.99):
    origin = total_rps * (1 - hit_ratio)
    print(f"  hit ratio {hit_ratio:>5.0%} -> origin sees {origin:>8,.0f} req/s")

assert round(total_rps * (1 - 0.95)) == 500
assert round((total_rps * (1 - 0.90)) / (total_rps * (1 - 0.95))) == 2
print("90% -> 95% is not a 5% improvement. It is half the servers.")
```

---

## 3. The cache key is the whole game

A cache stores responses under a **key**. Two requests share a cached response
only if they produce the same key.

Include something that varies per user - a session id, a tracking parameter, a
timestamp - and every request is unique. The cache fills up, nothing is ever
reused, and 100% of traffic reaches the origin. Nothing errors. The dashboards
look fine right up until the origin does not.

```python
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
```

---

## 4. Stale, and why it is usually the right answer

When a cached item expires, the obvious thing is to fetch a fresh one and make the
user wait. `stale-while-revalidate` does better: serve the slightly old copy
immediately and refresh in the background.

And `stale-if-error`: if the origin is *down*, keep serving the stale copy rather
than an error page. A five-minute-old price is almost always better than a 503.

```python
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
```

---

## 5. Predict before you run

A CDN serves 95% of requests from cache. Your origin was handling 10,000
requests per second. What is it handling now? Now suppose someone adds a
per-user tracking parameter to the URL. What is it handling then?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

A cache key mistake is one of the fastest ways to take down a service. The
CDN keeps reporting healthy, every response is correct, and your origin is
suddenly receiving 100% of the traffic it was built to be shielded from.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
