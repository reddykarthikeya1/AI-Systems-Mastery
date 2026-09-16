# Beginner Playground - Distributed Caching and Stampede Prevention

> *"One till closes at a busy supermarket and everybody rushes the next one at the same instant. Nothing failed - everyone simply made the same reasonable decision simultaneously."*

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

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import random
```

---

## 1. Cache-aside, the pattern almost everyone uses

Look in the cache. On a miss, fetch from the database, put it in the cache, return
it. Simple, and it works.

It contains a gap: between "miss" and "put it in the cache", every other request
also misses.

```python
database_calls = {"count": 0}
cache = {}


def load_from_database(key):
    database_calls["count"] += 1
    return f"value for {key}"


def cache_aside(key):
    if key in cache:
        return cache[key]
    value = load_from_database(key)
    cache[key] = value
    return value


database_calls["count"] = 0
for _ in range(5_000):
    cache_aside("popular_key")
print(f"5,000 sequential requests -> {database_calls['count']} database call(s)")
assert database_calls["count"] == 1, "when requests are spread out, the cache works"
```

---

## 2. Now expire it while 5,000 requests are in flight

The requests arrive concurrently. Every one of them checks the cache *before* any
of them has finished writing to it. Every one misses. Every one queries the
database.

Your cache hit ratio for that key drops to zero for the length of one database
query, and the database receives its entire month of avoided load at once.

```python
def concurrent_burst(handler, requests=5_000):
    cache.clear()
    database_calls["count"] = 0
    in_flight = [handler("popular_key", arrival=i) for i in range(requests)]
    return database_calls["count"], in_flight


def naive_handler(key, arrival):
    if key in cache:
        return cache[key]
    value = load_from_database(key)      # all 5,000 arrive here together
    if arrival == 4_999:
        cache[key] = value               # only the last one finishes in time
    return value


calls, _ = concurrent_burst(naive_handler)
print(f"5,000 concurrent requests -> {calls:,} database calls")
assert calls == 5_000, "the database took the full burst"
print("The cache did not fail. It was simply empty at the wrong moment.")
```

---

## 3. Single flight: one request fetches, the rest wait

The fix is a lock per key. The first request to miss takes the lock and does the
work; everyone else waits and uses its answer.

One database call instead of five thousand, and the users who waited waited for
one query rather than for a queue of five thousand.

```python
locks = {}


def single_flight_handler(key, arrival):
    if key in cache:
        return cache[key]
    if key in locks:
        return locks[key]                # somebody else is already fetching
    locks[key] = "pending"
    value = load_from_database(key)
    cache[key] = value
    locks[key] = value
    return value


cache.clear()
locks.clear()
calls, _ = concurrent_burst(single_flight_handler)
print(f"5,000 concurrent requests with single-flight -> {calls} database call(s)")
assert calls == 1, "exactly one request did the work"
```

---

## 4. And stop all the keys expiring together

Second cause of the same outage: you warmed 10,000 keys at start-up with a 1-hour
TTL, so all 10,000 expire in the same second. Single-flight protects each key
individually and does nothing about 10,000 keys at once.

The fix is **jitter** - add a random spread to each TTL so expiry is smeared over
a window instead of landing on one instant.

```python
random.seed(11)
BASE_TTL = 3_600


def expiry_second(jitter_fraction):
    spread = int(BASE_TTL * jitter_fraction)
    return BASE_TTL + random.randint(-spread, spread)


no_jitter = [expiry_second(0.0) for _ in range(10_000)]
with_jitter = [expiry_second(0.1) for _ in range(10_000)]

worst_no_jitter = max(no_jitter.count(t) for t in set(no_jitter))
worst_with_jitter = max(with_jitter.count(t) for t in set(with_jitter))

print(f"no jitter:   worst second expires {worst_no_jitter:,} keys")
print(f"10% jitter:  worst second expires {worst_with_jitter:,} keys")
assert worst_no_jitter == 10_000, "one second carries the whole load"
assert worst_with_jitter < 100, "spread across a 12-minute window"
```

---

## 5. Predict before you run

A popular cache entry expires. In the next 50 milliseconds, 5,000 requests
arrive for it. How many of them go to the database? Now say what happens to
the database.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

A cache stampede takes down the origin *after* the cache has been working
perfectly for months, which is why it is so often a surprise. The expiry is
the trigger, and popularity is the amplifier.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
